from typing import Protocol
from math import radians, cos, sin, sqrt, atan2
from .models.coordinates import Coordinates


class DistanceCalculator(Protocol):
    def __call__(self, p1: Coordinates, p2: Coordinates) -> float:
        ...


def haversine(earth_radius_km: float = 6371.0088) -> DistanceCalculator:
    def calculate(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = earth_radius_km * c
        return d

    return calculate


def equirectangular(earth_radius_km: float = 6371.0088) -> DistanceCalculator:
    def calculate(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        x = lng2 - lng1 * cos((lat1 + lat2) / 2)
        y = lat2 - lat1
        d = sqrt(x * x + y * y) * earth_radius_km
        return d

    return calculate
