from math import sqrt, radians, sin, cos, atan2
from typing import Tuple

import requests

from detectors.collections.sorted import HeapSet

EARTH_RADIUS = 6371.0
USGS_URI = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"


class Earthquake:
    __slots__ = ['place', 'longitude', 'latitude', 'distance']

    def __init__(self, place: str, longitude: float, latitude: float, origin: Tuple[float, float]):
        self.place = place
        self.longitude = longitude
        self.latitude = latitude
        self.distance = self._distance_from_origin(origin)

    def __eq__(self, other: 'Earthquake') -> bool:
        return self.longitude == other.longitude and self.latitude == other.latitude

    def __lt__(self, other: 'Earthquake') -> bool:
        return self.distance < other.distance

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))

    def _distance_from_origin(self, origin: Tuple[float, float]) -> int:
        lat1 = radians(origin[0])
        lat2 = radians(self.latitude)
        delta_lon = radians(self.longitude) - radians(origin[1])
        delta_lat = lat2 - lat1
        a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return int(EARTH_RADIUS * c)


class EarthquakeDetector:
    @staticmethod
    def find_k_nearest(geo_coordinates: Tuple[float, float], k: int = 10):
        request = requests.get(USGS_URI)
        features = request.json()['features']
        earthquakes = HeapSet()

        for feature in features:
            earthquakes.add(Earthquake(place=feature['properties']['title'],
                                       longitude=feature['geometry']['coordinates'][0],
                                       latitude=feature['geometry']['coordinates'][1],
                                       origin=geo_coordinates))

        return earthquakes.as_ordered_list()[:k] if k > 0 else []
