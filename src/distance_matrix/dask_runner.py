import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
import numpy as np
import pandas as pd
import pathlib
import time

from .calculators.numpy import HaversineCalculator
from .pandas_runner import permutations
from . import outputs


def coerce_path(path_str: str) -> str:
    path = pathlib.Path(path_str)
    return str(path.with_name(path.stem) / f"*{path.suffix}")


def run(path: str) -> None:
    cluster = LocalCluster()
    _ = Client(cluster)

    input(f"Press enter to continue, see dashboard at {cluster.dashboard_link}\n")

    df = pd.read_csv(path, names=np.array(["City", "Latitude", "Longitude"]))
    df = permutations(df)
    df = dd.from_pandas(df, npartitions=4)

    start_time = time.perf_counter()
    calculator = HaversineCalculator()
    distances = calculator.calculate_distance(
        df["Latitude_Origin"],
        df["Longitude_Origin"],
        df["Latitude_Destination"],
        df["Longitude_Destination"],
    )
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    output_path = outputs.get_output_path(path)
    output_path = coerce_path(output_path)

    df = dd.concat([df, pd.Series(distances)], axis=1)
    df.drop(
        [
            "Latitude_Origin",
            "Longitude_Origin",
            "Latitude_Destination",
            "Longitude_Destination",
        ],
        axis=1,
    ).to_csv(output_path, index=False, header=False)
    input("Press enter to terminate\n")
