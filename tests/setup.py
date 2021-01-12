"""Setup for all tests."""

from typing import Dict, List

from traiter.util import shorten

from src.matchers.pipeline import Pipeline

TEST_PIPELINE = Pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    """Find entities in the doc."""
    text = shorten(text)
    return TEST_PIPELINE.test_traits(text)
