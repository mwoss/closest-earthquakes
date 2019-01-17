from unittest import TestCase
from unittest.mock import Mock, patch

from detectors.coordinates import GeoCoordinates
from detectors.earthquake import Earthquake, EarthquakeWithDistance, EarthquakeDetector


class TestEarthquakeObject(TestCase):
    @patch("detectors.earthquake.EarthquakeWithDistance._distance_from", Mock())
    def test_earthquakes_with_same_coords_should_be_equal(self):
        earthquake = EarthquakeWithDistance(Earthquake('test1', GeoCoordinates(10.0, 10.0)), Mock())
        other_earthquake = EarthquakeWithDistance(Earthquake('test2', GeoCoordinates(10.0, 10.0)), Mock())

        self.assertEqual(earthquake, other_earthquake)

    def test_earthquake_with_smaller_distance_should_be_lesser(self):
        target = GeoCoordinates(0.0, 0.0)
        earthquake = EarthquakeWithDistance(Earthquake('test1', GeoCoordinates(5.0, 5.0)),
                                            target)
        other_earthquake = EarthquakeWithDistance(Earthquake('test2', GeoCoordinates(10.0, 10.0)), target)

        self.assertLess(earthquake, other_earthquake)

    def test_distance_from_target(self):
        target = (0.0, 0.0)
        test_cases = [
            ((10.0, 10.0), 1569),
            ((-50.0, -88.0), 9865),
            ((12.3, 34.5), 4044)
        ]

        for coordinates, expected_distance in test_cases:
            with self.subTest(test_tittle=coordinates):
                earthquake = EarthquakeWithDistance(Earthquake('test', GeoCoordinates(*coordinates)),
                                                    GeoCoordinates(*target))
                self.assertEqual(earthquake.distance_km, expected_distance)


class TestEarthquakeDetector(TestCase):
    @patch("detectors.earthquake.get_request", Mock())
    def test_should_raise_exception_with_negative_k(self):
        detector = EarthquakeDetector()

        with self.assertRaises(ValueError):
            detector.k_nearest_earthquakes(Mock(), -10)

    @patch("detectors.earthquake.get_request")
    def test_should_return_closest_earthquakes(self, mock_request):
        detector = EarthquakeDetector()
        target_place = GeoCoordinates(0.0, 0.0)
        json_mock = mock_request.return_value.json
        json_mock.return_value = {'features': [{'properties': {'title': 'title1'},
                                                'geometry': {'coordinates': [10.0, 10.0]}},
                                               {'properties': {'title': 'title2'},
                                                'geometry': {'coordinates': [20.0, 20.0]}}]}

        result = detector.k_nearest_earthquakes(target_place, 5)

        expected_result = [EarthquakeWithDistance(Earthquake('title1', GeoCoordinates(10.0, 10.0)), target_place),
                           EarthquakeWithDistance(Earthquake('title1', GeoCoordinates(20.0, 20.0)), target_place)]
        self.assertListEqual(result, expected_result)
