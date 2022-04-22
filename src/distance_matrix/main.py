import pathlib
import time

from . import calculators
from . import cli
from . import executors
from . import inputs
from . import outputs


def run(path: str) -> int:
    locations = list(inputs.read_input(path))

    start_time = time.perf_counter()
    calculator = calculators.haversine()
    executor = executors.basic_executor(calculator)
    output_records = executor(locations)
    end_time = time.perf_counter()
    print(f"{end_time - start_time:.20f}")

    output_path = pathlib.Path(path).parent / "output.csv"
    outputs.write_output(str(output_path), output_records)

    return 0


def main() -> int:
    args = cli.get_args()
    return run(args.input[0])
