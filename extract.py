#!/usr/bin/env python3

"""Extract butterfly traits from scientific literature."""

import csv

import chardet
import pandas as pd

from src.pylib.util import XLSX

# from src.pylib.pipeline import parse


TARGET = 'Full Species Account'


def main():
    """Extract data from the files."""
    df = pd.read_excel(XLSX)
    for index, row in df.iterrows():
        data = bytes(row[TARGET])
        enc = chardet.detect(data)
        print(enc)


if __name__ == '__main__':
    main()
