from typing import Protocol, TypeVar


_T = TypeVar("_T")


class QueueProtocol(Protocol[_T]):
    def get(self) -> _T:
        ...

    def empty(self) -> bool:
        ...

    def join(self) -> None:
        ...

    def put(self, value: _T) -> None:
        ...

    def task_done(self) -> None:
        ...
