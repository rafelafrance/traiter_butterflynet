"""Parse dimorphism notations."""

from .consts import GROUP_STEP, TRAIT_STEP

_SIMILARITY_LEMMAS = """
    similar different dissimilar vary """.split()

_RESEMBLE_LEMMAS = _SIMILARITY_LEMMAS + """ resemble """.split()

_SIZE_LEMMAS = """ large small """.split()

_SEASON_LEMMAS = """ season seasonal """.split()


def dimorphism(span):
    """Enrich the match."""
    data = {'dimorphism': span.lower_}
    sexes = set()
    for token in span:
        if token.lower_ in _SEASON_LEMMAS:
            return {}
        if token.ent_type_ == 'sex':
            if token.lower_ in sexes:
                return {}
            sexes.add(token.lower_)
    return data


def dimorphism_trunc(_):
    """Enrich the match."""
    data = {'dimorphism': 'sexual dimorphism'}
    return data


def not_dimorphism(_):
    """Enrich the match."""
    data = {'_forget': True}
    return data


_STOPPERS = ['female', 'male', 'sexes', 'dimorphic']

DIMORPHISM = {
    GROUP_STEP: [
        {
            'label': 'dimorphism_key',
            'patterns': [
                [
                    {'ENT_TYPE': 'sexes', 'OP': '?'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':'},
                ],
            ],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'dimorphism',
            'on_match': dimorphism,
            'patterns': [
                [
                    {'POS': 'DET', 'OP': '?'},
                    {'POS': 'ADJ', 'OP': '?'},
                    {'ENT_TYPE': 'sexes'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'POS': 'PART', 'OP': '?'},
                    {'POS': {'IN': ['ADJ', 'ADV']}, 'OP': '*'},
                ],
                [
                    {'ENT_TYPE': 'sexes', 'OP': '?'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':', 'OP': '?'},
                    {'POS': {'IN': ['AUX', 'PART', 'ADV']}, 'OP': '*'},
                    {'POS': {'IN': ['NOUN', 'VERB']}},
                ],
                [
                    {'ENT_TYPE': 'dimorphism_key'},
                    {'POS': {'IN': ['AUX', 'PART', 'ADV']}, 'OP': '*'},
                    {'POS': {'IN': ['NOUN', 'VERB']}},
                ],
                [
                    {'POS': {'IN': ['PART', 'ADV']}, 'OP': '?'},
                    {'ENT_TYPE': 'sexes', 'OP': '?'},
                    {'ENT_TYPE': 'dimorphic'},
                ],
                [
                    {'ENT_TYPE': 'sexes'},
                    {'POS': {'IN': ['AUX', 'PART', 'ADV', 'ADJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'dimorphic'},
                ],
                [
                    {'ENT_TYPE': 'sexes'},
                    {'TEXT': ':', 'OP': '?'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _SIMILARITY_LEMMAS}},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'female'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _RESEMBLE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP']}, 'OP': '*'},
                    {'ENT_TYPE': 'male'},
                ],
                [
                    {'ENT_TYPE': 'female'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _SIZE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP', 'SCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'male'},
                ],
                [
                    {'ENT_TYPE': 'male'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _RESEMBLE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP']}, 'OP': '*'},
                    {'ENT_TYPE': 'female'},
                ],
                [
                    {'ENT_TYPE': 'male'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _SIZE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP', 'SCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'female'},
                ],
            ],
        },
        {
            'label': 'dimorphism',
            'on_match': not_dimorphism,
            'patterns': [
                [
                    {'ENT_TYPE': 'sexes'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':', 'OP': '?'},
                ],
                [
                    {'LEMMA': {'IN': _SEASON_LEMMAS}},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':', 'OP': '?'},
                ],
            ],
        },
        {
            'label': 'dimorphism',
            'on_match': dimorphism_trunc,
            'patterns': [
                [
                    {'ENT_TYPE': 'dimorphism_key'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'female'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'male'},
                ],
                [
                    {'ENT_TYPE': 'dimorphism_key'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'female'},
                ],
                [
                    {'ENT_TYPE': 'dimorphism_key'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'male'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'female'},
                ],
                [
                    {'ENT_TYPE': 'dimorphism_key'},
                    {'ENT_TYPE': {'NOT_IN': _STOPPERS}, 'OP': '*'},
                    {'ENT_TYPE': 'male'},
                ],
            ],
        },
    ],
}
