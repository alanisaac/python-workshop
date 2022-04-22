import pathlib
import time

from . import calculators
from . import executors
from . import inputs
from . import outputs


async def run(path: str) -> None:
    locations = inputs.read_input_async(path)

    start_time = time.perf_counter()
    calculator = calculators.haversine()
    executor = executors.asyncio_executor(calculator)
    output_records = executor(locations)
    end_time = time.perf_counter()
    print(f"{end_time - start_time:.20f}")

    output_path = pathlib.Path(path).parent / "output.csv"
    await outputs.write_output_async(str(output_path), output_records)
