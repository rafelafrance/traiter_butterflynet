#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import pandas as pd

from src.matchers.pipeline import Pipeline
from src.pylib.util import DATA_DIR

IN_XLSX = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.xlsx'
IN_CSV = DATA_DIR / 'trait_download_all_traits_2020-11-23T19-55-54JUSTELEVATION.csv'
OUT_CSV = DATA_DIR / 'BNet_Traits_2020-12-15a.csv'

TARGET = 'Elevation'


def main():
    """Extract data from the files."""
    df = pd.read_csv(IN_CSV, dtype=str).fillna('')
    df = df.set_index('Unique ID')
    df[TARGET] = df[TARGET].str.strip()
    df[TARGET] = df[TARGET].str.replace(r'(?<=\d)\s(?=\d)', '', regex=True)

    pipeline = Pipeline()

    for doc in pipeline.nlp.pipe(df[TARGET]):
        traits = pipeline.trait_list(doc)
        if doc.text:
            print('=' * 80)
            print(doc)
            for trait in traits:
                print(trait)
            print()

    # df.to_csv(OUT_CSV)


if __name__ == '__main__':
    main()
