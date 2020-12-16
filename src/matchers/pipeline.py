"""Build the NLP pipeline."""

from traiter.pylib.pipeline import SpacyPipeline
from traiter.pylib.sentencizer import SpacySentencizer
from traiter.pylib.to_entities import ToEntities

from .matcher import Matcher
from .merge import merge
from ..pylib.util import ABBREVS, TRAIT_STEP


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    token2entity = {TRAIT_STEP}
    entities2keep = {TRAIT_STEP}

    def __init__(self):
        super().__init__()
        self.nlp.max_length *= 2

        self.nlp.disable_pipes(['ner'])

        self.matcher = Matcher(self.nlp)
        sentencizer = SpacySentencizer(ABBREVS)
        to_entities = ToEntities(self.entities2keep, self.token2entity)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)
        self.nlp.add_pipe(to_entities, last=True)
        self.nlp.add_pipe(merge, last=True)
