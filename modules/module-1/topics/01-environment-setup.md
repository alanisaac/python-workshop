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

_TODO_