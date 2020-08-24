#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import pandas as pd
import tqdm
from traiter.pylib.util import clean_text

from src.pylib.pipeline import Pipeline
from src.pylib.util import CSV, XLSX

TARGET = 'Full Species Account'


def main():
    """Extract data from the files."""
    df = pd.read_excel(XLSX, dtype=str).fillna('')
    df = df.set_index('Serial')
    pipeline = Pipeline()
    for index, row in tqdm.tqdm(df.iterrows()):
        text = clean_text(row[TARGET])
        traits = pipeline.trait_list(text)
        traits = sorted(traits, key=lambda t: (t['trait'], t['start']))
        for i, trait in enumerate(traits, 1):
            name = f'{trait["trait"]}.{i}'
            if name not in df.columns:
                df[name] = ''
            df.at[index, name] = trait[trait['trait']]

    df.to_csv(CSV)


if __name__ == '__main__':
    main()
