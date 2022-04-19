# Pandas Best Practices

## Under The Hood: Vectorization

_TODO: preamble_

Under the hood, these libraries leverage a programming technique called **vectorization**.  Also known as array programming ([wiki](https://en.wikipedia.org/wiki/Array_programming)), vectorization allows you to apply operations to entire vectors or matrices of values much faster than iterating over those values individually.

We can demonstrate this fairly easily.  First, let's install `numpy`:

```sh
pip install numpy
```

Then, in an interpreter, let's compare a vectorized operation with a simple `for` loop:

```py
>>> import numpy as np
>>> from timeit import timeit
>>> def total():
...     total = 0
...     for i in np.arange(10000):
...         total += i
...     return total
...
>>> timeit(total, number=1000)
1.1802237999999932
>>> def total():
...     return np.sum(np.arange(10000))
...
>>> timeit(total, number=1000)
0.018799099999966984
```

We can apply these functions to our distance matrix calculator.  Whereas our current calculator signature is designed to work on a single pair of coordinates at a time, our `numpy`-driven calculator will work on vectors.

_TODO: EXAMPLE_

## Recommended Dependencies

See also: [Pandas Recommended Dependencies](https://pandas.pydata.org/docs/getting_started/install.html#recommended-dependencies)

_TODO_

## Dask

In the parallelization topic, we saw how to use different techniques in Python to take advantage of multiple cores.  Can we go bigger?

There are [many frameworks in Python](https://wiki.python.org/moin/ParallelProcessing) to scale out computation to multiple nodes in a computing cluster.  We won't cover general-purpose solutions, but rather focus on one in particular in the `numpy` / `pandas` ecosystem: **Dask**.

Dask ([GitHub](https://github.com/dask/dask)) is a library for distributed computing, built to have a similar interface as `numpy`, `pandas`, and others.  It can run locally, scaling on a single machine, or deployed in a cluster of nodes via a [mechanism like](https://blog.dask.org/2020/07/23/current-state-of-distributed-dask-clusters) Kubernetes, AWS Fargate, or HPC job managers.

_TODO_