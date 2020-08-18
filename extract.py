#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import pandas as pd

from src.pylib.pipeline import parse
from src.pylib.util import CSV, XLSX, clean_text

TARGET = 'Full Species Account'


def main():
    """Extract data from the files."""
    df = pd.read_excel(XLSX, dtype=str).fillna('')
    df = df.set_index('Serial')
    for index, row in df.iterrows():
        text = clean_text(row[TARGET])
        traits = parse(text)
        traits = sorted(traits, key=lambda t: (t['trait'], t['start']))
        for i, trait in enumerate(traits[:4], 1):
            name = f'{trait["trait"]}.{i}'
            if name not in df.columns:
                df[name] = ''
            df.at[index, name] = trait[trait['trait']]

    df.to_csv(CSV)


if __name__ == '__main__':
    main()
