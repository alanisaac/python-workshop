import itertools
import numpy as np
import pandas as pd
import time
from typing import Iterable

from .calculators.numpy import HaversineCalculator, NumpyDistanceCalculator
from . import outputs


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


def calculate(
    df: pd.DataFrame,
    calculator: NumpyDistanceCalculator,
    column_names: Iterable[str]
) -> pd.DataFrame:
    start_time = time.perf_counter()
    columns = map(lambda x: df[x], column_names)
    distances = calculator.calculate_distance(*columns)
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    df = pd.concat([df, pd.Series(distances)], axis=1)
    return df


def run(path: str) -> None:
    output_path = outputs.get_output_path(path)
    calculator = HaversineCalculator()
    columns = [
        "Latitude_Origin",
        "Longitude_Origin",
        "Latitude_Destination",
        "Longitude_Destination",
    ]

    _ = (
        pd.read_csv(path, names=np.array(["City", "Latitude", "Longitude"]))
        .pipe(permutations)
        .pipe(calculate, calculator, columns)
        .drop(columns, axis=1)
        .to_csv(output_path, index=False, header=False)
    )
