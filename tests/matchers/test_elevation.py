"""Test elevation trait matcher."""

# pylint: disable=missing-function-docstring, too-many-public-methods

import unittest

from tests.setup import test


class TestElevation(unittest.TestCase):
    """Test elevation trait matcher."""

    def test_elevation_01(self):
        self.assertEqual(
            test('0- 1,200 m'),
            [{'elev_low': 0, 'elev_high': 1200, 'elev_units': 'm',
              'elev_ori_low': 0, 'elev_ori_high': 1200,
              'trait': 'elevation', 'start': 0, 'end': 10}]
        )

    def test_elevation_02(self):
        self.assertEqual(
            test('0-1900 m in Alps and up to 2500 m in Greece'),
            [{'elev_low': 0, 'elev_high': 2500, 'elev_units': 'm',
              'elev_ori_low': 0, 'elev_ori_high': 2500,
              'trait': 'elevation', 'start': 0, 'end': 33}]
        )

    def test_elevation_03(self):
        self.assertEqual(
            test('from sea level to one or two thousand feet.'),
            [{'elev_low': 0, 'elev_high': 610, 'elev_units': 'ft',
              'elev_ori_low': 0, 'elev_ori_high': 2000,
              'trait': 'elevation', 'start': 5, 'end': 42}]
        )

    def test_elevation_04(self):
        self.assertEqual(
            test('0- 200 m (and probably somewhat higher).'),
            [{'elev_low': 0, 'elev_high': 200, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_low': 0, 'elev_ori_high': 200,
              'trait': 'elevation', 'start': 0, 'end': 38}]
        )

    def test_elevation_05(self):
        self.assertEqual(
            test('Zambezi Source, 5000 ft'),
            [{'elev_high': 1524, 'elev_units': 'ft',
              'elev_ori_high': 5000,
              'trait': 'elevation', 'start': 16, 'end': 23}]
        )

    def test_elevation_06(self):
        self.assertEqual(
            test('sea level to 3000 ft'),
            [{'elev_low': 0, 'elev_high': 914, 'elev_units': 'ft',
              'elev_ori_low': 0, 'elev_ori_high': 3000,
              'trait': 'elevation', 'start': 0, 'end': 20}]
        )

    def test_elevation_07(self):
        self.assertEqual(
            test("""11°15S'; 24°18E'. 1500 m"""),
            [{'elev_high': 1500, 'elev_units': 'm',
              'elev_ori_high': 1500,
              'trait': 'elevation', 'start': 18, 'end': 24}]
        )

    def test_elevation_08(self):
        self.assertEqual(
            test("""
                Mufulira, Zambia. 4100 ft. [male]; Zambia, Copperbelt Prov., 
                South Mutunda River nr Mufulira. 1250 m [female]"""),
            [{'elev_high': 1250, 'elev_units': 'm',
              'elev_ori_high': 4100,
              'trait': 'elevation', 'start': 18, 'end': 100}]
        )

    def test_elevation_09(self):
        self.assertEqual(
            test('up to 500 m'),
            [{'elev_low': 0, 'elev_high': 500, 'elev_units': 'm',
              'elev_ori_low': 0, 'elev_ori_high': 500,
              'trait': 'elevation', 'start': 0, 'end': 11}]
        )

    def test_elevation_10(self):
        self.assertEqual(
            test('Saut d’Eau,183 m;'),
            [{'elev_high': 183, 'elev_units': 'm',
              'elev_ori_high': 183,
              'trait': 'elevation', 'start': 11, 'end': 16}]
        )

    def test_elevation_11(self):
        self.assertEqual(
            test('below about 1,000 m'),
            [{'elev_low': 0, 'elev_high': 1000, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_low': 0, 'elev_ori_high': 1000,
              'trait': 'elevation', 'start': 0, 'end': 19}]
        )

    def test_elevation_12(self):
        self.assertEqual(
            test('from near sea level to about 950 m'),
            [{'elev_low': 0, 'elev_high': 950, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_low': 0, 'elev_ori_high': 950,
              'trait': 'elevation', 'start': 10, 'end': 34}]
        )

    def test_elevation_13(self):
        self.assertEqual(
            test('up to 2000 m in Europe and up to 2500 m in Turkey'),
            [{'elev_low': 0, 'elev_high': 2500, 'elev_units': 'm',
              'elev_ori_low': 0, 'elev_ori_high': 2500,
              'trait': 'elevation', 'start': 0, 'end': 39}]
        )

    def test_elevation_14(self):
        self.assertEqual(
            test('< 1800 m'),
            [{'elev_low': 0, 'elev_high': 1800, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_low': 0, 'elev_ori_high': 1800,
              'trait': 'elevation', 'start': 0, 'end': 8}]
        )

    def test_elevation_15(self):
        self.assertEqual(
            test('>1500m'),
            [{'elev_low': 1500, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_low': 1500,
              'trait': 'elevation', 'start': 0, 'end': 6}]
        )

    def test_elevation_16(self):
        self.assertEqual(
            test('above 700 m asl... Below 150 m asl...'),
            [{'elev_low': 150, 'elev_high': 700, 'elev_units': 'm',
              'elev_ori_low': 150, 'elev_ori_high': 700,
              'trait': 'elevation', 'start': 0, 'end': 30}]
        )

    def test_elevation_17(self):
        self.assertEqual(
            test('~1,500 m'),
            [{'elev_high': 1500, 'elev_units': 'm', 'elev_approx': True,
              'elev_ori_high': 1500,
              'trait': 'elevation', 'start': 0, 'end': 8}]
        )

    def test_elevation_18(self):
        self.assertEqual(
            test('1400-2000 in Poland and up to 2500 m in Slovakia'),
            [{'elev_low': 1400, 'elev_high': 2500, 'elev_units': 'm',
              'elev_ori_low': 1400, 'elev_ori_high': 2500,
              'trait': 'elevation', 'start': 0, 'end': 36}]
        )

    def test_elevation_19(self):
        self.assertEqual(
            test('2-3000ft,'),
            [{'elev_low': 610, 'elev_high': 914, 'elev_units': 'ft',
              'elev_ori_low': 2000, 'elev_ori_high': 3000,
              'trait': 'elevation', 'start': 0, 'end': 8}]
        )

    def test_elevation_20(self):
        self.assertEqual(
            test("""
                altitudes vary in different parts of the range from 2,500 m 
                (the Zeravshansky Mts.) to 5,200 m a.s.l. (the SE. Pamirs)"""),
            [{'elev_low': 2500, 'elev_high': 5200, 'elev_units': 'm',
              'elev_ori_low': 2500, 'elev_ori_high': 5200,
              'trait': 'elevation', 'start': 47, 'end': 94}]
        )

    def test_elevation_21(self):
        self.assertEqual(
            test('as high as 1200 m'),
            [{'elev_low': 0, 'elev_high': 1200, 'elev_units': 'm',
              'elev_ori_low': 0, 'elev_ori_high': 1200,
              'trait': 'elevation', 'start': 0, 'end': 17}]
        )

    def test_elevation_22(self):
        self.assertEqual(
            test('perching from 4-7m'),
            []
        )

    def test_elevation_23(self):
        self.assertEqual(
            test('not below 8000 feet'),
            [{'elev_low': 2438, 'elev_units': 'ft',
              'elev_ori_low': 8000,
              'trait': 'elevation', 'start': 0, 'end': 19}]
        )

    def test_elevation_24(self):
        self.assertEqual(
            test('4°04’34,5’’N - 17°07’27,7’’E ; 538 m'),
            [{'elev_high': 538, 'elev_units': 'm', 'elev_ori_high': 538,
              'trait': 'elevation', 'start': 31, 'end': 36}]
        )
