# Asynchronous & Parallel Programming

Before we get into parallel programming, it's good to define the terminology we'll use to talk about it.  Asynchronous, concurrent, and parallel execution are all related terms but have different meanings.  Explanations around the internet [vary slightly](https://stackoverflow.com/questions/4844637/what-is-the-difference-between-concurrency-parallelism-and-asynchronous-methods), but these are the most common:

- **Parallel**: multiple tasks are executed at the same time
- **Concurrent**: multiple tasks _can_ be executed at the same time, _either_ interleaved or in parallel
- **Asynchrony**: declaring something "asynchronous" means further execution does not need to wait for it to complete.  It can be one way of expressing that code _allows for_ concurrency.

Some clarifying examples:

- I can declare my code asynchronous, but my language or framework might execute it sequentially rather than concurrently.
- I can have concurrently executing tasks, but because I only have one thread of execution, they do not execute in parallel.

See also:
- [Concurrent Computing (wikipedia)](https://en.wikipedia.org/wiki/Concurrent_computing)
- [Asynchrony (wikipedia)](https://en.wikipedia.org/wiki/Asynchrony_(computer_programming))

## Threading

_TODO_

## CPython and the GIL

_TODO_

## Asyncio

_TODO_

## Multiprocessing

_TODO_