from math import sqrt, radians, sin, cos, atan2
from typing import List

import requests_cache
from requests import get as get_request

from detectors.collections.sorted import LimitedMinSet
from detectors.coordinates import GeoCoordinates

EARTH_RADIUS = 6371.0
USGS_URI = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

requests_cache.install_cache(cache_name='usgs_cache', backend='sqlite', expire_after=300)


class Earthquake:
    __slots__ = ('place', 'source')

    def __init__(self, place: str, source: GeoCoordinates):
        self.place = place
        self.source = source


class EarthquakeWithDistance:
    __slots__ = ('earthquake', 'distance_km')

    def __init__(self, earthquake: Earthquake, target: GeoCoordinates):
        self.earthquake = earthquake
        self.distance_km = self._distance_from(target)

    def __eq__(self, other: 'EarthquakeWithDistance') -> bool:
        return self.earthquake.source == other.earthquake.source

    def __lt__(self, other: 'EarthquakeWithDistance') -> bool:
        return self.distance_km < other.distance_km

    def __hash__(self) -> int:
        return hash(self.earthquake.source)

    def _distance_from(self, target: GeoCoordinates) -> int:
        """
        Calculate distance from source of earthquake to target place.
        Method use haversine formula to calculate distance.
        :param target: Target place
        :return: Distance to target place from earthquake source expressed in kilometers
        """
        target_latitude = radians(target.latitude)
        source_latitude = radians(self.earthquake.source.latitude)
        delta_lon = radians(self.earthquake.source.longitude) - radians(target.longitude)
        delta_lat = source_latitude - target_latitude
        a = sin(delta_lat / 2) ** 2 + cos(target_latitude) * cos(source_latitude) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return round(EARTH_RADIUS * c)


class EarthquakeDetector:
    def k_nearest_earthquakes(self, target: GeoCoordinates, k: int = 10) -> List[EarthquakeWithDistance]:
        response = get_request(USGS_URI)
        features = response.json().get('features', [])
        earthquakes = LimitedMinSet(k)

        for feature in features:
            place = feature['properties']['title']
            longitude = feature['geometry']['coordinates'][0]
            latitude = feature['geometry']['coordinates'][1]
            earthquakes.add(EarthquakeWithDistance(Earthquake(place, GeoCoordinates(longitude, latitude)),
                                                   target))
        return earthquakes.as_ordered_list()
