import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
import numpy as np
import pandas as pd
import pathlib
import time
from typing import Iterable

from .calculators.numpy import HaversineCalculator, NumpyDistanceCalculator
from .pandas_runner import permutations
from . import outputs


def coerce_path(path_str: str) -> str:
    path = pathlib.Path(path_str)
    return str(path.with_name(path.stem) / f"*{path.suffix}")


def calculate(
    ddf: dd.DataFrame,
    calculator: NumpyDistanceCalculator,
    column_names: Iterable[str]
) -> dd.DataFrame:
    start_time = time.perf_counter()
    columns = map(lambda x: ddf[x], column_names)
    distances = calculator.calculate_distance(*columns)
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    ddf = dd.concat([ddf, pd.Series(distances)], axis=1)
    return ddf


def run(path: str) -> None:
    cluster = LocalCluster()
    _ = Client(cluster)

    input(f"Press enter to continue, see dashboard at {cluster.dashboard_link}\n")

    calculator = HaversineCalculator()
    output_path = outputs.get_output_path(path)
    output_path = coerce_path(output_path)
    column_names = [
        "Latitude_Origin",
        "Longitude_Origin",
        "Latitude_Destination",
        "Longitude_Destination",
    ]

    _ = (
        pd.read_csv(path, names=np.array(["City", "Latitude", "Longitude"]))
        .pipe(permutations)
        .pipe(dd.from_pandas, npartitions=4)
        .pipe(calculate, calculator, column_names)
        .drop(column_names, axis=1)
        .to_csv(output_path, index=False, header=False)
    )

    input("Press enter to terminate dashboard\n")
