import asyncio
from asyncio import Queue
from typing import AsyncIterable

from . import inputs
from . import outputs
from . import utils
from .calculators.functional import haversine
from .concurrency.producer_consumer import AsyncQueueProtocol, consume, produce
from .models.location import Location
from .models.output import Output


async def _read_inputs_task(output: AsyncQueueProtocol[Location], path: str) -> None:
    locations = inputs.read_input_async(path)
    await produce(output, locations)


async def _calculate_task(
    input: AsyncQueueProtocol[Location],
    output: AsyncQueueProtocol[Output]
) -> None:
    async def calculate() -> AsyncIterable[Output]:
        locations = consume(input)
        permutations = utils.permutations_async(locations)
        calculator = haversine()
        async for location_1, location_2 in permutations:
            distance = calculator(location_1.coordinates, location_2.coordinates)
            output_record = Output(location_1.name, location_2.name, distance)
            yield output_record

    output_records = calculate()
    await produce(output, output_records)


async def _write_task(input: AsyncQueueProtocol[Output], path: str) -> None:
    output_path = outputs.get_output_path(path)
    output_records = consume(input)
    await outputs.write_output_async(output_path, output_records)


async def run(path: str) -> None:
    input_queue: AsyncQueueProtocol[Location] = Queue()
    output_queue: AsyncQueueProtocol[Output] = Queue()

    input_task = asyncio.create_task(_read_inputs_task(input_queue, path))
    calculate_task = asyncio.create_task(_calculate_task(input_queue, output_queue))
    output_task = asyncio.create_task(_write_task(output_queue, path))

    tasks = (input_task, calculate_task, output_task)
    for task in tasks:
        await task
