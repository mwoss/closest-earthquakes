from math import sqrt, radians, sin, cos, atan2
from typing import Tuple

import requests

from utils.collections import UniqueSortedList
from utils.constants import EARTH_RADIUS, USGS_URI


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
        earthquakes = UniqueSortedList()

        for feature in features:
            earthquakes.add(Earthquake(place=feature['properties']['title'],
                                       longitude=feature['geometry']['coordinates'][0],
                                       latitude=feature['geometry']['coordinates'][1],
                                       origin=geo_coordinates))

        return earthquakes.ordered_result()[:k] if k > 0 else []
