# Module 2: Coding Patterns and Practices

## Type Hints

### A Brief History

In Python, the type system has two characteristics:

- **Strongly Typed**: variables have types, and the type matters when performing operations on a variable
- **Dynamically Typed**: the type of each variable is only determined at runtime

For example, in the following function, the `value` argument could be passed any type at runtime.

```py
def print(value):
    ...
```

And though Python is dynamic, because it is strongly typed, developers would often have a need to document what each function expects.  Before Python 3, Python did not have a standardized way to express any metadata about variables.  Often, when deemed necessary, type information was expressed through doc comments:

```py
def print(value):
    """
    Prints the value.

    Args:
        value (str): The value.
    """
    ...
```

But it could also be expressed through decorators introduced in [PEP-0318](https://peps.python.org/pep-0318/).

To standardize this eecosystem, Python 3.0 introduced **annotations** ([PEP-3107](https://peps.python.org/pep-3107/)), which allowed developers to add arbitrary information to variables.  This could take many forms, such as adding descriptions to arguments:

```py
def compile(source: "something compilable",
            filename: "where the compilable thing comes from",
            mode: "is this a single statement or a suite?"):
    ...
```

But it could also be used to express the type of each argument, as well as return types:

```py
def haul(item: Haulable, *vargs: PackAnimal) -> Distance:
    ...
```

However, PEP-3107 stopped short of formalizing a definition for type annotations.  It wasn't until Python 3.5 that **type hints** were introduced ([PEP-484](https://peps.python.org/pep-0484/)), making this syntax official (as well as introducing [type comments](https://peps.python.org/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code) for Python 2 compatibility).

### Inspecting Type Hints
Annotations (and therefore type hints) can be inspected at runtime.  There are multiple ways to accomplish this:

The `inspect.signature` function returns a [Signature](https://docs.python.org/3/library/inspect.html#inspect.Signature) object that includes annotations:

```py
>>> def func(a, b: str, c: "an annotation") -> None:
...   pass
... 
>>> import inspect
>>> inspect.signature(func)
<Signature (a, b: str, c: 'an annotation') -> None>
>>> inspect.signature(func).parameters['b'].annotation
<class 'str'>
```

The typing module also has a `get_type_hints` function that more directly returns type hints.

```py
>>> def func(a, b: str, c: int) -> None:
...   pass
... 
>>> import typing
>>> typing.get_type_hints(func) 
{'b': <class 'str'>, 'c': <class 'int'>, 'return': <class 'NoneType'>}
```

Note that this method will raise an error on `'an annotation'` in the previous example, as it interprets the annotation as a **forward reference**.  We'll discuss what this means later.