"""Test elevation trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from traiter.pylib.util import shorten

from tests.setup import test_traits


class TestElevation(unittest.TestCase):
    """Test elevation trait matcher."""

    def test_elevation_01(self):
        self.assertEqual(
            test_traits('0- 1,200 m'),
            [{'elev_low': 0, 'elev_high': 1200, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 10}]
        )

    def test_elevation_02(self):
        self.assertEqual(
            test_traits('0-1900 m in Alps and up to 2500 m in Greece'),
            [{'elev_low': 0, 'elev_high': 2500, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 33}]
        )

    def test_elevation_03(self):
        self.assertEqual(
            test_traits('from sea level to one or two thousand feet.'),
            [{'elev_low': 0, 'elev_high': 2000, 'elevation_units': 'ft',
              'trait': 'elevation', 'start': 5, 'end': 42}]
        )

    def test_elevation_04(self):
        self.assertEqual(
            test_traits('0- 200 m (and probably somewhat higher).'),
            [{'elev_low': 0, 'elev_high': 200,
                'elevation_units': 'm', 'elevation_approx': True,
              'trait': 'elevation', 'start': 0, 'end': 38}]
        )

    def test_elevation_05(self):
        self.assertEqual(
            test_traits('Zambezi Source, 5000 ft'),
            [{'elev_high': 5000, 'elevation_units': 'ft',
              'trait': 'elevation', 'start': 16, 'end': 23}]
        )

    def test_elevation_06(self):
        self.assertEqual(
            test_traits('sea level to 3000 ft'),
            [{'elev_low': 0, 'elev_high': 3000, 'elevation_units': 'ft',
              'trait': 'elevation', 'start': 0, 'end': 20}]
        )

    def test_elevation_07(self):
        self.assertEqual(
            test_traits("""11°15S'; 24°18E'. 1500 m"""),
            [{'elev_high': 1500, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 18, 'end': 24}]
        )

    def test_elevation_08(self):
        self.assertEqual(
            test_traits(shorten("""
                Mufulira, Zambia. 4100 ft. [male]; Zambia, Copperbelt Prov., 
                South Mutunda River nr Mufulira. 1250 m [female]""")),
            [{'elev_high': 1250, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 18, 'end': 100}]
        )

    def test_elevation_09(self):
        self.assertEqual(
            test_traits('up to 500 m'),
            [{'elev_low': 0, 'elev_high': 500, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 11}]
        )

    def test_elevation_10(self):
        self.assertEqual(
            test_traits('Saut d’Eau,183 m;'),
            [{'elev_high': 183, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 11, 'end': 16}]
        )

    def test_elevation_11(self):
        self.assertEqual(
            test_traits('below about 1,000 m'),
            [{'elev_low': 0, 'elev_high': 1000, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 19}]
        )

    def test_elevation_12(self):
        self.assertEqual(
            test_traits('from near sea level to about 950 m'),
            [{'elev_low': 0, 'elev_high': 950, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 10, 'end': 34}]
        )

    def test_elevation_13(self):
        self.assertEqual(
            test_traits('up to 2000 m in Europe and up to 2500 m in Turkey'),
            [{'elev_low': 0, 'elev_high': 2500, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 39}]
        )

    def test_elevation_14(self):
        self.assertEqual(
            test_traits('< 1800 m'),
            [{'elev_low': 0, 'elev_high': 1800, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 8}]
        )

    def test_elevation_15(self):
        self.assertEqual(
            test_traits('>1500m'),
            [{'elev_low': 1500, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 6}]
        )

    def test_elevation_16(self):
        self.assertEqual(
            test_traits('above 700 m asl... Below 150 m asl...'),
            [{'elev_low': 0, 'elev_high': 700, 'elevation_units': 'm',
              'trait': 'elevation', 'start': 0, 'end': 30}]
        )
