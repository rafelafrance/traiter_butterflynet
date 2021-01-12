"""Utilities and constants."""

from pathlib import Path

from traiter.terms.csv_ import Csv

DATA_DIR = Path.cwd() / 'data'
VOCAB_DIR = Path.cwd() / 'src' / 'vocabulary'
OUTPUT_DIR = Path.cwd() / 'output'

GROUP_STEP = 'group'
TRAIT_STEP = 'traits'
MERGE_STEP = 'merge'

TERMS = Csv.shared('numerics units time animals')
TERMS += Csv.read_csv(VOCAB_DIR / 'lepidoptera.csv')
TERMS.drop('in', field='pattern')

REPLACE = TERMS.pattern_dicts('replace')
EXTREME = TERMS.pattern_dicts('extreme')
APPROX = TERMS.pattern_dicts('approx')
IMPLIED = TERMS.pattern_dicts('implied')

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
