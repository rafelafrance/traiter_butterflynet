"""Test mimicry trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from src.pylib.pipeline import parse


class TestMimicry(unittest.TestCase):
    """Test range trait matcher."""

    def test_mimicry_01(self):
        self.assertEqual(
            parse(shorten("""
                acraeines are mimicked by a number of other Lepidoptera""")),
            [{'mimicry': 'are mimicked by a number of other lepidoptera',
              'trait': 'mimicry', 'start': 10, 'end': 55}]
        )

    def test_mimicry_02(self):
        self.assertEqual(
            parse(shorten("""
                interspecific Mullerian mimicry complexes within their
                own genera""")),
            [{'mimicry': 'interspecific mullerian mimicry',
              'trait': 'mimicry', 'start': 0, 'end': 31}]
        )

    def test_mimicry_03(self):
        self.assertEqual(
            parse(shorten("""Telchinia jodutta is probably a co-mimic.""")),
            [{'mimicry': 'co-mimic',
              'trait': 'mimicry', 'start': 32, 'end': 40}]
        )

    def test_mimicry_04(self):
        self.assertEqual(
            parse(shorten("""
                appears to be a mimic of the Chief butterflies""")),
            [{'mimicry': 'be a mimic of the chief butterflies',
              'trait': 'mimicry', 'start': 11, 'end': 46}]
        )

    def test_mimicry_05(self):
        self.assertEqual(
            parse(shorten("""Someren it is a mimic of a day-flying moth""")),
            [{'mimicry': 'is a mimic of a day-flying moth',
              'trait': 'mimicry', 'start': 11, 'end': 42}]
        )

    def test_mimicry_06(self):
        self.assertEqual(
            parse(shorten("""Mimicked by a very rare form of""")),
            [{'mimicry': 'mimicked by',
              'trait': 'mimicry', 'start': 0, 'end': 11}]
        )

    def test_mimicry_07(self):
        self.assertEqual(
            parse(shorten("""suggest that females mimic Amauris ochlea.""")),
            [{'mimicry': 'females mimic',
              'trait': 'mimicry', 'start': 13, 'end': 26}]
        )

    def test_mimicry_08(self):
        self.assertEqual(
            parse(shorten("""
                acraeines are involved in Mullerian and Batesian mimicry
                complexes""")),
            [{'mimicry': 'mullerian and batesian mimicry',
              'trait': 'mimicry', 'start': 26, 'end': 56}]
        )
