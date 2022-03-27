# Packaging Setup

In the Python ecosystem, there are multiple ways to create and manage packages.  In this workshop, we'll cover `pip`, but `poetry` (https://python-poetry.org/) and `flit` (https://flit.readthedocs.io/en/latest/) are other options.


## Package Creation

The Python Packaging Authority (PyPA) has good documentation on how to [create packages](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

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
