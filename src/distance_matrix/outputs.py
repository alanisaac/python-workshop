import csv
from typing import Iterable

from .models.output import Output


def write_output(path: str, output_records: Iterable[Output]) -> None:
    with open(path, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        for record in output_records:
            writer.writerow((record.origin, record.destination, record.distance))
