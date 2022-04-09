import argparse
import csv
import pathlib
from typing import Iterable, List, Sequence

from .calculators import haversine
from .models.coordinates import Coordinates
from .models.location import Location
from .models.output import Output
from .utils import permutations


def get_arg_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input', nargs=1)
    return arg_parser


def read_input(path: str) -> Sequence[Sequence[str]]:
    data = []
    with open(path, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            data.append(row)

    return data


def parse_input(row: Sequence[str]) -> Location:
    return Location(
        row[0],
        coordinates=Coordinates(
            latitude=row[1],
            longitude=row[2]
        )
    )


def write_output(path: str, output_records: Iterable[Output]) -> None:
    with open(path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for record in output_records:
            writer.writerow(
                (record.origin, record.destination, record.distance)
            )


def run(path: str) -> int:
    data = read_input(path)

    locations: List[Location] = []
    for row in data:
        locations.append(parse_input(row))

    output_records: List[Output] = []
    calculator = haversine()
    for location_1, location_2 in permutations(locations):
        distance = calculator(location_1.coordinates, location_2.coordinates)
        output = Output(location_1.name, location_2.name, distance)
        output_records.append(output)

    output_path = pathlib.Path(path).parent / "output.csv"
    write_output(str(output_path), output_records)

    return 0


def main() -> int:
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    return run(args.input)
