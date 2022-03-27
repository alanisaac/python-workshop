# Type Hints

## A Brief History

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

To standardize this ecosystem, Python 3.0 introduced **annotations** ([PEP-3107](https://peps.python.org/pep-3107/)), which allowed developers to add arbitrary information to variables.  This could take many forms, such as adding descriptions to arguments:

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

## Inspecting Type Hints
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

## Forward References

When using type hints, you may encounter a situation where adding type hints would lead to either a circular dependency, or a dependency on a type that hasn't been defined yet.  In the following example, the type hint on the `factory` argument won't work, as `Factory` hasn't been defined yet:

```py
class Service:
    def __init__(self, factory: Factory):
        self.factory = factory

class Factory:
    def create_service(self) -> Service:
        return Service(self)
```

The solution is to use a different annotation instead, called a **forward reference** ([PEP-484](https://peps.python.org/pep-0484/#forward-references)).  A forward reference is defined using a string literal that eventually resolves to the correct type:

```py
class Service:
    def __init__(self, factory: 'Factory'):
        self.factory = factory

class Factory:
    def create_service(self) -> Service:
        return Service(self)
```

## Postponed Evaluation

If you find that you are using many forward references in a module, there is another alternative.  In Python 3.7, [PEP-563](https://peps.python.org/pep-0563/) introduced a special import that effectively turns all function annotations into strings:

```py
from __future__ import annotations
``` 

By using this import on a module, you no longer have to manage individual forward references.

## Missing Type Hints
Occasionally, you may find certain 3rd party libraries do not have type hints.  `requests`, for example, is a notable popular package that does not ([GitHub](https://github.com/psf/requests/issues/3855)).  In some cases, other open source developers will create type hint packages to supplement these libraries with typing stubs.

The `typeshed` library ([GitHub](https://github.com/python/typeshed)) is a popular place to find typing stubs for common Python packages.  If you can't find a stub package there that you'd like, searching for `python <library> type stubs` can often yield results.