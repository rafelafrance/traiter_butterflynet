"""Get terms from various sources (CSV files or SQLite database."""

import csv

from .util import NAME, VOCAB_DIR

BUTTERFLY_TERMS = VOCAB_DIR / f'{NAME}.csv'


def read_terms(term_path):
    """Read and cache the terms."""
    with open(term_path) as term_file:
        reader = csv.DictReader(term_file)
        return list(reader)


TERMS = read_terms(BUTTERFLY_TERMS)

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
