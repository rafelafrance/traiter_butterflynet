"""Parse numbers."""

import re

from traiter.pylib.util import to_positive_int

from ..pylib.util import DASH, INT_RE, REPLACE, TRAIT_STEP

TO = 'up to about below under and between '.split() + DASH
WORDS = 'elevation_word word_number'.split()
UNITS = 'metric_length imperial_length'.split()
APPROX = ' ca about higher lower above below more less < > ~ '.split()

PREFIX_NO = """ ' """.split()
SUFFIX_NO = """ species b s e ) ° ' """.split()


def elevation(span):
    """Enrich the elevation match."""
    data = {}

    values = [to_positive_int(t.text) for t in span if re.match(INT_RE, t.text)]
    values += [int(REPLACE[t.lower_]) for t in span if t.ent_type_ in WORDS]

    multiply = [t.text for t in span if t.ent_type_ == 'numeric_units']
    if multiply:
        multiply = int(REPLACE[multiply[0]])
        values = [v * multiply for v in values]

    data['elevation_low'] = min(values)
    data['elevation_high'] = max(values)

    # Set up the units
    units = [t.lower_ for t in span if t.ent_type_ in UNITS]
    if units:
        units = REPLACE.get(units[0], units[0])
        data['elevation_units'] = units

        # Remove ridiculous values.
        if (units not in ('m', 'ft')
                or (units == 'm' and data['elevation_high'] > 9_000)
                or (units == 'ft' and data['elevation_high'] > 30_000)):
            return {'_forget': True}

    if data['elevation_low'] == data['elevation_high']:

        # handle "up to 6000 m."
        if span[0].lower_ == 'up' and span[1].lower_:
            data['elevation_approx'] = True

        # Filter years like "1937"
        if not data.get('elevation_units') and 1900 < data['elevation_high'] < 2000:
            return {'_forget': True}

    return data


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
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
                [
                    {'TEXT': {'REGEX': INT_RE}, 'OP': '?'},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                    {'LOWER': {'IN': TO}},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elevation_word'},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'ENT_TYPE': 'numeric_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elevation_word'},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elevation_approx',
            'patterns': [
                [
                    {'LOWER': {'IN': ['or']}, 'OP': '?'},
                    {'LOWER': {'IN': APPROX}},
                ],
                [
                    {'LOWER': {'IN': ['or']}},
                    {'LOWER': {'IN': ['more']}},
                ],
            ],
        },
        {
            'label': 'not_an_elevation',
            'on_match': not_an_elevation,
            'patterns': [
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'LOWER': {'IN': SUFFIX_NO}},
                ],
                [
                    {'LOWER': {'IN': PREFIX_NO}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
                [
                    {'LOWER': {'IN': PREFIX_NO}},
                    {'LOWER': {'IN': DASH}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
            ],
        },
    ],
}
