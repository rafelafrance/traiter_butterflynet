"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher

from .dimorphism import DIMORPHISM
from .mimicry import MIMICRY
from ..pylib.terms import TERMS
from ..pylib.util import GROUP_STEP, TRAIT_STEP

MATCHERS = (DIMORPHISM, MIMICRY)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        terms = TERMS
        self.add_terms(terms)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get(TRAIT_STEP, [])
            groupers += matcher.get(GROUP_STEP, [])

        self.add_patterns(groupers, GROUP_STEP)
        self.add_patterns(traiters, TRAIT_STEP)
