"""Parse dimorphism notations."""

from .consts import TRAIT_STEP


def mimicry(span):
    """Enrich the match."""
    data = {'mimicry': span.lower_}
    sexes = set()
    for token in span:
        if token.ent_type_ in {'female', 'male'}:
            if token.lower_ in sexes:
                return {}
            sexes.add(token.lower_)
    return data


MIMICRY = {
    TRAIT_STEP: [
        {
            'label': 'mimicry',
            'on_match': mimicry,
            'patterns': [
                [
                    {'ENT_TYPE': 'female', 'OP': '?'},
                    {'POS': {'IN': ['ADJ', 'CCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'mimic'},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                ],
                [
                    {'ENT_TYPE': 'male', 'OP': '?'},
                    {'POS': {'IN': ['ADJ', 'CCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'mimic'},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                ],
                [
                    {'LEMMA': 'be', 'OP': '?'},
                    {'POS': {'IN': ['DET']}, 'OP': '*'},
                    {'ENT_TYPE': 'mimic'},
                    {'LEMMA': 'by', 'OP': '?'},
                    {'POS': {'IN': ['DET', 'NOUN', 'ADP', 'ADJ', 'PROPN']}, 'OP': '*'},
                    {'ENT_TYPE': 'flying', 'OP': '?'},
                    {'POS': {'IN': ['DET', 'NOUN', 'ADP', 'ADJ', 'PROPN']}, 'OP': '*'},
                    {'ENT_TYPE': 'butterfly'},
                ],
                [
                    {'LOWER': {'REGEX': '^resembl'}},
                ],
            ],
        },
    ],
}
