import csv
from typing import AsyncIterable, Iterable, Sequence

from .models.coordinates import Coordinates
from .models.location import Location


def _parse_input(row: Sequence[str]) -> Location:
    return Location(row[0], coordinates=Coordinates(latitude=row[1], longitude=row[2]))


def read_input(path: str) -> Iterable[Location]:
    with open(path, "r") as input_file:
        for row in csv.reader(input_file):
            location = _parse_input(row)
            yield location


async def read_input_async(path: str) -> AsyncIterable[Location]:
    with open(path, "r") as input_file:
        for row in csv.reader(input_file):
            location = _parse_input(row)
            yield location
