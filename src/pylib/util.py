"""Utilities and constants."""

from pathlib import Path

from traiter.pylib.terms import drop, read_terms, shared_terms

DATA_DIR = Path.cwd() / 'data'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'
OUTPUT_DIR = Path.cwd() / 'output'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
MERGE_STEP = 'merge'

TERMS = read_terms(VOCAB_DIR / 'lepidoptera.csv')
TERMS += shared_terms('numerics.csv')
TERMS += shared_terms('units.csv')
TERMS += shared_terms('time.csv')
TERMS += shared_terms('animals.csv')

# Inches abbreviation "in" interferes with the preposition "in"
TERMS = drop(TERMS, 'in', field='pattern')

REPLACE = {t['pattern']: r for t in TERMS if (r := t.get('replace'))}
EXTREME = {t['pattern']: e for t in TERMS if (e := t.get('extreme'))}
APPROX = {t['pattern']: a for t in TERMS if (a := t.get('approx'))}
IMPLIED = {t['pattern']: i for t in TERMS if (i := t.get('implied'))}

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
FEET_QUOTE = ["'"]
INT_RE = r'^\d+([\d,]*\d|\d*)*$'
NUMBER_RE = r'^\d+(\.\d*)?$'
OPEN = ['(', '[']
PLUS = ['+']
QUOTE = ['"', "'"]
SEMICOLON = [';']
SLASH = ['/']
BREAK = DOT + SEMICOLON
