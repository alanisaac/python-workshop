# Testing

## Testing Basics

_TODO_

## Mocking & Patching

_TODO_

## Code Coverage Tools

### coverage
The `coverage` package ([GitHub](https://github.com/nedbat/coveragepy)) provides code coverage support for Python.  It can measure line or branch coverage, and supports outputs in a variety of standard formats, including HTML, XML (Cobertura), JSON, and LCOV, allowing it to integrate with most popular CI tools.

### diff_cover
While `coverage` provides overall code coverage reports, it can also be useful to understand coverage changes as a result of a pull request (or "merge request", "diff", etc. depending on your source control tool of choice).

The `diff_cover` package ([GitHub](https://github.com/Bachmann1234/diff_cover)) adds this capability, combining a code coverage report generated from a tool like `coverage` with `git diff` to produce coverage information specifically for lines in the diff.  

> Note that when used in CI, you may need to ensure that **both** the `main` branch and `merging` branch involved in the diff are available in order to make a comparison.

One pattern for improving unit test coverage in a codebase, for example, is to set a coverage standard for _new_ code.  `diff_cover` allows for this enforcement with the `--fail-under` flag.