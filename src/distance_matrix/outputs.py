import csv
import pathlib
from typing import AsyncIterable, Iterable

from .models.output import Output


def get_output_path(input_path: str) -> str:
    return str(pathlib.Path(input_path).parent / "output.csv")


def write_output(path: str, output_records: Iterable[Output]) -> None:
    with open(path, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        for record in output_records:
            writer.writerow((record.origin, record.destination, record.distance))


async def write_output_async(path: str, output_records: AsyncIterable[Output]) -> None:
    with open(path, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        async for record in output_records:
            writer.writerow((record.origin, record.destination, record.distance))
