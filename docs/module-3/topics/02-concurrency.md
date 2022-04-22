# Asynchronous & Parallel Programming

Before we get into parallel programming, it's good to define the terminology we'll use to talk about it.  Asynchronous, concurrent, and parallel execution are all related terms but have different meanings.  Explanations around the internet [vary slightly](https://stackoverflow.com/questions/4844637/what-is-the-difference-between-concurrency-parallelism-and-asynchronous-methods), but these are the most common:

- **Parallel**: multiple tasks are executed at the same time
- **Concurrent**: multiple tasks _can_ be executed at the same time, _either_ interleaved or in parallel
- **Asynchrony**: declaring something "asynchronous" means further execution does not need to wait for it to complete.  It can be one way of expressing that code _allows for_ concurrency.

Some clarifying examples:

- I can declare my code asynchronous, but my language or framework might execute it sequentially rather than concurrently.
- I can have concurrently executing tasks, but because I only have one thread of execution, they do not execute in parallel.

To help illustrate these concepts:

![parallelism and asynchrony](./asynchronous.png)

See also:
- [Concurrent Computing (wikipedia)](https://en.wikipedia.org/wiki/Concurrent_computing)
- [Asynchrony (wikipedia)](https://en.wikipedia.org/wiki/Asynchrony_(computer_programming))

## Threading

Let's put this into practice with threads.  A thread is a separate flow of execution in a single process.

Calculating distances between two points in a distance matrix calculator is an embarrassingly parallel problem: each distance calculation is entirely independent from the others.  So we _could_ try to maximize parallelism by dividing every calculation into its own thread.  

Open up [executors.py](../../../src/distance_matrix/executors.py) and look at the implementation of `threaded_executor`.  This implementation uses a `Queue` to gather results from multiple threads.

Next, open up [main.py](../../../src/distance_matrix/main.py), and see which executor we are using in `run`.  Note also that we are timing the execution of this function.  Try running the `distance_matrix` module like so:

```sh
python -m distance_matrix tests/integration/data/locations.csv
```

And observe that the time taken is printed.  Change this out for the threaded implementation like so:

```py
executor = executors.threaded_executor(calculator)
```

Run the module again.  Was it faster or slower?

Threads come with their own overhead, so putting every calculation in its own thread may not be the most efficient way of performing these calculations.

What if we tried using a fixed number of threads?  This pattern is called a **thread pool**.  There are a couple implementations in Python, but we can make a simple thread pool of our own to demonstrate how they work.  Open up [concurrency/thread_pool.py](../../../src/distance_matrix/concurrency/thread_pool.py).

Change out the executor for the threadpool implementation like so:

```py
executor = executors.threadpool_executor(calculator)
```

> Notice in the `executors` module that we declare the `_THREAD_POOL` outside the `threadpool_executor` function, so we are not including its initialization time in the performance timing.

Run the module again.  Was it faster or slower?

The threadpool is better than individual threads, but still worse than the basic implementation.  Why is that?  There is still some overhead of threading which adds time, but importantly, the work isn't being done in parallel.

> It's hard to separate the significant overhead of creating threads from the time of the work being done.  For a more apples-to-apples comparison, try changing the number of threads in the thread pool and re-running.

To understand why this is slower, we'll need to talk about...

## CPython and the GIL

To talk about the constraints of threading in Python, it's important to talk about what Python is.  Python is a _programming language_, but Python code is executed by one of several **implementations**.  These [implementations](https://wiki.python.org/moin/PythonImplementations) include:

- **CPython**: the original, and most common implementation
- **PyPy**: Python with its own Just-In-Time (JIT) compiler
- **Jython**: Python running on the Java Virtual Machine 
- **IronPython**: Python running on the .NET CLR/DLR
 threading

You can see what implementation you're running with the following code:

```py
>>> import platform
>>> print(platform.python_implementation())
CPython
```

CPython is the one you are most likely using.  And CPython has a particular characteristic that is challenging for multithreading use cases: a **global interpreter lock** or GIL.

What does that mean?  Python is an [interpreted language](https://en.wikipedia.org/wiki/Interpreter_(computing)), which means instructions are executed without previously being compiled into machine code.  The interpreter does a lot of work in order for this to happen, and importantly, that work is not thread-safe.  Because it's not thread-safe, the interpreter must acquire a lock to make sure only one thread is executing at a time.  The net effect is that _in many cases_, Python can run threads concurrently, but not in parallel, effectively single-threading the execution of the application.

> For more than you ever wanted to know about the GIL, see [Understanding the Python GIL](http://www.dabeaz.com/GIL/)

Why "in many cases"?  The keyword in "Global Interpreter Lock" is "interpreter".  There are many tasks your computer does for a long time that does not involve interpreting Python code.  For example:

- Reading data from a large file might wait on disk
- Calling an API over the internet might wait on your network

While these operations might take a long time, they do not require the current thread to interpret any code.  They are generally called **I/O bound** operations because they [wait on I/O](https://en.wikipedia.org/wiki/I/O_bound), in contrast with **CPU bound** operations which use your computer's CPU (say, a `for` loop doing math).  Generally, I/O bound work on one thread allows other threads to continue to execute.

CPU-bound work doesn't _always_ have to lock threads, however.  Library writers can create Python code that [takes advantage of C/C++](https://docs.python.org/3/extending/extending.html) to optimize performance.  When you do that, you can control [releasing and locking the GIL](https://docs.python.org/3/c-api/init.html#releasing-the-gil-from-extension-code).

So: many libraries that perform CPU-intensive number crunching, such as [array math in `numpy`](https://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html#Threads) also release the GIL during those operations.

> If the GIL in CPython is problematic, should you use a different implementation?  Beware of premature optimization, and be extremely cautious with other implementations like PyPy as [support and tooling](https://stackoverflow.com/a/18946824) may or may not meet your needs.

Another function that releases the GIL is `time.sleep()` (after all, if one thread sleeps, other threads can do work).

To see this in action, take a look at [gil.py](../gil.py) in this topic.  Run it with:

```sh
python docs/module-3/gil.py
```

Note how it takes 1s to run rather than 5s, indicating that sleep does not wait.  If we replaced `time.sleep` with 1s worth of CPU-bound work, the script would take 5s to run instead.

## Asyncio

_TODO_

> Note: note how in our integration tests, we're also using a special `@pytest.mark.asyncio` decorator to mark tests asynchronous.  See the `pytest-asyncio` library ([GitHub](https://github.com/pytest-dev/pytest-asyncio)) for more details on that extension.

See also:
- [Python Asyncio (series)](https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-1.html)

## Multiprocessing

_TODO_

## A Note on Performance

Premature optimization: prove it

_TODO_