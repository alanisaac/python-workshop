# Static Code Analysis & Style
_TODO_

## General

There are many tools in the Python linting ecosystem.  The following is a short list of a few popular tools as examples:

- `flake8` ([GitHub](https://github.com/PyCQA/flake8)): a combination of `pyflakes`, `pycodestyle`, and `mccabe`, identifies common issues in Python code.
- `pylint` ([GitHub](https://github.com/PyCQA/pylint)): general Python static code analysis; identifies code smells and has a plugin system.
- `black` ([GitHub](https://github.com/psf/black)): "The uncompromising Python code formatter", enforces strict code style on Python projects with deliberately limited options.
- `isort` ([GitHub](https://github.com/PyCQA/isort)): simple tool to sort import statements.

These tools often have areas of overlap with one another.  In some cases, they may be incompatible with one another by default, but can be configured to work together.

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

