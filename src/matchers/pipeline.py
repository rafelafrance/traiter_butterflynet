"""Build the NLP pipeline."""
from traiter.pylib.pipeline import SpacyPipeline
from traiter.pylib.sentencizer import SpacySentencizer

from ..pylib.util import ABBREVS
from ..matchers.matcher import Matcher


class Pipeline(SpacyPipeline):
    """Build a custom traiter pipeline."""

    def __init__(self):
        super().__init__()
        self.nlp.max_length *= 2

        self.nlp.disable_pipes(['ner'])

        self.matcher = Matcher(self.nlp)
        sentencizer = SpacySentencizer(ABBREVS)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)
