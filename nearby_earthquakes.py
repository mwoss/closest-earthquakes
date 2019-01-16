import argparse

from detectors.earthquake import EarthquakeDetector


def geo_coordinates(coordinate: str):
    coordinate = float(coordinate)
    if -180.0 > coordinate or coordinate > 180.0:
        raise argparse.ArgumentTypeError(f"Coordinate: {coordinate} is not in range [-180, 180]")
    return coordinate


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for finding 10 most nearby earthquakes "
                                                 "to the given city (longitude, latitude).")
    parser.add_argument('longitude', type=geo_coordinates, help='Longitude coordinates.')
    parser.add_argument('latitude', type=geo_coordinates, help='Latitude coordinates.')
    args = parser.parse_args()

    try:
        detector = EarthquakeDetector()
        nearest_earthquakes = detector.find_k_nearest_from((args.longitude, args.latitude))

        for earthquake in nearest_earthquakes:
            print(f"{earthquake.place} || {earthquake.distance}")
    except TypeError as exc:
        print(f"Object used in UniqueSortedList is not hashable\n{exc}")
