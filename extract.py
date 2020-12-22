#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import pandas as pd
from tqdm import tqdm

from src.matchers.pipeline import Pipeline
from src.pylib.util import DATA_DIR, OUTPUT_DIR

IN_XLSX = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.xlsx'
IN_CSV = DATA_DIR / 'trait_download_all_traits_2020-11-23T19-55-54JUSTELEVATION.csv'
OUT_CSV = OUTPUT_DIR / 'BNet_Traits_2020-12-21d.csv'

TARGET = 'Elevation'
KEEP = """
    elev_low elev_high elev_units elev_units_inferred elev_approx
    elev_ori_low elev_ori_high """.split()


def elevations():
    """Extract elevations from a CSV file."""
    df = pd.read_csv(IN_CSV, dtype=str).fillna('')
    df = df.set_index('Unique ID')

    df[TARGET] = df[TARGET].str.strip()
    df[TARGET] = df[TARGET].str.replace(r'(?<=[\d,])\s(?=[\d])', '', regex=True)

    for col in KEEP:
        df[col] = None

    pipeline = Pipeline()

    for index, row in tqdm(df.iterrows()):
        text = row[TARGET]

        if not text:
            continue

        doc = pipeline.nlp(text)
        traits = pipeline.trait_list(doc)
        for trait in traits:
            for key, value in trait.items():
                if key in KEEP:
                    df.at[index, key] = value

    df.to_csv(OUT_CSV, index=False)


if __name__ == '__main__':
    elevations()    # The current one-off project
