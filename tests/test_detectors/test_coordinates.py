from unittest import TestCase

from detectors.coordinates import GeoCoordinates, CoordinateException


class TestGeoCoordinates(TestCase):
    def test_should_be_equal_with_identical_coordinates(self):
        coordinate = GeoCoordinates(1.0, 1.0)
        other_coordinate = GeoCoordinates(1.0, 1.0)

        self.assertEqual(coordinate, other_coordinate)

    def test_incorrect_coordinates_should_raise_exception(self):
        coords_test_cases = [
            (1.0, -95.0),
            (199.0, -25.0),
            (234.0, 567.0),
            (0.1231, -104.1)
        ]
        for coords in coords_test_cases:
            with self.subTest(name='a'), self.assertRaises(CoordinateException):
                GeoCoordinates(*coords)
