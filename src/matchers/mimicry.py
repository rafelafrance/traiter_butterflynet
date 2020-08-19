"""Parse dimorphism notations."""


def mimicry(span):
    """Enrich the match."""
    data = {'mimicry': span.lower_}
    sexes = set()
    for token in span:
        if token.ent_type_ == 'sex':
            if token.lower_ in sexes:
                return {}
            sexes.add(token.lower_)
    return data


MIMICRY = {
    'name': 'mimicry',
    'traits': [
        {
            'label': 'mimicry',
            'on_match': mimicry,
            'patterns': [
                [
                    {'ENT_TYPE': 'sex', 'OP': '?'},
                    {'POS': {'IN': ['ADJ', 'CCONJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'mimic'},
                    {'POS': {'IN': ['ADP']}, 'OP': '?'},
                ],
                [
                    {'LEMMA': 'be', 'OP': '?'},
                    {'POS': {'IN': ['DET']}, 'OP': '*'},
                    {'ENT_TYPE': 'mimic'},
                    {'LEMMA': 'by', 'OP': '?'},
                    {'POS': {'IN': ['DET', 'NOUN', 'ADP', 'ADJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'flying', 'OP': '?'},
                    {'POS': {'IN': ['DET', 'NOUN', 'ADP', 'ADJ']}, 'OP': '*'},
                    {'ENT_TYPE': 'butterfly'},
                ],
            ],
        },
    ],
}
