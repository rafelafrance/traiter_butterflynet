"""Parse numbers."""

import re

from traiter.pylib.util import to_positive_int

from ..pylib.util import APPROX, EXTREME, IMPLIED, INT_RE, REPLACE, TRAIT_STEP

NUM_WORD_ENTS = """ elev_word number_word """.split()
UNIT_ENTS = """ metric_length imperial_length """.split()
LEADER_ENTS = """ elev_to elev_approx """.split()
BETWEEN_ENTS = LEADER_ENTS + ['dash']
APPROX_ENTS = """ elev_approx """.split()
REJECT_ENTS = """ time_units sex month """.split()

PREFIX_REJECT = """ ’ ' ° perching perched """.split()
SUFFIX_REJECT = """ species b s e ) ° ' ’ """.split()

FEET_TO_METERS = 0.3048


def elevation(span):
    """Enrich the elevation match."""
    data = {}

    if not (valid_units(span, data) and valid_values(span, data)):
        return {'_forget': True}

    set_extreme(span, data)
    set_approx(span, data)
    set_implied(span, data)

    return data


def valid_units(span, data):
    """Validate and update data units."""
    units = [t.lower_ for t in span if t.ent_type_ in UNIT_ENTS]

    if units:
        units = REPLACE.get(units[0], units[0])

        # Remove bad units
        if units not in ('m', 'ft'):
            return False

        data['elev_units'] = units

    return True


def valid_values(span, data):
    """Validate and update data values."""
    values = [to_positive_int(t.text) for t in span if re.match(INT_RE, t.text)]
    values += [int(REPLACE[t.lower_]) for t in span if t.ent_type_ in NUM_WORD_ENTS]
    values = multiply_values(span, values)

    # Remove triples like" "sea level to one or two thousand feet"
    if len(values) > 1:
        values = [min(values), max(values)]

    units = data.get('elev_units')

    if len(values) == 1 and not units:

        # Remove years
        if 1800 < values[0] < 2000:
            return False

        # Remove values that are too low
        if values[0] < 10:
            return False

    # Handle 2-3000 ft
    elif len(values) == 2 and values[0] < 10 and values[1] % 1000 == 0:
        values[0] *= 1000

    # Handle 1 to 200 m
    elif len(values) == 2 and values[0] < 30 and values[1] % 100 == 0:
        values[0] *= 100

    # Convert feet to meters
    data['elev_ori_values'] = values
    if units == 'ft':
        values = [round(v * FEET_TO_METERS) for v in values]

    # Remove values that are too high
    if values[-1] > 9_000:
        return False

    data['elev_values'] = values

    return True


def multiply_values(span, values):
    """Update values written as 'two to five or six thousand feet'."""
    multiply = [t.text for t in span if t.ent_type_ == 'numeric_units']
    if multiply:
        multiply = int(REPLACE[multiply[0]])
        values = [v * multiply for v in values]
    return values


def set_extreme(span, data):
    """Update the extreme value flag (min or max) on the data dict."""
    extreme = [e for t in span if ((e := EXTREME.get(t.lower_)) is not None)]
    if extreme:
        data['elev_extreme'] = extreme[0]


def set_approx(span, data):
    """Update the extreme approximate value flag on the data dict."""
    approx = [e for t in span if ((e := APPROX.get(t.lower_)) is not None)]
    if approx:
        data['elev_approx'] = True


def set_implied(span, data):
    """Update the the implied value in the data dict."""
    implied = [i for t in span if ((i := IMPLIED.get(t.lower_)) is not None)]
    if implied:
        data['elev_implied'] = implied[0]
        data['ori_elev_implied'] = implied[0]


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
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elev_word'},
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': {'IN': LEADER_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'elev_word'},
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'ENT_TYPE': 'number_word'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'number_word'},
                    {'ENT_TYPE': 'numeric_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': UNIT_ENTS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elev_approx',
            'patterns': [
                [
                    {'ENT_TYPE': {'IN': APPROX_ENTS}},
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
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
                [
                    {'LOWER': {'IN': PREFIX_REJECT}},
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': BETWEEN_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': REJECT_ENTS}},
                ],
                [
                    {'ENT_TYPE': {'IN': UNIT_ENTS}},
                    {'TEXT': {'REGEX': INT_RE}},
                ],
            ],
        },
    ],
}
