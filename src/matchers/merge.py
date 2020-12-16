"""Merge multiple elevation traits into one for each document."""

from spacy.tokens import Span

from ..pylib.util import MERGE_STEP

ELEVATIONS = """
    elevation max_elevation high_elevation high_elevation_approx """.split()

KEYS = """
    trait start end
    elevation_units elevation_high_approx
    elevation_min elevation_low elevation_high elevation_max
    """.split()

MIN = -1
MAX = 99_999_999


def merge(doc):
    """Merge multiple elevation traits into one for each document."""
    elevations = [e for e in doc.ents if e.label_ in ELEVATIONS]
    if len(elevations) < 2:
        return doc

    merged = init_entity_data()

    for partial in elevations:
        data = partial._.data

        merged['start_idx'] = min(merged['start_idx'], partial.start)
        merged['end_idx'] = max(merged['end_idx'], partial.end)

        merged['start'] = min(merged['start'], partial.start_char)
        merged['end'] = max(merged['end'], partial.end_char)

        if units := data.get('elevation_units'):
            imperial = data.get('imperial_length', False)
            # If no units in merged then update things
            if not merged['elevation_units']:
                merged['elevation_units'] = units
                merged['imperial_length'] = imperial
            # If merged units are imperial and partial units are metric
            # then reset object and add the new data
            elif merged['imperial_length'] and not imperial:
                reset_entity_data(merged)
                merged['elevation_units'] = units
                merged['imperial_length'] = imperial
            # If merged and partial units don't match then skip the entity
            elif merged['elevation_units'] != units:
                continue
            # Else just extend the range

        if partial.label_ == 'high_elevation':
            print('high_elevation')
            continue

        if partial.label_ == 'high_elevation_approx':
            merged['elevation_high_approx'] = True

        if (value := data.get('elevation_min')) is not None:
            merged['elevation_min'] = min(merged['elevation_min'], value)

        if (value := data.get('elevation_low')) is not None:
            merged['elevation_low'] = min(merged['elevation_low'], value)

        if (value := data.get('elevation_high')) is not None:
            merged['elevation_high'] = max(merged['elevation_high'], value)

        if (value := data.get('elevation_max')) is not None:
            merged['elevation_max'] = max(merged['elevation_max'], value)

    ent = Span(doc, merged['start_idx'], merged['end_idx'], label=merged['trait'])
    ent._.step = MERGE_STEP
    ent._.data = {k: v for k, v in merged.items()
                  if k in KEYS and v != MIN and v != MAX and v is not None}

    entities = [e for e in doc.ents if e.label_ not in ELEVATIONS]
    entities += [ent]

    doc.ents = tuple(entities)

    return doc


def init_entity_data():
    """Initialize the new entity object."""
    return {
        'trait': 'elevation',
        'start': MAX,
        'end': MIN,
        'start_idx': MAX,
        'end_idx': MIN,
        'elevation_min': MAX,
        'elevation_low': MAX,
        'elevation_high': MIN,
        'elevation_max': MIN,
        'elevation_units': '',
        'elevation_high_approx': None,
        'imperial_length': False
    }


def reset_entity_data(data):
    """Reset the new entity object."""
    data['elevation_min'] = MAX
    data['elevation_low'] = MAX
    data['elevation_high'] = MIN
    data['elevation_max'] = MIN
    data['elevation_units'] = ''
    data['imperial_length'] = False
