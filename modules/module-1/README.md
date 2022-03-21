# Module 1: Environment Setup

## Virtual Environments

In Python, it's common best practice to use **virtual environments**: isolated environments for Python projects.  But why is that isolation needed in the first place?

There are a couple places that Python resolves packages from:

For system-level packages like `email`, `http`, `logging`, and others, you can find them in the `sys.prefix` directory:

```py
>>> import sys
>>> sys.prefix
'C:\\Python38'
```

Additional packages installed with tools like `pip` will install into a **site packages** directory.  You can find this directory at:

```py
>>> import site
>>> site.getsitepackages()
['C:\\Python38', 'C:\\Python38\\lib\\site-packages']
```

Importantly, Python cannot distinguish between two versions of the same installed package.  This is problematic when different projects need different versions of the same dependency.  Virtual environments solve this problem by running an isolated environment for each project.

> Some operating systems come with a system-wide installation of Python.  Avoid installing packages into a system installation, as it may require root privileges and may interfere with normal system operations.

### Using a Virtual Environment

Before we create a virtual environment, observe what Python installation you're using with the following command:

```sh
which python
```

Without a virtual environment active, this might be a system or user installation of Python.

Next, from the root of this workshop, run the following commands:

```sh
python3 -m venv .env
source .env/Scripts/activate
```

> Common conventions for virtual environment directory names include `env`, `venv`, `.env`, and `.venv`.  Regardless of the name you choose, good practice is to make sure the virtual environment directory is ignored in the repository's [`.gitignore`](../../.gitignore) file (or equivalent), to avoid checking it in to source control.

You should notice your command prompt is prefixed with the name of the virtual environment.  For example:

```sh
(.venv) Alan Pinkert@DESKTOP-IB30L3B ...
```

Now run `which python` again.  Notice that the path is pointing to the virtual environment you just created.  To demonstrate that the environments are different, let's also install a package using `pip`:

```sh
pip install requests
```

Enter the Python interpreter, and try to import the `requests` module.  The command should run successfully.

```py
>>> import requests
```

Exit the Python interpreter, and deactivate the virtual environment with:

```sh
deactivate
```

Enter the Python interpreter again, and attempt to import `requests`.  Assuming your user or system installation does not have this module, it will fail:

```py
>>> import requests
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'requests'
```


For more information on virtual environments, see [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer).

> Other package management solutions, like `conda` combine both package installation and virtual environment solutions in one.  This workshop won't go in-depth into `conda`, but for those curious on the differences see [Understanding Conda and Pip](https://www.anaconda.com/blog/understanding-conda-and-pip).

## Static Code Analysis Tools
Why?

### General

There are many tools in the Python linting ecosystem.  

- `flake8` ([GitHub](https://github.com/PyCQA/flake8)): a combination of `pyflakes`, `pycodestyle`, and `mccabe`, identifies common issues in Python code.
- `pylint` ([GitHub](https://github.com/PyCQA/pylint)): general Python static code analysis; identifies code smells and has a plugin system.
- `black` ([GitHub](https://github.com/psf/black)): "The uncompromising Python code formatter", enforces strict code style on Python projects with deliberately limited options.
- `isort` ([GitHub](https://github.com/PyCQA/isort)): simple tool to sort import statements.

These tools often have areas of overlap with one another.  In some cases, they may be incompatible with one another by default, but can be configured to work together.

### Docstrings

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

## Creating Packages

In the Python ecosystem, there are multiple ways to create and manage packages.  In this workshop, we'll cover `pip`, but `poetry` (https://python-poetry.org/) and `flit` (https://flit.readthedocs.io/en/latest/) are other options.

The Python Packaging Authority (PyPA) has good documentation on how to [create packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

_tutorial: important files, etc._

### Running a Local Package Repository

Before we publish a package, we'll need a place to publish to.  For this workshop, we'll use a local pypi server run through Docker.  To start the server, run:

```sh
docker run -d -p 80:8080 pypiserver/pypiserver:v1.4.2
```

When the command is finished, navigate to http://localhost:80 to see the server running.

### Packaging for Multiple Environments

`tox` ([GitHub](https://github.com/tox-dev/tox)) is a development automation tool that can help with many common Python tasks.  It's especially useful for testing packages against multiple Python versions, interpreters, and package dependencies.

### Publishing Packages

`twine` ([GitHub](https://github.com/pypa/twine)) is a [recommended](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) tool used to help publish packages to Python repositories.  It has better security features than basic Python packaging through verified HTTPS connections and package signing, and provides publishing as a separate step. 