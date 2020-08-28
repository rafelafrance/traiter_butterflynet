"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher

from .dimorphism import DIMORPHISM
from .mimicry import MIMICRY
from ..pylib.util import GROUP_STEP, TERMS, TRAIT_STEP

MATCHERS = (DIMORPHISM, MIMICRY)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        terms = TERMS
        self.add_terms(terms)

        groups = TraitMatcher.step_rules(MATCHERS, GROUP_STEP)
        traits = TraitMatcher.step_rules(MATCHERS, TRAIT_STEP)

        self.add_patterns(groups, GROUP_STEP)
        self.add_patterns(traits, TRAIT_STEP)
