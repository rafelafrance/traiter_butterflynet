"""Test elevation trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

# from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestElevation(unittest.TestCase):
    """Test elevation trait matcher."""

    def test_elevation_01(self):
        self.assertEqual(
            test_traits('0- 1,200 m'),
            [{'elevation_low': 0, 'elevation_high': 1200,
              'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 10}]
        )

    def test_elevation_02(self):
        self.assertEqual(
            test_traits('0-1900 m in Alps and up to 2500 m in Greece'),
            [{'elevation_low': 0, 'elevation_high': 1900, 'elevation_max': 2500,
              'elevation_units': 'm', 'trait': 'elevation', 'start': 0, 'end': 33}]
        )

    def test_elevation_03(self):
        self.assertEqual(
            test_traits('from sea level to one or two thousand feet.'),
            [{'elevation_low': 0, 'elevation_high': 1000, 'elevation_max': 2000,
                'elevation_units': 'ft', 'imperial_length': True,
              'trait': 'elevation', 'start': 5, 'end': 42}]
        )

    def test_elevation_04(self):
        self.assertEqual(
            test_traits('0- 200 m (and probably somewhat higher).'),
            [{'elevation_low': 0, 'elevation_high': 200,
                'elevation_units': 'm', 'elevation_high_approx': True,
              'trait': 'elevation', 'start': 0, 'end': 38}]
        )
