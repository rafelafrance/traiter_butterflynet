"""Parse numbers."""

import re
from functools import partial

from traiter.pylib.util import to_positive_int

from ..pylib.util import DASH, INT_RE, REPLACE, TRAIT_STEP

TO = 'up to and'.split() + DASH
MAX = 'up to'.split()
HIGH = 'below under'.split()
WORDS = 'elevation_word word_number'.split()
UNITS = 'metric_length imperial_length'.split()
HIGH_APPROX = 'higher'.split()


def elevation(span, fields=''):
    """Enrich the elevation match."""
    fields = fields.split()
    data = {}

    values = [t.text for t in span if re.match(INT_RE, t.text)]
    for field, value in zip(fields, values):
        data[field] = to_positive_int(value)

    units = [t.lower_ for t in span if t.ent_type_ in UNITS]
    if units:
        data['elevation_units'] = REPLACE.get(units[0], units[0])

    return data


def elevation_words(span, fields=''):
    """Convert words to numbers before enriching the match."""
    fields = fields.split()
    data = {}

    values = [t.text for t in span if t.ent_type_ in WORDS]
    for field, value in zip(fields, values):
        data[field] = int(REPLACE.get(value, value))

    multiply = [t.text for t in span if t.ent_type_ == 'numeric_units']
    if multiply:
        multiply = int(REPLACE[multiply[0]])
        for field in fields:
            data[field] *= multiply

    units = [t for t in span if t.ent_type_ in UNITS]
    if units:
        if units[0].ent_type_ == 'imperial_length':
            data['imperial_length'] = True
        units = units[0].lower_
        data['elevation_units'] = REPLACE.get(units, units)

    return data


ELEVATION = {
    TRAIT_STEP: [
        {
            'label': 'elevation',
            'on_match': partial(
                elevation,
                fields='elevation_low elevation_high'),
            'patterns': [
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
                [
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                    {'LOWER': {'IN': TO}},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'max_elevation',
            'on_match': partial(elevation, fields='elevation_max'),
            'patterns': [
                [
                    {'LOWER': {'IN': MAX}},
                    {'LOWER': {'IN': MAX}, 'OP': '?'},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'high_elevation',
            'on_match': partial(elevation, fields='elevation_high'),
            'patterns': [
                [
                    {'LOWER': {'IN': HIGH}},
                    {'TEXT': {'REGEX': INT_RE}},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'elevation',
            'on_match': partial(
                elevation_words,
                fields='elevation_low elevation_high elevation_max'),
            'patterns': [
                [
                    {'ENT_TYPE': 'elevation_word'},
                    {'LOWER': {'IN': TO}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'POS': {'IN': ['CCONJ']}, 'OP': '?'},
                    {'ENT_TYPE': 'word_number'},
                    {'ENT_TYPE': 'numeric_units', 'OP': '?'},
                    {'ENT_TYPE': {'IN': UNITS}, 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'high_elevation_approx',
            'patterns': [
                [
                    {'LOWER': {'IN': HIGH_APPROX}},
                ],
            ],
        },
    ],
}
