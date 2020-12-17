"""Merge multiple elevation traits into one for each document."""

from spacy.tokens import Span

from ..pylib.util import MERGE_STEP

ELEVATIONS = """ elevation elevation_approx """.split()

KEYS = """
    trait start end elevation_units elevation_approx elevation_low elevation_high
    """.split()

MIN = -1
MAX = 99_999_999


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

    if merged['elevation_low'] == merged['elevation_high']:
        merged['elevation_low'] = None

    ent = Span(doc, merged['start_idx'], merged['end_idx'], label=merged['trait'])
    ent._.step = MERGE_STEP
    ent._.data = {k: v for k, v in merged.items() if k in KEYS and v is not None}

    entities = [e for e in doc.ents if e.label_ not in ELEVATIONS]
    if merged['elevation_low'] != MAX and merged['elevation_high'] != MIN:
        entities += [ent]

    doc.ents = tuple(entities)

    return doc


def expand_range(data, merged, partial):
    """Expand the range of the elevations."""
    if partial.label_ == 'elevation_approx' or data.get('elevation_approx'):
        merged['elevation_approx'] = True

    if (value := data.get('elevation_low')) is not None:
        merged['elevation_low'] = min(merged['elevation_low'], value)
    if (value := data.get('elevation_high')) is not None:
        merged['elevation_high'] = max(merged['elevation_high'], value)


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
        'start': MAX,
        'end': MIN,
        'start_idx': MAX,
        'end_idx': MIN,
        'elevation_low': MAX,
        'elevation_high': MIN,
        'elevation_units': '',
        'elevation_approx': None,
    }


def reset_entity_data(data):
    """Reset the new entity object."""
    data['elevation_low'] = MAX
    data['elevation_high'] = MIN
    data['elevation_units'] = ''
