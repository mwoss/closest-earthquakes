from math import sqrt, radians, sin, cos, atan2

import requests

from detectors.collections.sorted import LimitedHeapSet

EARTH_RADIUS = 6371.0
USGS_URI = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"


class Coordinates:
    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude

    def __eq__(self, other: 'Coordinates'):
        return self.longitude == other.longitude and self.latitude == other.latitude

    def __hash__(self):
        return hash((self.longitude, self.latitude))


class Earthquake:
    __slots__ = ['place', 'source', 'distance']

    def __init__(self, place: str, source: Coordinates):
        self.place = place
        self.source = source


class EarthquakeWithDistance:
    def __init__(self, earthquake: Earthquake, target: Coordinates):
        self.earthquake = earthquake
        self.distance_km = self._distance_between_from(target)

    def __eq__(self, other: 'EarthquakeWithDistance') -> bool:
        return self.earthquake.source == other.earthquake.source

    def __lt__(self, other: 'EarthquakeWithDistance') -> bool:
        return self.distance_km < other.distance_km

    def __hash__(self) -> int:
        return hash(self.earthquake.source)

    def _distance_between_from(self, target: Coordinates) -> int:
        """
        Calculate distance from source of earthquake to target place.
        :param target: Target place
        :return: Distance to target place from earthquake source expressed in kilometers
        """
        lat1 = radians(target.latitude)
        lat2 = radians(self.earthquake.source.latitude)
        delta_lon = radians(self.earthquake.source.longitude) - radians(target.longitude)
        delta_lat = lat2 - lat1
        a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return int(EARTH_RADIUS * c)


class EarthquakeDetector:
    def __init__(self):
        pass

    def find_k_nearest_from(self, target: Coordinates, k: int = 10):
        request = requests.get(USGS_URI)
        features = request.json()['features']
        earthquakes = LimitedHeapSet()

        for feature in features:
            place = feature['properties']['title']
            longitude = feature['geometry']['coordinates'][0]
            latitude = feature['geometry']['coordinates'][1]
            earthquakes.add(EarthquakeWithDistance(Earthquake(place, Coordinates(longitude, latitude)),
                                                   target))

        return earthquakes.as_ordered_list()[:k] if k > 0 else []
