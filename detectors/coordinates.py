class CoordinateException(Exception):
    def __init__(self, message: str, coordinate: float):
        self.coordinate = coordinate
        self.message = message
        super().__init__(message)


class GeoCoordinates:
    __slots__ = ('_longitude', '_latitude')

    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude

    def __eq__(self, other) -> bool:
        return self.longitude == other.longitude and self.latitude == other.latitude

    def __hash__(self) -> int:
        return hash((self.longitude, self.latitude))

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, coordinate: float):
        if -180.0 > coordinate or coordinate > 180.0:
            raise CoordinateException(f"Incorrect longitude value: {coordinate}", coordinate)
        self._longitude = coordinate

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, coordinate: float):
        if -90.0 > coordinate or coordinate > 90.0:
            raise CoordinateException(f"Incorrect latitude value: {coordinate}", coordinate)
        self._latitude = coordinate
