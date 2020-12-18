"""Parse numbers."""

import re
from functools import partial

from traiter.pylib.util import to_positive_int

from ..pylib.util import DASH, INT_RE, REPLACE, TRAIT_STEP

MIN_VALUE = -1

WORD_ENTS = 'elevation_word word_number'.split()
UNIT_ENTS = 'metric_length imperial_length'.split()

# Tokens that indicate a single max value follows
MAX_WORDS = """ up   to below about < """.split()
MIN_WORDS = """ down to above about > """.split()
TO_WORDS = 'up to ca about below under and between '.split() + DASH
APPROX_WORDS = ' ca about higher lower above below more less < > ~ '.split()

PREFIX_REJECT = """ ' """.split()
SUFFIX_REJECT = """ species b s e ) ° ' """.split()


def elevation(span, low=None, high=None):
    """Enrich the elevation match."""
    data = {}

    values = [to_positive_int(t.text) for t in span if re.match(INT_RE, t.text)]
    values += [int(REPLACE[t.lower_]) for t in span if t.ent_type_ in WORD_ENTS]
    values = multiply_values(span, values)

    data['elev_low'] = low if low is not None else min(values)
    if high != MIN_VALUE:
        data['elev_high'] = high if high is not None else max(values)

    if problem_units(span, data) or problem_values(data):
        return {'_forget': True}

    return data


def multiply_values(span, values):
    """Update values written as 'two to five or six thousand feet'."""
    multiply = [t.text for t in span if t.ent_type_ == 'numeric_units']
    if multiply:
        multiply = int(REPLACE[multiply[0]])
        values = [v * multiply for v in values]
    return values


def problem_units(span, data):
    """Flag values that are problematic."""
    units = [t.lower_ for t in span if t.ent_type_ in UNIT_ENTS]
    if units:
        units = REPLACE.get(units[0], units[0])
        data['elevation_units'] = units

        # Remove bad units
        if units not in ('m', 'ft'):
            return True

        # Remove extreme values
        high = data.get('elev_high')
        if (high is not None and (
                (units == 'm' and high > 9_000) or (units == 'ft' and high > 30_000))):
            return True

    return False


def problem_values(data):
    """Flag values that are problematic."""
    low = data.get('elev_low')
    high = data.get('elev_high')

    if high is None or low == high:
        # Filter years like "1937"
        if not data.get('elevation_units') and 1900 < low < 2000:
            return True

    return False


def not_an_elevation(_):
    """Negative matches."""
    return {'_forget': True}


ELEVATION = {
    TRAIT_STEP: [
        {
            'label': 'elevation',
            'on_match': elevation,
            'patterns': [
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                    {'LOWER': {'IN': TO_WORDS}},
                    {'LOWER': {'IN': TO_WORDS}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elevation_word'},
                    {'LOWER': {'IN': TO_WORDS}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'ENT_TYPE': 'numeric_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elevation_word'},
                    {'LOWER': {'IN': TO_WORDS}, 'OP': '?'},
                    {'LOWER': {'IN': TO_WORDS}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elevation',
            'on_match': partial(elevation, low=0),
            'patterns': [
                [
                    {'LOWER': {'IN': MAX_WORDS}},
                    {'LOWER': {'IN': MAX_WORDS}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elevation',
            'on_match': partial(elevation, high=MIN_VALUE),
            'patterns': [
                [
                    {'LOWER': {'IN': MIN_WORDS}},
                    {'LOWER': {'IN': MIN_WORDS}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elevation_approx',
            'patterns': [
                [
                    {'LOWER': {'IN': APPROX_WORDS}},
                ],
            ],
        },
        {
            'label': 'not_an_elevation',
            'on_match': not_an_elevation,
            'patterns': [
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'LOWER': {'IN': SUFFIX_REJECT}},
                ],
                [
                    {'LOWER': {'IN': PREFIX_REJECT}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
                [
                    {'LOWER': {'IN': PREFIX_REJECT}},
                    {'LOWER': {'IN': DASH}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
            ],
        },
    ],
}
