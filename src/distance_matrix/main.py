import asyncio
import time

from .calculators.functional import haversine
from . import async_runner
from . import cli
from . import executors
from . import inputs
from . import outputs
from . import pandas_runner


def run(path: str) -> None:
    locations = list(inputs.read_input(path))

    start_time = time.perf_counter()
    calculator = haversine()
    executor = executors.basic_executor(calculator)
    output_records = executor(locations)
    end_time = time.perf_counter()
    print(f"Calc time: {end_time - start_time:.20f}")

    output_path = outputs.get_output_path(path)
    outputs.write_output(output_path, output_records)


def main() -> int:
    args = cli.get_args()
    path = args.input[0]

    start_time = time.perf_counter()

    if args.runner == cli.Runner.STANDARD:
        run(path)
    elif args.runner == cli.Runner.ASYNCIO:
        asyncio.run(async_runner.run(path))
    elif args.runner == cli.Runner.PANDAS:
        pandas_runner.run(path)
    else:
        raise ValueError(f"The runner '{args.runner}' is not supported")

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time}")
    return 0
