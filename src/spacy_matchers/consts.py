"""Define spacy related constants."""

from traiter.spacy_nlp.terms import read_terms

from src.pylib.util import VOCAB_DIR

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
