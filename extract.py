#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import pandas as pd
import regex as re
import tqdm
from traiter.pylib.util import FLAGS, clean_text

from src.pylib.pipeline import parse
from src.pylib.util import CSV, XLSX

TARGET = 'Full Species Account'


def main():
    """Extract data from the files."""
    df = pd.read_excel(XLSX, dtype=str).fillna('')
    df = df.set_index('Serial')
    # for index, row in df.iterrows():
    for index, row in tqdm.tqdm(df.iterrows()):
        text = clean_text(row[TARGET])
        traits, sents = parse(text, with_sents=True)

        traits = sorted(traits, key=lambda t: (t['trait'], t['start']))
        for i, trait in enumerate(traits, 1):
            name = f'{trait["trait"]}.{i}'
            if name not in df.columns:
                df[name] = ''
            df.at[index, name] = trait[trait['trait']]

        # for start, end in sents:
        #     sent = text[start:end]
        #     if re.search(r'mimic', sent, flags=FLAGS):
        #         print(sent)

    df.to_csv(CSV)


if __name__ == '__main__':
    main()
