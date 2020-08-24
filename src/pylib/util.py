"""Utilities and constants."""

from pathlib import Path

NAME = 'lepidoptera'

DATA_DIR = Path('.') / 'data'
VOCAB_DIR = Path('.') / 'src' / 'vocabulary'

XLSX = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.xlsx'
CSV = DATA_DIR / 'BNet_Traits_2020-08-19a.csv'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
