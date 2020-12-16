"""Utilities and constants."""

from pathlib import Path

from traiter.pylib.terms import read_terms, shared_terms

DATA_DIR = Path.cwd() / 'data'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
MERGE_STEP = 'merge'

BUTTERFLY_TERMS = VOCAB_DIR / 'lepidoptera.csv'
TERMS = read_terms(BUTTERFLY_TERMS)
TERMS += shared_terms('units.csv')
TERMS += shared_terms('numerics.csv')

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}

ABBREVS = """
    Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    mm cm m
    Am Anim Bio Biol Bull Bull Conserv DC Ecol Entomol Fig Hist IUCN Inst Int
    Lond Me´m Mol Mus Nat Physiol Rep Sci Soc Syst Zool
    """

CLOSE = [')', ']']
COLON = [':']
COMMA = [',']
CROSS = ['x', '×', '⫻']  # ⫻ = 0x3f
DASH = ['–', '-', '––', '--']
DOT = ['.']
EQ = ['=', '¼']  # ¼ = 0xbc
INT_RE = r'^\d+([\d,]*\d|\d*)*$'
NUMBER_RE = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SEMICOLON = [';']
SLASH = ['/']
BREAK = DOT + SEMICOLON
