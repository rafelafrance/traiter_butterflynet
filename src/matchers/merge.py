"""Merge multiple elevation traits into one for each document."""

from spacy.tokens import Span

from ..pylib.util import MERGE_STEP

ELEVATIONS = """ elevation elevation_approx """.split()

KEYS = """
    trait start end elevation_units elevation_approx elev_low elev_high
    """.split()

MIN_VALUE = -1
MAX_VALUE = 99_999_999


def merge(doc):
    """Merge multiple elevation traits into one for each document."""
    elevations = [e for e in doc.ents if e.label_ in ELEVATIONS]
    if len(elevations) == 0:
        return doc

    merged = init_entity_data()

    for partial in elevations:
        data = partial._.data

        merged['start_idx'] = min(merged['start_idx'], partial.start)
        merged['end_idx'] = max(merged['end_idx'], partial.end)

        merged['start'] = min(merged['start'], partial.start_char)
        merged['end'] = max(merged['end'], partial.end_char)

        if not update_units(data, merged):
            continue

        expand_range(data, merged, partial)

    if merged['elev_low'] == merged['elev_high']:
        merged['elev_low'] = None
    elif merged['elev_high'] <= MIN_VALUE:
        merged['elev_high'] = None
    elif merged['elev_low'] > merged['elev_high']:
        low, high = merged['elev_low'], merged['elev_high']
        merged['elev_low'], merged['elev_high'] = high, low

    ent = Span(doc, merged['start_idx'], merged['end_idx'], label=merged['trait'])
    ent._.step = MERGE_STEP
    ent._.data = {k: v for k, v in merged.items() if k in KEYS and v is not None}

    entities = [e for e in doc.ents if e.label_ not in ELEVATIONS]
    if merged['elev_low'] != MAX_VALUE and merged['elev_high'] != MIN_VALUE:
        entities += [ent]

    doc.ents = tuple(entities)

    return doc


def expand_range(data, merged, partial):
    """Expand the range of the elevations."""
    if partial.label_ == 'elevation_approx' or data.get('elevation_approx'):
        merged['elevation_approx'] = True

    data_low = data.get('elev_low')
    data_high = data.get('elev_high')
    merged_low = merged.get('elev_low')
    merged_high = merged.get('elev_high')

    if data_low is not None:
        min_values = [data_low, merged_low]
        if merged_high != MIN_VALUE:
            min_values += [merged_high]
        merged['elev_low'] = min(v for v in min_values if v is not None)

    if data_high is not None:
        max_values = [data_high, merged_high]
        if merged_low != MAX_VALUE:
            max_values += [merged_low]
        merged['elev_high'] = max(v for v in max_values if v is not None)


def update_units(data, merged):
    """Update the units for the merged entity."""
    if units := data.get('elevation_units'):

        # If no units in merged then update things
        if not merged['elevation_units']:
            merged['elevation_units'] = units

        # If merged units are imperial and partial units are metric
        # then reset object and add the new data
        elif merged['elevation_units'] == 'ft' and units == 'm':
            reset_entity_data(merged)
            merged['elevation_units'] = units

        # If merged and partial units don't match then skip the entity
        elif merged['elevation_units'] != units:
            return False

        # Else just extend the range
    return True


def init_entity_data():
    """Initialize the new entity object."""
    return {
        'trait': 'elevation',
        'start': MAX_VALUE,
        'end': MIN_VALUE,
        'start_idx': MAX_VALUE,
        'end_idx': MIN_VALUE,
        'elev_low': MAX_VALUE,
        'elev_high': MIN_VALUE,
        'elevation_units': '',
        'elevation_approx': None,
    }


def reset_entity_data(data):
    """Reset the new entity object."""
    data['elev_low'] = MAX_VALUE
    data['elev_high'] = MIN_VALUE
    data['elevation_units'] = ''
