import asyncio
from asyncio import Queue

from . import calculators
from . import inputs
from . import outputs
from . import utils
from .concurrency.queue import AsyncQueueProtocol
from .models.location import Location
from .models.output import Output


async def _read_inputs_task(output: AsyncQueueProtocol[Location], path: str) -> None:
    locations = inputs.read_input_async(path)
    async for location in locations:
        await output.put(location)


async def _calculate_task(
    input: AsyncQueueProtocol[Location],
    output: AsyncQueueProtocol[Output]
) -> None:
    locations = utils.consume(input)
    permutations = utils.permutations_async(locations)
    calculator = calculators.haversine()
    async for location_1, location_2 in permutations:
        distance = calculator(location_1.coordinates, location_2.coordinates)
        output_record = Output(location_1.name, location_2.name, distance)
        await output.put(output_record)


async def _write_task(input: AsyncQueueProtocol[Output], path: str) -> None:
    output_path = outputs.get_output_path(path)
    output_records = utils.consume(input)
    await outputs.write_output_async(output_path, output_records)


async def run(path: str) -> None:
    input_queue: AsyncQueueProtocol[Location] = Queue()
    output_queue: AsyncQueueProtocol[Output] = Queue()

    input_task = asyncio.create_task(_read_inputs_task(input_queue, path))
    _ = asyncio.create_task(_calculate_task(input_queue, output_queue))
    _ = asyncio.create_task(_write_task(output_queue, path))

    await input_task
    await input_queue.join()
    await output_queue.join()
