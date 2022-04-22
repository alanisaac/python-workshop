from typing import AsyncIterable, Iterable, List, Tuple, TypeVar

from .concurrency.queue import AsyncQueueProtocol


_T = TypeVar("_T")


def permutations(iterable: Iterable[_T]) -> Iterable[Tuple[_T, _T]]:
    """
    Returns the set of permutations from a single sequence.

    This is available as `itertools.permutations`,
    but implemented here as an example of type vars.
    """
    existing: List[_T] = []
    count = 0
    for first in iterable:
        for second in existing[:count]:
            yield (second, first)
        count += 1
        existing.append(first)


async def permutations_async(
    iterable: AsyncIterable[_T]
) -> AsyncIterable[Tuple[_T, _T]]:
    """
    Returns the set of permutations from a single sequence.
    """
    existing: List[_T] = []
    count = 0
    async for first in iterable:
        for second in existing[:count]:
            yield (second, first)
        count += 1
        existing.append(first)


async def consume(queue: AsyncQueueProtocol[_T]) -> AsyncIterable[_T]:
    while True:
        item = await queue.get()
        try:
            yield item
        finally:
            queue.task_done()
