"""Base matcher object."""

from traiter.trait_matcher import TraitMatcher  # pylint: disable=import-error

from ..pylib.terms import TERMS

MATCHERS = ()


class Matcher(TraitMatcher):
    """Base matcher object."""

    def __init__(self, nlp, attach=True, as_entities=True):
        super().__init__(nlp, as_entities=as_entities)

        terms = TERMS
        self.add_terms(terms)

        traiters = []
        groupers = []

        for matcher in MATCHERS:
            traiters += matcher.get('traits', [])
            groupers += matcher.get('groupers', [])

        self.add_patterns(groupers, 'groups')
        self.add_patterns(traiters, 'traits')
