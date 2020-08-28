"""Utilities and constants."""

from pathlib import Path

from traiter.pylib.terms import read_terms

DATA_DIR = Path.cwd() / 'data'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

XLSX = DATA_DIR / 'BNet_Traits_MothsRemoved_NamesNormalized_DL_2020.06.12.xlsx'
CSV = DATA_DIR / 'BNet_Traits_2020-08-19a.csv'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
BUTTERFLY_TERMS = VOCAB_DIR / 'lepidoptera.csv'
TERMS = read_terms(BUTTERFLY_TERMS)
REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

ABBREVS = """
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    mm cm m
    Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Hist IUCN Inst Int
    Lond Me´m Mol Mus Nat Physiol Rep Sci Soc Syst Zool
    """
