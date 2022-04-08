# Testing

## Test Runners

There are a few popular test runners in the Python ecosystem:

- `unittest` is both the testing framework that comes with Python as well as the default test runner.  It provides basic functionality to organize tests in test classes derived from `unittest.TestCase`.  Other test runners typically can run `unittest` test cases.
- `pytest` ([GitHub](https://github.com/pytest-dev/pytest)) is an alternative test runner with a broad set of features that allows for plain function tests and the use of Python's `assert` statement.
- `nose2` ([GitHub](https://github.com/nose-devs/nose2)) is another test runner, very similar to `pytest` but somewhat less popular.

For the purposes of this workshop, we'll explore testing using `pytest`.

> `pytest` has a [huge array](https://docs.pytest.org/en/7.0.x/reference/plugin_list.html) of plugins.  We'll cover a few important ones in this workshop, but if there's a specific testing use case you neeed to cover, it's a good idea to check on whether there's a `pytest` plugin for it.

If you haven't already, install `pytest` with:

```sh
pip install pytest
```

## Test Structure

`pytest` allows you to write tests directly within test modules or use `unittest.TestCase` to group them into classes.  Which pattern you see in the wild can be a matter of personal preference.

### Class Method

_TODO_

### Functional Method

_TODO_

### Parallelizing Execution

For unit tests, by default `pytest` will run them sequentially.  If your test cases are thread-safe, you might want to parallelize execution of those tests.  This can help speed up tests both locally, and in CI pipelines.

The `pytest-xdist` plugin ([GitHub](https://github.com/pytest-dev/pytest-xdist)) allows you to run tests in parallel.  It will run tests in parallel according to the number of CPU cores with the command:

```sh
pytest -n auto
```

> `pytest-parallel` ([GitHub](https://github.com/browsertron/pytest-parallel)) is a newer plugin that can additionally handle testing concurrency, if needed.

## Mocking & Patching

_TODO_

## Code Coverage Tools

### coverage
The `coverage` package ([GitHub](https://github.com/nedbat/coveragepy)) provides code coverage support for Python.  It can measure line or branch coverage, and supports outputs in a variety of standard formats, including HTML, XML (Cobertura), JSON, and LCOV, allowing it to integrate with most popular CI tools.

When using `pytest`, it is recommended to use the `pytest-cov` plugin ([GitHub](https://github.com/pytest-dev/pytest-cov)) as opposed to using `coverage` directly.  `pytest-cov` is a wrapper around `coverage` but slightly better compatibility and supports collecting coverage while using `pytest-xdist` as well.

_TODO: Example_

### diff_cover
While `coverage` provides overall code coverage reports, it can also be useful to understand coverage changes as a result of a pull request (or "merge request", "diff", etc. depending on your source control tool of choice).

The `diff_cover` package ([GitHub](https://github.com/Bachmann1234/diff_cover)) adds this capability, combining a code coverage report generated from a tool like `coverage` with `git diff` to produce coverage information specifically for lines in the diff.  

> Note that when used in CI, you may need to ensure that **both** the `main` branch and `merging` branch involved in the diff are available in order to make a comparison.

One pattern for improving unit test coverage in a codebase, for example, is to set a coverage standard for _new_ code.  `diff_cover` allows for this enforcement with the `--fail-under` flag.

_TODO: Example_