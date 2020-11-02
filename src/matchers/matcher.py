"""Base matcher object."""

from traiter.spacy_nlp.matcher import SpacyMatcher

from .consts import GROUP_STEP, TERMS, TRAIT_STEP
from .dimorphism import DIMORPHISM
from .mimicry import MIMICRY

MATCHERS = (DIMORPHISM, MIMICRY)


class Matcher(SpacyMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        self.add_terms(TERMS)
        self.add_patterns(MATCHERS, GROUP_STEP)
        self.add_patterns(MATCHERS, TRAIT_STEP)
