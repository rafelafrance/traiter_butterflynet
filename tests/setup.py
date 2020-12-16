"""Setup for all tests."""

from typing import Dict, List

from src.matchers.pipeline import Pipeline

TEST_PIPELINE = Pipeline()  # Singleton for testing


def test_traits(text: str) -> List[Dict]:
    """Find entities in the doc."""
    return TEST_PIPELINE.test_traits(text)
