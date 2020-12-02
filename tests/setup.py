"""Setup for all tests."""

from typing import Dict, List

from traiter.pylib.to_entities import ToEntities

from src.matchers.pipeline import Pipeline
from src.pylib.util import TRAIT_STEP

TEST_PIPELINE = Pipeline()  # Singleton for testing

TO_ENTITIES = ToEntities(token2entity={TRAIT_STEP})
TEST_PIPELINE.nlp.add_pipe(TO_ENTITIES, last=True)


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST_PIPELINE.test_traits(text)
