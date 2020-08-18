"""Utilities and constants."""

from pathlib import Path
import regex

NAME = 'lepidoptera'

DATA_DIR = Path('.') / 'data'
VOCAB_DIR = Path('.') / 'src' / 'vocabulary'

XLSX = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.xlsx'
CSV = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.csv'


def clean_text(text):
    """Strip control characters from improperly encoded input strings."""
    text = text if text else ''
    return regex.sub(r'\p{Cc}+', ' ', text)
