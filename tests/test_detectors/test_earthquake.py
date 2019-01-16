from unittest import TestCase

from detectors.earthquake import Earthquake


class TestEarthquakeObject(TestCase):
    def test_earthquakes_with_same_coords_should_be_equal(self):
        earthquake = Earthquake('test_1', 100, 100, (0.0, 0.0))
        other_earthquake = Earthquake('test_2', 100, 100, (0.0, 0.0))

        self.assertEquals(earthquake, other_earthquake)

    def test_earthquakes_with_same_coords_should_be_equal(self):
        pass

    def test_earthquake_with_smaller_distance_should_be_lesser(self):
        pass

    def test_distance_from_origin(self):
        test_cases = [
            ((0.0, 0.0), 12345),
            ((0.0, 0.0), 12345),
            ((0.0, 0.0), 12345)
        ]

        for coordinates, distance in test_cases:
            with self.subTest(test_tittle=coordinates):
                pass


class TestEarthquakeDetector(TestCase):
    def test_should_return_empty_list_with_negative_k(self):
        pass

    def test_should_return_k_closest_earthquakes(self):
        pass
