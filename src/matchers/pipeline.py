"""Build the NLP pipeline."""

from traiter.matchers.rule import Rule
from traiter.matchers.term import Term
from traiter.pipeline import SpacyPipeline
from traiter.sentencizer import Sentencizer
from traiter.to_entities import ToEntities

from .dimorphism import DIMORPHISM
from .elevation import ELEVATION
from .merge import merge
from .mimicry import MIMICRY
from ..pylib.consts import ABBREVS, GROUP_STEP, TERMS, TRAIT_STEP

MATCHERS = [DIMORPHISM, MIMICRY, ELEVATION]
# MATCHERS = [ELEVATION]


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    def __init__(self):
        super().__init__()
        self.nlp.max_length *= 2

        self.nlp.disable_pipes(['ner'])

        token2entity = {TRAIT_STEP}
        entities2keep = {TRAIT_STEP}

        Sentencizer.add_pipe(self.nlp, ABBREVS, before='parser')
        Term.add_pipes(self.nlp, TERMS, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, GROUP_STEP, before='parser')
        Rule.add_pipe(self.nlp, MATCHERS, TRAIT_STEP, before='parser')
        ToEntities.add_pipe(self.nlp, entities2keep, token2entity)
        self.nlp.add_pipe(merge, last=True)
