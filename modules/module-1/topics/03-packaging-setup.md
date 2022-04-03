# Packaging Setup

In the Python ecosystem, there are multiple ways to create and manage packages.  In this workshop, we'll cover `pip`, but `poetry` (https://python-poetry.org/) and `flit` (https://flit.readthedocs.io/en/latest/) are other options.


## Package Creation

The Python Packaging Authority (PyPA) has good documentation on how to [create packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/).  What follows is an abbreviated and adapted version of that tutorial.

Note that there are two things in the Python ecosystem called "packages":

- **Import packages** ([glossary](https://packaging.python.org/en/latest/glossary/#term-Import-Package)) are collections of modules.  _Essentially_, a folder with an `__init__.py` file.
- **Distribution packages** ([glossary](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)) are archived files that you publish and install.  A Python distribution package generally contains one or more import packages.

For this workshop we'll refer to both as "package" but clarify if the type can't be inferred from context.

### Important Files

- `pyproject.toml` ([link](../../../pyproject.toml)) contains metadata about the build of your project, like the packages necessary for a build and the build system to use.
- `setup.cfg` ([link](../../../setup.cfg)) contains metadata describing the distribution package to build, like the name, version, and where to find import packages.

Open up the links above to explore these files in more detail:  

- Note how in the `[options]` section, the distribution package is set up to `find:` import packages in the `src` folder.  This is a commonly used pattern in Python repositories called the "[`src` layout](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#using-a-src-layout)".

> In more advanced scenarios, you can create package metadata programmatically using a `setup.py` file instead of `setup.cfg`.  Best practice is to do this only when absolutely necessary, so it won't be covered in this workshop.  For more info, see the guide to [different metadata configurations](https://packaging.python.org/en/latest/tutorials/packaging-projects/#configuring-metadata).

### Defining Package Dependencies

Our package uses `pydantic`, but it's not listed as a dependency -- let's fix that.  Package dependencies are defined using the `install_requires` option in metadata.  Copy and paste the following into the `setup.cfg` file, under the `[options]` section:

```py
install_requires =
    pydantic >= 1.7
```

Note how we're specifying a dependency version greater than or equal to `1.7`.  Python package versioning and the syntax to specify dependency versions is defined by [PEP-440](https://peps.python.org/pep-0440/).

Later on, we'll see how to test that different versions of a dependency work with our library.

### Creating a Build

Since we have the package files already created, we can create a build.

_TODO_

## Package Publishing

### Running a Local Package Repository

Before we publish a package, we'll need a place to publish to.  For this workshop, we'll use a local pypi server run through Docker.  To start the server, run:

```sh
docker run -d -p 80:8080 pypiserver/pypiserver:v1.4.2
```

When the command is finished, navigate to http://localhost:80 to see the server running.

### Publishing Using Twine

`twine` ([GitHub](https://github.com/pypa/twine)) is a [recommended](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) tool used to help publish packages to Python repositories.  It has better security features than basic Python packaging through verified HTTPS connections and package signing, and provides publishing as a separate step. 

_TODO: Example_

## Packaging for Multiple Environments

`tox` ([GitHub](https://github.com/tox-dev/tox)) is a development automation tool that can help with many common Python tasks.  It's especially useful for testing packages against multiple Python versions, interpreters, and package dependencies.

_TODO: Example_
