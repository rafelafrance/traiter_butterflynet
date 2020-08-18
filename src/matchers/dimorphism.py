"""Parse dimorphism notations."""


def dimorphism(span):
    """Enrich the match."""
    data = {'dimorphism': span.lower_}
    sexes = set()
    for token in span:
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
    data = {}
    return data


_SIMILARITY_LEMMAS = """
    similar different dissimilar vary """.split()

_RESEMBLE_LEMMAS = _SIMILARITY_LEMMAS + """ resemble """.split()

_SIZE_LEMMAS = """ large small """.split()

_SEASON_LEMMAS = """ season seasonal """.split()


DIMORPHISM = {
    'name': 'dimorphism',
    'traits': [
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
                    {'ENT_TYPE': 'sex'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _RESEMBLE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP']}, 'OP': '*'},
                    {'ENT_TYPE': 'sex'},
                ],
                [
                    {'ENT_TYPE': 'sex'},
                    {'LEMMA': {'IN': ['be']}, 'OP': '?'},
                    {'POS': {'IN': ['ADV']}, 'OP': '?'},
                    {'LEMMA': {'IN': _SIZE_LEMMAS}},
                    {'POS': {'IN': ['DET', 'ADP', 'SCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'sex'},
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
                    {'ENT_TYPE': 'sexes'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':'},
                    {'ENT_TYPE': {'NOT_IN': ['sex', 'sexes', 'dimorphic']},
                     'OP': '*'},
                    {'ENT_TYPE': 'sex'},
                    {'ENT_TYPE': {'NOT_IN': ['sex', 'sexes', 'dimorphic']},
                     'OP': '*'},
                    {'ENT_TYPE': 'sex'},
                ],
                [
                    {'ENT_TYPE': 'sexes'},
                    {'ENT_TYPE': 'dimorphic'},
                    {'TEXT': ':'},
                    {'ENT_TYPE': {'NOT_IN': ['sex', 'sexes', 'dimorphic']},
                     'OP': '*'},
                    {'ENT_TYPE': 'sex'},
                ],
            ],
        },
    ],
}
