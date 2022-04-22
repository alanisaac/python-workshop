from aiocsv import AsyncReader
import aiofiles
import csv
from typing import AsyncIterable, Iterable, Sequence

from .models.coordinates import Coordinates
from .models.location import Location


def _parse_input(row: Sequence[str]) -> Location:
    return Location(row[0], coordinates=Coordinates(latitude=row[1], longitude=row[2]))


def _read_csv(path: str) -> Sequence[Sequence[str]]:
    data = []
    with open(path, "r") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            data.append(row)

    return data


def read_input(path: str) -> Iterable[Location]:
    data = _read_csv(path)

    for row in data:
        location = _parse_input(row)
        yield location


async def read_input_async(path: str) -> AsyncIterable[Location]:
    async with aiofiles.open(path, "r") as input_file:
        async for row in AsyncReader(input_file):
            location = _parse_input(row)
            yield location
