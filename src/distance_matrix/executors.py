from queue import Queue
from threading import Thread
from typing import List, Sequence, Protocol, Tuple

from .calculators import DistanceCalculator
from .models.location import Location
from .models.output import Output
from .utils import permutations


class Executor(Protocol):
    def __call__(
        self,
        locations: Sequence[Location]
    ) -> Sequence[Output]:
        ...


def basic_executor(calculator: DistanceCalculator) -> Executor:
    def execute(locations: Sequence[Location]) -> Sequence[Output]:
        output_records: List[Output] = []
        for location_1, location_2 in permutations(locations):
            distance = calculator(location_1.coordinates, location_2.coordinates)
            output = Output(location_1.name, location_2.name, distance)
            output_records.append(output)

        return output_records
    return execute


def calculate_threaded(
    calculator: DistanceCalculator,
    locations: Tuple[Location, Location],
    results_queue: Queue,
) -> None:
    origin = locations[0]
    destination = locations[1]
    distance = calculator(origin.coordinates, destination.coordinates)
    output = Output(origin.name, destination.name, distance)
    results_queue.put(output)


def threaded_executor(calculator: DistanceCalculator) -> Executor:
    def execute(locations: Sequence[Location]) -> Sequence[Output]:
        output_records: List[Output] = []
        threads: List[Thread] = []
        results_queue: Queue = Queue()
        for pair in permutations(locations):
            new_thread = Thread(
                target=calculate_threaded,
                args=(
                    calculator,
                    pair,
                    results_queue
                )
            )
            threads.append(new_thread)
            new_thread.start()

        for thread in threads:
            thread.join()

        while not results_queue.empty():
            output = results_queue.get()
            output_records.append(output)

        return output_records

    return execute
