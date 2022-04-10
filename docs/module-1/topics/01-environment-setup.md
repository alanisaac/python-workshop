# Environment Setup

This first topic covers how to set up your local environment for Python development, including virtual environments, and IDE settings.

![Python Environments](https://imgs.xkcd.com/comics/python_environment.png)

_[credit: xkcd](https://xkcd.com/1987/) ([CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/))_

## Python Versions

When working with Python on a project, it's important everyone is working using the same version for consistent language features and reproducibility.

`pyenv` ([GitHub](https://github.com/pyenv/pyenv)) is an important tool for managing Python versions on your system.  If you don't already have it, you can see the installation instructions at:

- `pyenv` [installation](https://github.com/pyenv/pyenv#installation) (*NIX systems)
- `pyenv-win` [installation](https://github.com/pyenv-win/pyenv-win#installation) (Windows systems)

Or simply using your system's package manager:

```sh
# win
choco install pyenv-win

# mac
brew install pyenv
```

You may need to restart any terminals or terminal-containing IDEs (VS Code, PyCharm) for `pyenv` to work.  Once installed, you can view the (many) available Python versions with:

```sh
pyenv install -l
```

For this workshop, we'll be using Python 3.8 or above.  You can install the latest version of Python 3.8 with:

```sh
pyenv install 3.8.10
```

It may take a couple of minutes to install.  Afterwords, you can set the Python version globally or locally with:

```ini
# set the version globally
pyenv global 3.8.10

# OR set the version locally
pyenv local 3.8.10

python --version
```

> Note that if you're not seeing the Python version change with `pyenv` on Windows, you might need to adjust your `PATH`.  Make sure your system Python is not taking precedence.  See also this [StackOverflow](https://stackoverflow.com/a/67986712) post.

## Virtual Environments

In Python, it's common best practice to use **virtual environments**: isolated environments for Python projects.  But why is that isolation needed in the first place?

There are a couple places that Python resolves packages from:

For system-level packages like `email`, `http`, `logging`, and others, you can find them in the `sys.prefix` directory:

```py
>>> import sys
>>> sys.prefix
'C:\\Users\\alanisaac\\.pyenv\\pyenv-win\\versions\\3.8.10'
```

Additional packages installed with tools like `pip` will install into a **site packages** directory.  You can find this directory at:

```py
>>> import site
>>> site.getsitepackages()
['C:\\Users\\alanisaac\\.pyenv\\pyenv-win\\versions\\3.8.10', 'C:\\Users\\alanisaac\\.pyenv\\pyenv-win\\versions\\3.8.10\\lib\\site-packages']
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

## IDE Setup

There are many ways to work with Python code.  This workshop will cover two setup for two popular IDEs: VS Code and PyCharm.

If you prefer text editors, there are several plugins that can enhance the Python editing experience:

- [vim and Python: a match made in heaven](https://realpython.com/vim-and-python-a-match-made-in-heaven/)
- [Python Programming in Emacs](https://www.emacswiki.org/emacs/PythonProgrammingInEmacs)

### PyCharm
[PyCharm](https://www.jetbrains.com/pycharm/) is a paid IDE built by JetBrains (with a free community edition), tailored specifically for Python development.

#### Settings

Most IDE settings are a matter of personal preference.  However, it's a good idea to look at the [Python Integrated Tools](https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html) settings page.  This is how PyCharm determines the default test runner and the docstring format (both of which we'll discuss later in this workshop).

PyCharm should be able to autodetect the correct default test runner from the repository.  However, you may want to set the docstring format if it is different than the default.  This will determine how PyCharm autofills docstrings.  You can try it out by documenting one of the functions in the `Coordinates` class [in this workshop](../../../src/distance_matrix/models/coordinates.py).

#### Plugins & External Tools

PyCharm has a [plugin library](https://plugins.jetbrains.com/pycharm_ce) with plugins for various additional features.  This includes support for additional file types, integration with tools like Docker, and many more.  PyCharm is specifically tailored around Python development, so there aren't any required plugins to download.

PyCharm lets you create your own macro buttons using the **external tools** feature.  For example, you could create a macro to run code formatting through a specific formatter.  See more about:

- [External tools](https://www.jetbrains.com/help/pycharm/configuring-third-party-tools.html)
- [An example of integrating `black` as an external tool](https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea)


### VS Code
[VS Code](https://code.visualstudio.com/) is a free, cross-language IDE built by Microsoft.  It boasts a wide variety of plugins, which can enhance the development experience.

#### Plugins and Settings

The primary VS Code plugin you'll need for Python development is [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python).  By default, this installs Pylance, Microsoft's Python language server, as well as Jupyter.

There are many settings available with the Python plugin that can control the tools used for linting and analysis.  For the purposes of the workshop, we'll enable the following settings for the Python plugin:

- `python.formatting.provider`: choose the provider for formatting code (defaults to `autopep8`, we'll experiment with `black`)
- `python.linting.flake8Enabled`: enables `flake8` linting
- `python.linting.mypyEnabled`: enables `mypy` type checking
- `python.testing.pytestEnabled`: enables `pytest` as our test runner

Combined, this produces a `settings.json` [file](../../../.vscode/settings.json) with:

```json
{
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true
}
```

Other useful Python-specific plugins include:
- Additional support for static type checkers like [mypy](https://marketplace.visualstudio.com/items?itemName=matangover.mypy) and [pyright](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright&ssr=false) (not strictly needed with the `python` plugin settings)
- Support for [jinja templates](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml).
- [Docstring generation](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring).
- Python [environment management](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager)
- [Spellchecking](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) (very useful for writing all the docs for this workshop)
