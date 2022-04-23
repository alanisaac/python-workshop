import itertools
import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import time
from typing import Protocol

from . import const
from . import outputs


class NumpyDistanceCalculator(Protocol):
    def __call__(
        self, lat1: ArrayLike, lng1: ArrayLike, lat2: ArrayLike, lng2: ArrayLike
    ) -> ArrayLike:
        ...


def haversine_numpy(
    earth_radius_km: float = const.DEFAULT_EARTH_RADIUS_KM,
) -> NumpyDistanceCalculator:
    def calculate(
        lat1: ArrayLike, lng1: ArrayLike, lat2: ArrayLike, lng2: ArrayLike
    ) -> ArrayLike:
        lng1, lat1, lng2, lat2 = map(np.radians, [lng1, lat1, lng2, lat2])

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = (
            np.sin(lat * 0.5) ** 2
            + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
        )

        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        d = earth_radius_km * c
        return d

    return calculate


def permutations(df: pd.DataFrame) -> pd.DataFrame:
    combinations = list(itertools.combinations(df.index, 2))
    index_columns = ["Origin_Index", "Destination_Index"]

    return (
        pd.DataFrame(combinations, columns=index_columns)
        .merge(
            df.add_suffix("_Origin"),
            left_on="Origin_Index",
            right_index=True,
        )
        .merge(
            df.add_suffix("_Destination"),
            left_on="Destination_Index",
            right_index=True,
        )
        .drop(index_columns, axis=1)
    )


def run(path: str) -> None:
    df = pd.read_csv(path, names=np.array(["City", "Latitude", "Longitude"]))
    df = permutations(df)

    start_time = time.perf_counter()
    calculator = haversine_numpy()
    distances = calculator(
        df["Latitude_Origin"],
        df["Longitude_Origin"],
        df["Latitude_Destination"],
        df["Longitude_Destination"],
    )
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    output_path = outputs.get_output_path(path)
    df = pd.concat([df, pd.Series(distances)], axis=1)
    df.drop(
        [
            "Latitude_Origin",
            "Longitude_Origin",
            "Latitude_Destination",
            "Longitude_Destination",
        ],
        axis=1,
    ).to_csv(output_path, index=False, header=False)
