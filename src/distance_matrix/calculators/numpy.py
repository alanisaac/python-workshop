from abc import ABC
import numpy as np
from numpy.typing import ArrayLike

from .. import const


class NumpyDistanceCalculator(ABC):
    def calculate_distance(
        self, lat1: ArrayLike, lng1: ArrayLike, lat2: ArrayLike, lng2: ArrayLike
    ) -> ArrayLike:
        raise NotImplementedError


class HaversineCalculator(NumpyDistanceCalculator):
    def __init__(
        self,
        earth_radius_km: float = const.DEFAULT_EARTH_RADIUS_KM
    ):
        self.earth_radius_km = earth_radius_km

    def calculate_distance(
        self, lat1: ArrayLike, lng1: ArrayLike, lat2: ArrayLike, lng2: ArrayLike
    ) -> ArrayLike:
        lng1, lat1, lng2, lat2 = map(np.radians, [lng1, lat1, lng2, lat2])

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = (
            np.sin(lat * 0.5) ** 2
            + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
        )

        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        d = self.earth_radius_km * c
        return d
