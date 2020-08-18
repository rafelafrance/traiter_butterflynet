"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from .dimorphism import DIMORPHISM
from ..pylib.terms import TERMS

MATCHERS = (DIMORPHISM,)


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp):
        super().__init__(nlp)

        terms = TERMS
        self.add_terms(terms)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('traits', [])
            groupers += matcher.get('groups', [])

        self.add_patterns(groupers, 'groups')
        self.add_patterns(traiters, 'traits')
