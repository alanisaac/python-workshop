from abc import ABC
from math import atan2, cos, radians, sin, sqrt

from ..models.coordinates import Coordinates
from .. import const


class DistanceCalculator(ABC):
    def calculate_distance(self, p1: Coordinates, p2: Coordinates) -> float:
        raise NotImplementedError()


class HaversineCalculator(DistanceCalculator):
    def __init__(
        self,
        earth_radius_km: float = const.DEFAULT_EARTH_RADIUS_KM
    ):
        self.earth_radius_km = earth_radius_km

    def calculate_distance(self, p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = self.earth_radius_km * c
        return d


class EquirectangularCalculator(DistanceCalculator):
    def __init__(
        self,
        earth_radius_km: float = const.DEFAULT_EARTH_RADIUS_KM
    ):
        self.earth_radius_km = earth_radius_km

    def calculate_distance(self, p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        x = lng2 - lng1 * cos((lat1 + lat2) / 2)
        y = lat2 - lat1
        d = sqrt(x * x + y * y) * self.earth_radius_km
        return d
