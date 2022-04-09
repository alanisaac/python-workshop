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

### Postponed Evaluation

If you find that you are using many forward references in a module, there is another alternative.  In Python 3.7, [PEP-563](https://peps.python.org/pep-0563/) introduced a special import that effectively turns all function annotations into strings:

```py
from __future__ import annotations
```

By using this import on a module, you no longer have to manage individual forward references.

## Other Useful Typing Constructs

### TypeVars and Generics

In order to calculate a distance matrix, we first read input in the form of a list of locations:

```csv
ann arbor, 42.279594, -83.732124
pleasant grove, 40.364118, -111.738540
boston, 42.364758, -71.067421
```

We then need to iterate the permutations of these locations to form our matrix (assuming the distance is symmetrical).

Python's `itertools` library already has a way to get `permutations`.  But for demonstrating `TypeVars`, we've written our own in the [utils module](../../../src/distance_matrix/utils.py).  But so far, we've left it untyped:

```py
def permutations(sequence):
    ...
```

> What's the drawback here?  Without the type hints, our type checker doesn't know the type of the return value, and therefore doesn't know what attributes it has.  In the [main module](../../../src/distance_matrix/main.py), on the line `distance = calculator(location_1.coordinates, location_2.coordinates)`, try changing the attribute access from `.coordinates` to `.cheese` and run `mypy` again.  You won't see any errors.


How should we add type hints?  The function doesn't care what the contents of `sequence` are -- they could be anything.  All we know is that the input is a sequence of _something_ and the output is pairs of _something_.

This is a good case to make the function generic with a **TypeVar**.  [TypeVars](https://docs.python.org/3/library/typing.html#typing.TypeVar) are used to create generic functions or classes.  Here's one way to type this function:

```py
_T = TypeVar("_T")


def permutations(sequence: Sequence[_T]) -> Iterable[Tuple[_T, _T]]:
    ...
```

> You might notice the use of the underscore in `_T` to make the `TypeVar` "private" (by convention).  Since `TypeVars` are typically not part of public APIs, it's [best practice](https://github.com/microsoft/pyright/blob/main/docs/typed-libraries.md#generic-classes-and-functions) to mark them private.

**Generics** ([docs](https://docs.python.org/3/library/typing.html#typing.Generic)) are similar, but are a way to apply a `TypeVar` to a class.  You can create your own generic by inheriting `Generic`:

```py
from typing import Generic, TypeVar


_T = TypeVar("_T")


class SortedList(Generic[_T]):
    def __getitem__(self, index: int) -> _T:
        ...
```


Collection abstractions like `Sequence` and `Iterable` above are both generics.

### Final

In Python typing, there are [three ways](https://mypy.readthedocs.io/en/latest/final_attrs.html) something can be declared **final** or "should not be modified":

- variables and attributes can be declared as constants with `Final`
- methods can be decorated with `@final` preventing them from being overridden
- classes can be decorated with `@final` preventing them being inherited

For example, let's look at the `calculators.py` module here.  We'll talk about the structure of this file later.  For now, observe how the signatures of two functions use the same default value:

```py
def haversine(earth_radius_km: float = 6371.0088) -> DistanceCalculator:
    ...
```

Seems like a good opportunity to introduce a constant.  Because we want the value to remain constant, we can mark it `Final` so `mypy` will raise an error if anyone tries to assign another value:

```py
DEFAULT_EARTH_RADIUS_KM: Final = 6371.0088
```

Note how this behaves a little differently than other type hints.  The _actual_ type is still `float`.

> Don't believe it?  There is a [special construct](https://mypy.readthedocs.io/en/stable/common_issues.html#reveal-type) called `reveal_type` that you can use to debug type hints.  Add `reveal_type(DEFAULT_EARTH_RADIUS_KM)` on the line after the constant (no import needed, `flake8` _will_ yell) and run `mypy` again.  You should see a line noting the "revealed" type as `builtins.float`.

## Missing Type Hints
Occasionally, you may find certain 3rd party libraries do not have type hints.  `requests`, for example, is a notable popular package that does not ([GitHub](https://github.com/psf/requests/issues/3855)).  In some cases, other open source developers will create type hint packages to supplement these libraries with typing stubs.

The `typeshed` library ([GitHub](https://github.com/python/typeshed)) is a popular place to find typing stubs for common Python packages.  If you can't find a stub package there that you'd like, searching for `python <library> type stubs` can often yield results.
