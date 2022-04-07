# Static Code Analysis & Style
_TODO_

## General

There are many tools in the Python linting ecosystem.  The following is a short list of a few popular tools as examples:

- `flake8` ([GitHub](https://github.com/PyCQA/flake8)): a combination of `pyflakes`, `pycodestyle`, and `mccabe`, identifies common issues in Python code.
- `pylint` ([GitHub](https://github.com/PyCQA/pylint)): general Python static code analysis; identifies code smells and has a plugin system.
- `black` ([GitHub](https://github.com/psf/black)): "The uncompromising Python code formatter", enforces strict code style on Python projects with deliberately limited options.
- `isort` ([GitHub](https://github.com/PyCQA/isort)): simple tool to sort import statements.

These tools often have areas of overlap with one another.  In some cases, they may be incompatible with one another by default, but can be configured to work together.

For example, the default settings for `isort` and `black` conflict.  However, `isort` has an [option](https://pycqa.github.io/isort/docs/configuration/black_compatibility.html) that allows you to specify `black` as your profile, by adding the following to `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
```

You can see this setting in the [pyproject.toml file](../../../pyproject.toml) in this repository.

## Docstrings

**docstrings** are string literals that document functions, classes, and other code constructs in Python, and are defined by an unassigned string directly after the documented member. They often appear in contextual overlays in IDEs, and are also accessible through the `__doc__` attribute:

```py
>>> class Square:
...   """A shape with four equal sides.""" 
... 
>>> Square.__doc__
'A shape with four equal sides.'
```

There are [multiple conventions](https://stackoverflow.com/a/24385103) for Python docstrings, including:

- `Epytext`: javadoc-like style built for `epydoc` (now pretty much dead)
- `reST`: uses the `reStructuredText` markup format
- `google`: Google made and published its own style that many projects have adopted
- `numpydoc`: uses `reST` but with a different format

Docstring formats are a matter of personal preference, but considerations include:
- **Code Analysis**: use a tool that supports enforcing your chosen format like [pydocstyle](https://www.pydocstyle.org/en/stable/usage.html).
- **IDE Support**: make sure your preferred format is supported by the range of IDEs in your organization.
- **Documentation Generators**: if you plan to create published documentation, make sure your documentation generator (like [Sphinx](https://www.sphinx-doc.org/en/master/)) supports your format.

## Type Checking

**Type Hints** in Python are code annotations that help indicate to developers what types are used for variables, arguments, and return values.  We'll go more in-depth into Python type hints in the second module of this workshop.

Type hints on their own provide documentation, but you can also pair them with static analysis tools to verify expectations about how types are used.  For example, a type checker can validate that the following scenario is incorrect:

```py
def add_numbers(a: int, b: int) -> int:
    ...

add_numbers("not a number", 7)
```

There are several static type checkers in Python, including:

- `mypy` ([GitHub](https://github.com/python/mypy)): originally made by Dropbox, including [Python's BDFL Guido](https://gvanrossum.github.io/), the oldest and most widely used type checker
- `pyright` ([GitHub](https://github.com/microsoft/pyright)): Microsoft's type checker, known for its speed and incremental updates, as well as being the embedded type checker in `pylance`
- `pytype` ([GitHub](https://github.com/google/pytype)): Google's type checker, known for being able to infer type problems without type hints
- `pyre` ([GitHub](https://github.com/facebook/pyre-check)): Facebook's type checker, similar to the others but also includes some security-related features as well

See [this article](https://www.infoworld.com/article/3575079/4-python-type-checkers-to-keep-your-code-clean.html) for a more detailed comparison of these type checkers.

For the purposes of this workshop, we'll use `mypy`, but it's worth exploring the other options if the features sound interesting or `mypy` doesn't meet your needs.

## Persisting Development Requirements
Static analysis and testing tools are added for development purposes, but shouldn't be packaged along with your code.

It's common practice to persist development requirements as well as package requirements in the reepository.

Pipenv ([GitHub](https://github.com/pypa/pipenv)) is another great tool to help with managing package requirements, and specifically handles a separation between dev requirements and package requirements.  For now, we'll stick with using `requirements.txt` files.

_TODO_

