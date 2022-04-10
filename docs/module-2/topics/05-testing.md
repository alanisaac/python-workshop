# Testing

![](https://geekandpoke.typepad.com/.a/6a00d8341d3df553ef01116901f637970c-800wi)

_[credit: geek & poke](https://geekandpoke.typepad.com/geekandpoke/2009/03/stress-test.html) ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/))_

## Test Runners

There are a few popular test runners in the Python ecosystem:

- `unittest` is both the testing framework that comes with Python as well as the default test runner.  It provides basic functionality to organize tests in test classes derived from `unittest.TestCase`.  Other test runners typically can run `unittest` test cases.
- `pytest` ([GitHub](https://github.com/pytest-dev/pytest)) is an alternative test runner with a broad set of features that allows for plain function tests and the use of Python's `assert` statement.
- `nose2` ([GitHub](https://github.com/nose-devs/nose2)) is another test runner, very similar to `pytest` but somewhat less popular.

For the purposes of this workshop, we'll explore testing using `pytest`.

> `pytest` has a [huge array](https://docs.pytest.org/en/7.0.x/reference/plugin_list.html) of plugins.  We'll cover a few important ones in this workshop, but if there's a specific testing use case you need to cover, it's a good idea to check on whether there's a `pytest` plugin for it.

If you haven't already, install `pytest` with:

```sh
pip install pytest
```

## Test Structure

By convention, tests in Python are commonly discovered by searching for functions with a `test_` prefix, inside of files with a `test_` prefix.  Most test runners, `pytest` included have their own [discovery mechanism](https://docs.pytest.org/en/6.2.x/goodpractices.html#conventions-for-python-test-discovery), and offer a way to [change those conventions](https://docs.pytest.org/en/6.2.x/example/pythoncollection.html#changing-naming-conventions).

`pytest` allows you to write tests directly within test modules or use `unittest.TestCase` to group them into classes (also prefixed with `Test`, by convention).  Which pattern you see in the wild can be a matter of personal preference.

### Functional Method

Let's take a test from the `tests/models/test_coordinates.py` file.  This is an example of the functional style of testing:

```py
@pytest.mark.parametrize(
    "latitude,longitude",
    [
        (0, 0),
        (90, 180),
        (-90, -180)
    ]
)
def test_valid_coordinates_are_constructed_correctly(latitude, longitude):
    coordinates = Coordinates(latitude=latitude, longitude=longitude)

    assert coordinates.latitude == latitude
    assert coordinates.longitude == longitude

```

The test is defined directly in the module.  If common setup or teardown is needed across multiple tests, you can use **fixtures** to represent it.  We won't go in-depth into fixtures in this workshop, but `pytest` has good documentation on how to use them:

- For simple setup use cases, see [this section](https://docs.pytest.org/en/latest/how-to/fixtures.html#quick-example). 
- For setup and teardown use cases see [this section](https://docs.pytest.org/en/latest/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization). 

### Class Method

`pytest` can also represent tests in classes (`unittest` style).  Let's take our tests and change them into the class style.  

Parameterization, through `pytest.mark.parametrize` isn't supported between `pytest` and `TestCase`.  However, we can use the `parameterized` library ([GitHub](https://github.com/wolever/parameterized)) to help:

```sh
pip install parameterized
```

With this library, we can change our tests to:

```py
from parameterized import parameterized
import pytest
from pydantic import ValidationError
from unittest import TestCase

from distance_matrix.models.coordinates import Coordinates


class TestCoordinates(TestCase):
    @parameterized.expand(
        [
            (-1000, 0),
            (1000, 0),
            (0, -1000),
            (0, 1000)
        ]
    )
    def test_invalid_coordinates_raises_error(self, latitude, longitude):
        with pytest.raises(ValidationError):
            _ = Coordinates(latitude=latitude, longitude=longitude)

    @parameterized.expand(
        [
            (0, 0),
            (90, 180),
            (-90, -180)
        ]
    )
    def test_valid_coordinates_are_constructed_correctly(self, latitude, longitude):
        coordinates = Coordinates(latitude=latitude, longitude=longitude)

        assert coordinates.latitude == latitude
        assert coordinates.longitude == longitude
```

> Note how there is less boilerplate with the `parameterized` library (no need to define variable names).  You can use it with either test case style, and it works with the other major test runners above.

`TestCase` has a number of functions on it commonly used for setup and teardown of tests:

- `setUp` / `tearDown`
- `setUpClass` / `tearDownClass`
- `setUpModule` / `tearDownModule`

### Parallelizing Execution

For unit tests, by default `pytest` will run them sequentially.  If your test cases are thread-safe, you might want to parallelize execution of those tests.  This can help speed up tests both locally, and in CI pipelines.

The `pytest-xdist` plugin ([GitHub](https://github.com/pytest-dev/pytest-xdist)) allows you to run tests in parallel.  You can install it with:

```
pip install pytest-xdist
```

It will run tests in parallel according to the number of CPU cores with the command:

```sh
pytest -n auto
```

Notice that the output from testing is slightly different (for the curious, `gw` stands for "`execnet`'s [gateway](https://execnet.readthedocs.io/en/latest/basics.html)" but is essentially a subprocess).

> `pytest-parallel` ([GitHub](https://github.com/browsertron/pytest-parallel)) is a newer plugin that can additionally handle testing concurrency, if needed.

## Mocking & Patching

_TODO_

## Code Coverage Tools

### coverage
The `coverage` package ([GitHub](https://github.com/nedbat/coveragepy)) provides code coverage support for Python.  It can measure line or branch coverage, and supports outputs in a variety of standard formats, including HTML, XML (Cobertura), JSON, and LCOV, allowing it to integrate with most popular CI tools.

When using `pytest`, it is recommended to use the `pytest-cov` plugin ([GitHub](https://github.com/pytest-dev/pytest-cov)) as opposed to using `coverage` directly.  `pytest-cov` is a wrapper around `coverage` but slightly better compatibility and supports collecting coverage while using `pytest-xdist` as well.  Let's install it with:

```sh
pip install pytest-cov
```

And then run it with:

```sh
pytest --cov=src
```

Both PyCharm and VS Code have the ability to display code coverage reports within the IDE.  Many CI/CD tools can also display code coverage, check your tool's docs for integration steps.

In both of these cases, the [calculators.py file](../../../src/distance_matrix/calculators.py) is a good example to look at, as it is partially covered.

#### PyCharm Integration (Professional Only)

PyCharm can only show coverage reports in the professional edition.  You'll want to configure pytest to generate an `xml` coverage report:

```sh
pytest --cov=src --cov-report=xml
```

You'll also need a setting in your `.coveragerc` file.  See [this StackOverflow post](https://stackoverflow.com/a/68231308) for details.

#### VS Code Integration

In VS Code, you'll need a code coverage plugin like [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters).  To generate an `xml` coverage report, run `pytest` like so:

```sh
pytest --cov=src --cov-report=xml
```

### diff_cover
While `coverage` provides overall code coverage reports, it can also be useful to understand coverage changes as a result of a pull request (or "merge request", "diff", etc. depending on your source control tool of choice).

The `diff_cover` package ([GitHub](https://github.com/Bachmann1234/diff_cover)) adds this capability, combining a code coverage report generated from a tool like `coverage` with `git diff` to produce coverage information specifically for lines in the diff.  Install it with:

```py
pip install diff_cover
```

Now let's make a change that would change our code coverage.  For example, write a new function in any `src` file.  Then re-run `pytest` with coverage and run `diff-cover`:

```sh
pytest --cov=src --cov-report=xml
diff-cover coverage.xml
```

You'll see a report with coverage differences.  This can be helpful to identify missing coverage in changes you made, so you don't need to hunt them down in the overall report.  You can also generate this report in [other formats](https://github.com/Bachmann1234/diff_cover#getting-started) like markdown and HTML.

> Note that when used in CI, you may need to ensure that **both** the `main` branch and `merging` branch involved in the diff are available in order to make a comparison.

One pattern for improving unit test coverage in a codebase, for example, is to set a coverage standard for _new_ code.  `diff_cover` allows for this enforcement with the `--fail-under` flag, which you can run in CI environments.
