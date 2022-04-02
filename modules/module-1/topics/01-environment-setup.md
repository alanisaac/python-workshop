# Environment Setup

This first topic covers how to set up your local environment for Python development, including virtual environments, and IDE settings.

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

## IDE Setup

There are many ways to work with Python code.  This workshop will cover two setup for two popular IDEs: VS Code and PyCharm.

If you prefer text editors, there are several plugins that can enhance the Python editing experience:

- [vim and Python: a match made in heaven](https://realpython.com/vim-and-python-a-match-made-in-heaven/)
- [Python Programming in Emacs](https://www.emacswiki.org/emacs/PythonProgrammingInEmacs)

### PyCharm
[PyCharm](https://www.jetbrains.com/pycharm/) is a paid IDE built by JetBrains, tailored specifically for Python development.

_TODO_

### VS Code
[VS Code](https://code.visualstudio.com/) is a free, cross-language IDE built by Microsoft.  It boasts a wide variety of plugins, which can enhance the development experience.

#### Plugins and Settings

The primary VS Code plugin you'll need for Python development is [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python).  By default, this installs Pylance, Microsoft's Python language server, as well as Jupyter.

There are many settings available with the Python plugin that can control the tools used for linting and analysis.  For the purposes of the workshop, we'll enable the following settings for the Python plugin:

- `python.formatting.provider`: choose the provider for formatting code (defaults to `autopep8`, we'll experiment with `black`)
- `python.linting.flake8Enabled`: enables `flake8` linting
- `python.linting.mypyEnabled`: enables `mypy` type checking
- `python.linting.pylintEnabled`: enables `pylint` linting

Combined, this produces a `settings.json` [file](../../../.vscode/settings.json) with:

```json
{
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.pylintEnabled": true
}
```

Other useful Python-specific plugins include:
- Additional support for static type checkers like [mypy](https://marketplace.visualstudio.com/items?itemName=matangover.mypy) and [pyright](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright&ssr=false).
- Support for [jinja templates](https://marketplace.visualstudio.com/items?itemName=samuelcolvin.jinjahtml).
- [Docstring generation](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring).
- Python [environment management](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager)

_TODO_