import argparse

from detectors.coordinates import GeoCoordinates, CoordinateException
from detectors.earthquake import EarthquakeDetector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for finding 10 most nearby earthquakes "
                                                 "to the given city (longitude, latitude).")
    parser.add_argument('latitude', type=float, help='Latitude coordinates.')
    parser.add_argument('longitude', type=float, help='Longitude coordinates.')
    args = parser.parse_args()

    try:
        detector = EarthquakeDetector()
        nearest_earthquakes = detector.k_nearest_earthquakes(GeoCoordinates(args.longitude, args.latitude))

        for ne in nearest_earthquakes:
            print(f"{ne.earthquake.place} || {ne.distance_km}")

    except CoordinateException as exc:
        print(exc.message)
