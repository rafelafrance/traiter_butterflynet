"""Test dimorphism trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from src.matchers.pipeline import PIPELINE

NLP = PIPELINE.test_traits


class TestDimorphism(unittest.TestCase):
    """Test range trait matcher."""

    def test_dimorphism_01(self):
        self.assertEqual(
            NLP('is sexually dimorphic and seasonally variable'),
            [{'dimorphism': 'sexually dimorphic',
              'trait': 'dimorphism', 'start': 3, 'end': 21}]
        )

    def test_dimorphism_02(self):
        self.assertEqual(
            NLP('Sexual dimorphism not prominent.'),
            [{'dimorphism': 'sexual dimorphism not prominent',
              'trait': 'dimorphism', 'start': 0, 'end': 31}]
        )

    def test_dimorphism_03(self):
        self.assertEqual(
            NLP('sexual dimorphism is often pronounced'),
            [{'dimorphism': 'sexual dimorphism is often pronounced',
              'trait': 'dimorphism', 'start': 0, 'end': 37}]
        )

    def test_dimorphism_04(self):
        self.assertEqual(
            NLP('Marked sexual dimorphism occurs in some genera'),
            [{'dimorphism': 'marked sexual dimorphism',
              'trait': 'dimorphism', 'start': 0, 'end': 24}]
        )

    def test_dimorphism_05(self):
        self.assertEqual(
            NLP('Acraea adults exhibit little sexual dimorphism.'),
            [{'dimorphism': 'little sexual dimorphism',
              'trait': 'dimorphism', 'start': 22, 'end': 46}]
        )

    def test_dimorphism_06(self):
        self.assertEqual(
            NLP(', not dimorphic,'),
            [{'dimorphism': 'not dimorphic',
              'trait': 'dimorphism', 'start': 2, 'end': 15}]
        )

    def test_dimorphism_07(self):
        self.assertEqual(
            NLP(', not sexual dimorphism)'),
            [{'dimorphism': 'not sexual dimorphism',
              'trait': 'dimorphism', 'start': 2, 'end': 23}]
        )

    def test_dimorphism_08(self):
        self.assertEqual(
            NLP(shorten("""
                Sexual dimorphism: There is no special sexual dimorphism
                in the species""")),
            [{'dimorphism': 'no special sexual dimorphism',
              'trait': 'dimorphism', 'start': 28, 'end': 56}]
        )

    def test_dimorphism_09(self):
        self.assertEqual(
            NLP('Sexual dimorphism is not pronounced'),
            [{'dimorphism': 'sexual dimorphism is not pronounced',
              'trait': 'dimorphism', 'start': 0, 'end': 35}]
        )

    def test_dimorphism_10(self):
        self.assertEqual(
            NLP('Sexual dimorphism present.'),
            [{'dimorphism': 'sexual dimorphism present',
              'trait': 'dimorphism', 'start': 0, 'end': 25}]
        )

    def test_dimorphism_11(self):
        self.assertEqual(
            NLP('There is no conspicuous sexual dimorphism,'),
            [{'dimorphism': 'no conspicuous sexual dimorphism',
              'trait': 'dimorphism', 'start': 9, 'end': 41}]
        )

    def test_dimorphism_12(self):
        self.assertEqual(
            NLP(shorten("""
                Sexual dimorphism: Upper side of male with brown colour
                bright reddish-orange, and some  black markings; in the female
                 llie ground colour is duller and the black markings 
                 more numerous.
                """)),
            [{'dimorphism': 'sexual dimorphism',
              'trait': 'dimorphism', 'start': 0, 'end': 117}]
        )

    def test_dimorphism_13(self):
        self.assertEqual(
            NLP(shorten("""Algiachroa adults are slightly dimorphic,""")),
            [{'dimorphism': 'slightly dimorphic',
              'trait': 'dimorphism', 'start': 22, 'end': 40}]
        )

    def test_dimorphism_14(self):
        self.assertEqual(
            NLP(shorten("""
                Leto Fritillaries are strongly sexually dimorphic""")),
            [{'dimorphism': 'strongly sexually dimorphic',
              'trait': 'dimorphism', 'start': 22, 'end': 49}]
        )

    def test_dimorphism_15(self):
        self.assertEqual(
            NLP(shorten("""
                The Arhopala male lacks sex-brands, but species are usually
                fairly sexually dimorphic.""")),
            [{'dimorphism': 'fairly sexually dimorphic',
              'trait': 'dimorphism', 'start': 60, 'end': 85}]
        )

    def test_dimorphism_16(self):
        self.assertEqual(
            NLP(shorten("""Sexual dimorphism weakly recognizable.""")),
            [{'dimorphism': 'sexual dimorphism weakly recognizable',
              'trait': 'dimorphism', 'start': 0, 'end': 37}]
        )

    def test_dimorphism_17(self):
        self.assertEqual(
            NLP(shorten("""Sexual dimorphism absent.""")),
            [{'dimorphism': 'sexual dimorphism absent',
              'trait': 'dimorphism', 'start': 0, 'end': 24}]
        )

    def test_dimorphism_18(self):
        self.assertEqual(
            NLP(shorten("""Sexual dimorphism: Not observed.""")),
            [{'dimorphism': 'sexual dimorphism: not observed',
              'trait': 'dimorphism', 'start': 0, 'end': 31}]
        )

    def test_dimorphism_19(self):
        self.assertEqual(
            NLP(shorten("""
                Secondly, it exhibits a striking sexual dimorphism,""")),
            [{'dimorphism': 'a striking sexual dimorphism',
              'trait': 'dimorphism', 'start': 22, 'end': 50}]
        )

    def test_dimorphism_20(self):
        self.assertEqual(
            NLP(shorten("""
                Sexual dimorphism: There is no special sexual dimorphism,""")),
            [{'dimorphism': 'no special sexual dimorphism',
              'trait': 'dimorphism', 'start': 28, 'end': 56}]
        )

    def test_dimorphism_21(self):
        self.assertEqual(
            NLP(shorten("""Sexual dimorphism: Almost none;""")),
            [{'dimorphism': 'sexual dimorphism: almost none',
              'trait': 'dimorphism', 'start': 0, 'end': 30}]
        )

    def test_dimorphism_22(self):
        self.assertEqual(
            NLP(shorten("""
                but species are usually fairly sexually dimorphic.""")),
            [{'dimorphism': 'fairly sexually dimorphic',
              'trait': 'dimorphism', 'start': 24, 'end': 49}]
        )

    def test_dimorphism_23(self):
        self.assertEqual(
            NLP(shorten("""
                Sexual dimorphism weakly recognizable.""")),
            [{'dimorphism': 'sexual dimorphism weakly recognizable',
              'trait': 'dimorphism', 'start': 0, 'end': 37}]
        )

    def test_dimorphism_24(self):
        self.assertEqual(
            NLP(shorten("""
                There is no sexual dimorphism,""")),
            [{'dimorphism': 'no sexual dimorphism',
              'trait': 'dimorphism', 'start': 9, 'end': 29}]
        )

    def test_dimorphism_25(self):
        self.assertEqual(
            NLP(shorten("""
                The sexes are strongly dimorphic,""")),
            [{'dimorphism': 'sexes are strongly dimorphic',
              'trait': 'dimorphism', 'start': 4, 'end': 32}]
        )

    def test_dimorphism_26(self):
        self.assertEqual(
            NLP(shorten("""
                Both sexes vary considerably in size.""")),
            [{'dimorphism': 'sexes vary considerably',
              'trait': 'dimorphism', 'start': 5, 'end': 28}]
        )

    def test_dimorphism_27(self):
        self.assertEqual(
            NLP(shorten("""hind wing and sexes are similar""")),
            [{'dimorphism': 'sexes are similar',
              'trait': 'dimorphism', 'start': 14, 'end': 31}]
        )

    def test_dimorphism_28(self):
        self.assertEqual(
            NLP(shorten("""The abdomen in both sexes is orange""")),
            []
        )

    def test_dimorphism_29(self):
        self.assertEqual(
            NLP(shorten("""hind wing and sexes are different""")),
            [{'dimorphism': 'sexes are different',
              'trait': 'dimorphism', 'start': 14, 'end': 33}]
        )

    def test_dimorphism_30(self):
        self.assertEqual(
            NLP(shorten("""Sexes: dissimilar;""")),
            [{'dimorphism': 'sexes: dissimilar',
              'trait': 'dimorphism', 'start': 0, 'end': 17}]
        )

    def test_dimorphism_31(self):
        self.assertEqual(
            NLP(shorten("""The sexes are very similar,""")),
            [{'dimorphism': 'sexes are very similar',
              'trait': 'dimorphism', 'start': 4, 'end': 26}]
        )

    def test_dimorphism_32(self):
        self.assertEqual(
            NLP(shorten("""female resembles the male""")),
            [{'dimorphism': 'female resembles the male',
              'trait': 'dimorphism', 'start': 0, 'end': 25}]
        )

    def test_dimorphism_33(self):
        self.assertEqual(
            NLP(shorten("""The females are similar to the males.""")),
            [{'dimorphism': 'females are similar to the males',
              'trait': 'dimorphism', 'start': 4, 'end': 36}]
        )

    def test_dimorphism_34(self):
        self.assertEqual(
            NLP(shorten("""The female is much larger than the male.""")),
            [{'dimorphism': 'female is much larger than the male',
              'trait': 'dimorphism', 'start': 4, 'end': 39}]
        )

    def test_dimorphism_35(self):
        self.assertEqual(
            NLP(shorten("""Both sexes fly high in the canopy""")),
            []
        )

    def test_dimorphism_36(self):
        self.assertEqual(
            NLP(shorten("""While seasonal dimorphism as such""")),
            []
        )
