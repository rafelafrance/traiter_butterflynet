"""Build the NLP pipeline."""
from traiter.spacy_nlp.pipeline import SpacyPipeline
from traiter.spacy_nlp.sentencizer import SpacySentencizer

from .consts import ABBREVS, TRAIT_STEP
from ..matchers.matcher import Matcher


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP}

    def __init__(self):
        super().__init__()
        self.nlp.max_length *= 2

        self.nlp.disable_pipes(['ner'])

        self.matcher = Matcher(self.nlp)
        sentencizer = SpacySentencizer(ABBREVS)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)


PIPELINE = Pipeline()