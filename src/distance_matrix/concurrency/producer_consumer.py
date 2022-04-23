from enum import Enum
from typing import AsyncIterable, Literal, Protocol, TypeVar, Union


_T = TypeVar("_T")


class _Sentinel(Enum):
    """
    A sentinel value indicating the end of work in a producer / consumer queue.

    See https://github.com/python/typing/issues/689
    for more on this approach to sentinels.
    """
    VALUE = 0


class AsyncQueueProtocol(Protocol[_T]):
    async def get(self) -> Union[_T, Literal[_Sentinel.VALUE]]:
        ...

    def empty(self) -> bool:
        ...

    async def join(self) -> None:
        ...

    async def put(self, value: Union[_T, Literal[_Sentinel.VALUE]]) -> None:
        ...

    def task_done(self) -> None:
        ...


async def produce(queue: AsyncQueueProtocol[_T], items: AsyncIterable[_T]) -> None:
    async for item in items:
        await queue.put(item)

    await queue.put(_Sentinel.VALUE)


async def consume(queue: AsyncQueueProtocol[_T]) -> AsyncIterable[_T]:
    while True:
        item = await queue.get()
        try:
            if item == _Sentinel.VALUE:
                break
            else:
                yield item
        finally:
            queue.task_done()
