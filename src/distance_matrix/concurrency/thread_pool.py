from queue import Queue
from threading import Thread
from typing import Any, Callable, Dict, List, NamedTuple, Tuple

from .queue import QueueProtocol


class _Task(NamedTuple):
    func: Callable
    args: Tuple
    kwargs: Dict[str, Any]


def _run_thread(tasks: QueueProtocol[_Task]) -> None:
    while True:
        func, args, kwargs = tasks.get()
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            tasks.task_done()


class ThreadPool:
    """
    A simple threadpool.

    See also:
        concurrent.futures.ThreadPoolExecutor
        multiprocessing.pool.ThreadPool
    """
    def __init__(self, count: int) -> None:
        self.count = count
        self.tasks: QueueProtocol[_Task] = Queue()
        self.threads: List[Thread] = []

        for _ in range(count):
            new_thread = Thread(
                target=_run_thread,
                args=(self.tasks,)
            )
            new_thread.daemon = True
            new_thread.start()
            self.threads.append(new_thread)

    def add(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        self.tasks.put(_Task(func, args, kwargs))

    def wait_for_completion(self) -> None:
        self.tasks.join()
