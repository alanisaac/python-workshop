import asyncio
import pathlib
import time

from . import async_runner
from . import calculators
from . import cli
from . import executors
from . import inputs
from . import outputs


def run(path: str) -> None:
    locations = list(inputs.read_input(path))

    start_time = time.perf_counter()
    calculator = calculators.haversine()
    executor = executors.basic_executor(calculator)
    output_records = executor(locations)
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    output_path = pathlib.Path(path).parent / "output.csv"
    outputs.write_output(str(output_path), output_records)


def main() -> int:
    args = cli.get_args()
    path = args.input[0]

    start_time = time.perf_counter()
    if args.asyncio:
        asyncio.run(async_runner.run(path))
    else:
        run(path)
    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time}")
    return 0
