"""Merge multiple elevation traits into one for each document."""

from spacy.tokens import Span

from ..pylib.util import MERGE_STEP

ELEVATION = """ elevation elev_approx """.split()

KEYS = """
    trait start end elev_units elev_approx elev_low elev_high
    """.split()

# Sentinels for expanding elevation ranges
MIN_VALUE = -1
MAX_VALUE = 99_999_999


def merge(doc):
    """Merge multiple elevation traits into one for each document."""
    elevations = [e for e in doc.ents if e.label_ in ELEVATION]

    merged = {
        'trait': 'elevation',
        'start': MAX_VALUE,
        'end': MIN_VALUE,
        'start_idx': MAX_VALUE,
        'end_idx': MIN_VALUE,
        'elev_low': MAX_VALUE,
        'elev_high': MIN_VALUE,
        'implied_low': MAX_VALUE,
        'implied_high': MIN_VALUE,
        'elev_units': '',
    }

    for elev in elevations:
        data = elev._.data

        update_indexes(elev, merged)

        if elev.label_ == 'elev_approx':
            merged['elev_approx'] = True
            continue

        if not update_units(data, merged):
            continue

        update_range(data, merged)

        if data.get('elev_approx'):
            merged['elev_approx'] = True

    adjust_range(merged)
    update_doc_entities(doc, merged)

    return doc


def update_indexes(elev, merged):
    """Update the indexes to include the current elevation match."""
    merged['start_idx'] = min(merged['start_idx'], elev.start)
    merged['end_idx'] = max(merged['end_idx'], elev.end)
    merged['start'] = min(merged['start'], elev.start_char)
    merged['end'] = max(merged['end'], elev.end_char)


def update_units(data, merged):
    """Update the units for the merged entity."""
    if units := data.get('elev_units'):

        # If no units in merged then update things
        if not merged['elev_units']:
            merged['elev_units'] = units

        # If merged units are imperial and data units are metric
        # then reset object and add the new metric elevations
        elif merged['elev_units'] == 'ft' and units == 'm':
            merged['elev_low'] = MAX_VALUE
            merged['elev_high'] = MIN_VALUE
            merged['elev_units'] = units

        # If merged and partial units don't match then skip the entity
        elif merged['elev_units'] != units:
            return False

        # Else just extend the range
    return True


def update_range(data, merged):
    """Expand the range of the elevations to include the current data."""
    # Make sure the data length is 2
    values = (data['elev_values'] + [None])[:2]
    extreme = data.get('elev_extreme')

    if values[-1] is not None:
        # The is a real range with both low and high values
        merged['elev_low'] = min(values[0], merged['elev_low'])
        merged['elev_high'] = max(values[1], merged['elev_high'])
    elif extreme == 'min':
        merged['elev_low'] = min(values[0], merged['elev_low'])
        if (implied := data.get('elev_implied')) is not None:
            merged['implied_high'] = int(implied)
    elif extreme == 'max':
        merged['elev_high'] = max(values[0], merged['elev_high'])
        if (implied := data.get('elev_implied')) is not None:
            merged['implied_low'] = int(implied)
    else:
        merged['elev_low'] = min(values[0], merged['elev_low'])
        merged['elev_high'] = max(values[0], merged['elev_high'])


def update_doc_entities(doc, merged):
    """Update the doc entities to replace the old elevations with the merged one."""
    entities = [e for e in doc.ents if e.label_ not in ELEVATION]

    if merged['start'] != MAX_VALUE:
        ent = Span(doc, merged['start_idx'], merged['end_idx'], label=merged['trait'])
        ent._.step = MERGE_STEP
        ent._.data = {k: v for k, v in merged.items() if k in KEYS and v is not None}
        entities += [ent]

    doc.ents = tuple(entities)


def adjust_range(merged):
    """Correct range values to remove sentinels etc."""
    if (merged['elev_low'] != MAX_VALUE and merged['elev_high'] != MIN_VALUE
            and merged['elev_low'] > merged['elev_high']):
        lo, hi = merged['elev_low'], merged['elev_high']
        merged['elev_low'], merged['elev_high'] = hi, lo

    if merged['elev_low'] == MAX_VALUE and merged['implied_low'] != MAX_VALUE:
        merged['elev_low'] = merged['implied_low']

    if merged['elev_high'] == MIN_VALUE and merged['implied_high'] != MIN_VALUE:
        merged['elev_high'] = merged['implied_low']

    if merged['elev_low'] == MAX_VALUE:
        merged['elev_low'] = None

    if merged['elev_high'] == MIN_VALUE:
        merged['elev_high'] = None

    if merged['elev_low'] == merged['elev_high']:
        merged['elev_low'] = None
