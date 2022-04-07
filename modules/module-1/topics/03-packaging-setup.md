# Packaging Setup

In the Python ecosystem, there are multiple ways to create and manage packages.  In this workshop, we'll cover `pip`, but `poetry` (https://python-poetry.org/) and `flit` (https://flit.readthedocs.io/en/latest/) are other options.

Note that there are two things in the Python ecosystem called "packages":

- **Import packages** ([glossary](https://packaging.python.org/en/latest/glossary/#term-Import-Package)) are collections of modules.  _Essentially_, a folder with an `__init__.py` file.
- **Distribution packages** ([glossary](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)) are archived files that you publish and install.  A Python distribution package generally contains one or more import packages.

For this workshop we'll refer to both as "package" but clarify if the type can't be inferred from context.

## Repository Layout

Before we start on creating packages, it's worth discussing the layout of the repository.  There are two common patterns for repositories designed for Python packaging:

### The `src` Layout

The [src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout) places one or more packages underneath a `src` directory, like so:

```
project_root_directory
├── pyproject.toml
├── setup.cfg  # or setup.py
├── ...
└── src/
    └── mypkg/
        ├── __init__.py
        ├── ...
        └── mymodule.py
```

This package layout is easier for packaging, as there's less chance that you accidentally distribute files in your package that you don't mean to.  However, it's harder for dealing with the Python REPL and for testing, as the default `PYTHONPATH` will not contain your package.

### The Flat Layout

The [flat-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#flat-layout) places the main package under the repository root directory, like so:

```
project_root_directory
├── pyproject.toml
├── setup.cfg  # or setup.py
├── ...
└── mypkg/
    ├── __init__.py
    ├── ...
    └── mymodule.py
```

This makes it very easy to use the REPL, but packaging may be more error-prone.

### Which to Choose?

This is still under active debate in the Python community, though `src` has grown in popularity.  Here are examples of each in popular packages:

Flat Layouts:
- [requests](https://github.com/psf/requests)
- [numpy](https://github.com/numpy/numpy)

Src Layouts:
- [dateutil](https://github.com/dateutil/dateutil)
- [cryptography](https://github.com/pyca/cryptography)
- [flask](https://github.com/pallets/flask)
- [pytest](https://github.com/pytest-dev/pytest)


For more on the benefits of the `src` layout, [see this blog post](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure), and this follow-up.

See also this [GitHub discussion](https://github.com/pypa/packaging.python.org/issues/320#issuecomment-495990983).

This repository uses the `src` layout.  While it's a little less accessible for beginners, it's useful to understand the benefits and how to work in this layout.

## Package Creation

The Python Packaging Authority (PyPA) has good documentation on how to [create packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/).  What follows is an abbreviated and adapted version of that tutorial.

### Important Files

- `pyproject.toml` ([link](../../../pyproject.toml)) contains metadata about the build of your project, like the packages necessary for a build and the build system to use.
- `setup.cfg` ([link](../../../setup.cfg)) contains metadata describing the distribution package to build, like the name, version, and where to find import packages.

Open up the links above to explore these files in more detail:  

- Note how in the `[options]` section, the distribution package is set up to `find:` import packages in the `src` folder, as we're using the `src` layout. 
- Think the syntax for `package_dir` looks funny?  `package_dir` is actually a mapping, and we're [mapping the empty string](https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages) to `src`.

> In more advanced scenarios, you can create package metadata programmatically using a `setup.py` file instead of `setup.cfg`.  Best practice is to do this only when absolutely necessary, so it won't be covered in this workshop.  For more info, see the guide to [different metadata configurations](https://packaging.python.org/en/latest/tutorials/packaging-projects/#configuring-metadata).

### Defining Package Dependencies

Our package uses `pydantic`, but it's not listed as a dependency -- let's fix that.  Package dependencies are defined using the `install_requires` option in metadata.  Copy and paste the following into the `setup.cfg` file, under the `[options]` section:

```ini
install_requires =
    pydantic >= 1.7
```

Note how we're specifying a dependency version greater than or equal to `1.7`.  Python package versioning and the syntax to specify dependency versions is defined by [PEP-440](https://peps.python.org/pep-0440/).

We can also use `pip-compile` to create a `requirements.txt` file, just like we did for `dev-requirements.txt`:

```sh
pip-compile setup.cfg
```

Later on, we'll see how to test that different versions of a dependency work with our library.

### Creating a Build

Since we have the package files already created, we can create a build.

First, let's make sure we have the most up-to-date version of the build package.  In the virtual environment for this repository, run the following command:

```sh
python -m pip install --upgrade build
```

Next, we'll build the package.  In the virtual environment for this repository, run the following command:

```sh
python -m build
```

This command should output a lot of text and once completed should generate two files in the `dist` directory:

- a `.tar.gz` file, which is a [source archive](https://packaging.python.org/en/latest/glossary/#term-Source-Archive)
- a `.whl` file, which is a [built distribution](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)

> Newer pip versions preferentially install built distributions, but will fall back to source archives if needed. Best practice is to publish both.

## Package Publishing

### Running a Local Package Repository

Before we publish a package, we'll need a place to publish to.  There is a [test PyPI server](https://packaging.python.org/en/latest/guides/using-testpypi/) that you can use to test out publishing packages publically.  However, it requires registering user accounts and periodically gets pruned.

For the purposes of this workshop, we'll run a local PyPI server through Docker and `pypiserver` ([GitHub](https://github.com/pypiserver/pypiserver)).  

> Don't have Docker installed?  [Get Docker](https://docs.docker.com/get-docker/).

To start the server, run:

```sh
docker run -d -p 80:8080 pypiserver/pypiserver:v1.4.2 -P . -a . /data/packages
```

> The `-P .` and `-a .` flags disable authentication for everything in `pypiserver` so we don't need to worry about it in this workshop.  Never run it this way in a real scenario.

When the command is finished, navigate to http://localhost:80 to see the server running.  If you click on one of the links to the package index, you can see it starts out empty.

### Publishing Using Twine

`twine` ([GitHub](https://github.com/pypa/twine)) is a [recommended](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) tool used to help publish packages to Python repositories.  It has better security features than basic Python packaging through verified HTTPS connections and package signing, and provides publishing as a separate step. 

Let's install `twine`.  In the virtual environment for this repository, run the following command:

```sh
python -m pip install --upgrade twine
```

Next we'll publish our package.  We'll run the upload step with the `--verbose` flag in case there are any errors.  In the virtual environment for this repository, run the following command:

```sh
python -m twine upload --verbose --repository-url http://localhost:80 dist/* 
```

The command will prompt you for a username and password, you can keep these blank and press enter.

If everything was successful, you should see two upload progress bars.  Note that if you try to upload it again, it'll return a `409 Conflict` response: by default `pypiserver` does not allow overwriting packages.

Now navigate to the simple package index at http://localhost:80/simple/.  You should see the `distance-matrix` package in the index.

### Installing From the Local Server

Now let's try installing our package we just uploaded.  To start, let's make a scratch virtual environment so we don't modify the main one in our workspace.

For kicks, let's use the _other_ common naming convention for virtual environments: `.venv`.  Run the commands:

```sh
python -m venv .venv
source .venv/Scripts/activate
```

To be sure you're in the right (clean) environment you can run `pip list` and make sure you only see `pip` and `setuptools`.

Now let's install the package:

```sh
pip install --index-url http://localhost:80/simple/ distance-matrix
```

If all went well, you should see the line:

```sh
Successfully installed distance-matrix-0.0.1
```

For proof, we can enter the Python interpreter and import the library:

```py
from distance_matrix.models.coordinates import Coordinates
c = Coordinates(40, 180)
```

Finally, exit the interpreter and re-activate our original env:

```sh
source .env/Scripts/activate
```

You can then delete the scratch environment at `.env`.

## Automating With Tox

`tox` ([GitHub](https://github.com/tox-dev/tox)) is a development automation tool that can help with many common Python tasks.  It's especially useful for testing packages against multiple Python versions, interpreters, and package dependencies.

`tox` also runs tests against a packaged and installed version of your code, so it can detect packaging problems as well.

> Another popular option for automation is `make`.  You can also combine the two, running tox commands through a `makefile`, if you like the capabilities of `tox` but prefer the interface of `make`.

To start, let's install `tox`.  In the virtual environment for this repository, run the following command:

```sh
python -m pip install tox
```

Then simply run:

```sh
tox
```

Note that:
- `tox` caches the virtual environment used, so subsequent runs should be much faster.
- However, if you change dependencies, you'll want to force the environment to be recreated.  You can do that with the `--recreate` [flag](https://tox.wiki/en/3.24.5/example/basic.html?highlight=recreate#forcing-re-creation-of-virtual-environments).

### Analysis Environments

In topic 2, we covered many different forms of static code analysis.  We can use `tox` is to bring together automation for these different tools.

Recall that we created a `dev-requirements.txt` file based on the tools we added.  Let's create a new environment in our `tox.ini` file that will run these tools for us.  Copy and paste the following section into the bottom of `tox.ini`:

```ini
[testenv:lint]
skip_install = true
deps =
  -r dev-requirements.txt

commands =
  flake8 src tests
  isort src tests --check --diff
  black src tests --check --diff
```

Note how we can use the `dev-requirements` file we created earlier as one way to specify dependencies.

Then run the environment with:

```sh
tox -e lint
```

Note how for linting, we skipped the installation of the package with `skip_install = true`.  It's not useful to build and install an actual package in order to fix code style errors.  That's _not_ the case with type checkers like `mypy`, since they need to understand the types from dependencies.

We can create another environment for `mypy`:

```ini
[testenv:types]
deps =
  pytest
  mypy

commands =
  mypy src tests
```

Finally, we can chain all of these together by adding them to the `envlist`:

```ini
envlist = lint,types,py38
```

Now running `tox` alone will run all of the environments in sequence.

### Dev Environment
We can also use `tox` to create our development virtual environment.  Consider the following `tox` environment:

```ini
[testenv:dev]
envdir = {posargs:.venv}
recreate = True
deps =
    {[testenv]deps}
    {[testenv:lint]deps}
    {[testenv:types]deps}
download = True
usedevelop = True
commands =
    python --version
```

In the environment above we:
- Place it by default in the .venv folder (with the option to pass positional args instead)
- Recreate the full environment every time (no caching)
- Install the deps of all our other environments
- Use the [`download` flag](https://tox.wiki/en/latest/config.html#conf-download) to upgrade basic Python tools to latest
- Use the [`usedevelop` flag](https://tox.wiki/en/latest/config.html#conf-usedevelop): our source code is still "installed" into the environment but using symbolic links to the source files, not a packaged build

This means the entire setup for our development virtual environment is created with:

```sh
python -m pip install tox
tox -e dev
source .venv/Scripts/activate
```

### Other Examples

Many open source projects use `tox` to automate testing against multiple Python versions or dependencies.  A great example of `tox` usage is in `twine`.  Check out:
- The structure of the `twine` [`tox.ini` file](https://github.com/pypa/twine/blob/main/tox.ini)
- The commands to run in the `twine` [contributing guide](https://twine.readthedocs.io/en/latest/contributing.html)

Most core [Python Packaging Authority libraries](https://github.com/pypa) take advantage of `tox` as well.