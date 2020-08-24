"""Build the NLP pipeline."""
import spacy

from traiter.spacy_nlp import spacy_nlp  # pylint: disable=import-error
from traiter.pipeline import TraitPipeline  # pylint: disable=import-error
from traiter.spacy_nlp import setup_tokenizer  # pylint: disable=import-error

from .segmenter import sentencizer
from ..matchers.matcher import Matcher
from ..pylib.util import TRAIT_STEP

NLP = spacy_nlp(disable=['ner'])
NLP.add_pipe(sentencizer, before='parser')

MATCHER = Matcher(NLP)
NLP.add_pipe(MATCHER, after='parser')


class Pipeline(TraitPipeline):
    """Build a custom traiter pipeline."""

    steps2link = {TRAIT_STEP}

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.max_length *= 2

        super().__init__(self.nlp)

        self.nlp.disable_pipes(['ner'])

        setup_tokenizer(self.nlp)

        self.matcher = Matcher(self.nlp)

        self.nlp.add_pipe(sentencizer, before='parser')
        self.nlp.add_pipe(self.matcher, last=True)


PIPELINE = Pipeline()
