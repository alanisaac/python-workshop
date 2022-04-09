# Abstractions

Many object oriented languages have the concept of an **interface**: a pure contract or specification for a set of class members with no implementation.  In Python, these contracts can be represented by **abstract base classes**, or `ABC`s.

```py
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_noise(self) -> None:
        raise NotImplementedError

class Dog(Animal):
    def make_noise(self) -> None:
        print("Bark!")
```

The `@abstractmethod` decorator above indicates the `make_noise` method must be overriden by class inheritors.  Notably, enforcement of abstract methods is done at class instantiation time, not at definition time.  For example, if we try to create the `Dog` class without the `make_noise` function, Python will only complain when we try to _create_ a `Dog()` object:

```py
>>> class Animal(ABC):
...     @abstractmethod
...     def make_noise(self) -> None:
...         raise NotImplementedError
...
>>> class Dog(Animal):
...     pass
...
>>> d = Dog()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Can't instantiate abstract class Dog with abstract methods make_noise
```

Type checkers like `mypy`, however, can check for this condition as well:

```sh
mypy docs/module-2/animals.py
docs\module-2\animals.py:11: error: Cannot instantiate abstract class "Dog" with abstract attribute "make_noise"
Found 1 error in 1 file (checked 1 source file)
```

> Extension: try removing the line `d = Dog()` in `animals.py` and run `mypy` again.  Note how it does not complain without the instantiation line.  Why not?

## Protocols

Another characteristic of typing in Python is that it supports **duck typing**.  That is, so long as objects share the same properties, they can be treated the same way (e.g. if it looks like a duck and quacks like a duck...).  Take the following example:

```py
class Dog:
    def make_noise(self) -> None:
        print("Bark!")

class Car:
    def make_noise(self) -> None:
        print("Honk!")

def make_noise(thing):
    thing.make_noise()

dog = Dog()
car = Car()

make_noise(dog)
make_noise(car)
```

Note how `Dog` and `Car` do not share a common inherited type, but can both be used in the `make_noise` function.  But how would we type hint the `thing` argument?

In Python, the **Protocol** ([PEP-544](https://peps.python.org/pep-0544/)) is used to represent structural subtyping (or duck typed) scenarios.

```py
from typing import Protocol

class NoiseMaker(Protocol):
    def make_noise(self) -> None:
        ...
```

We can use `NoiseMaker` to type the `thing` argument above.

> How else could we type hint the `thing` argument?  Another option is to use a **Union** type:
> 
> ```py
> def make_noise(thing: Union[Car, Dog]) -> None:
>     thing.make_noise()
> ```
> 
> However, this limits the `thing` argument to only `Car` and `Dog` and would need to be changed for any new noise makers.  The choice can depend on the purpose of the function at hand.

ABCs and protocols have different behaviors with static type checkers.  Whereas ABCs will error on construction of the concrete class if methods are not implemented, Protocols will error where they are used.  Using our `NoiseMaker` protocol as an example:

```py
from typing import Protocol

class NoiseMaker(Protocol):
    def make_noise(self) -> None:
        ...

class SeaCucumber:
    pass

def make_noise(thing: NoiseMaker) -> None:
    thing.make_noise()

sea_cucumber = SeaCucumber() # an ABC will error here
make_noise(sea_cucumber) # a protocol will error here
```

For that reason, if you subscribe to [fail fast](https://en.wikipedia.org/wiki/Fail-fast) principles in systems design, ABCs might typically be a better choice, as they error earlier than protocols.

> Note that you can inherit protocols as well, where they _act like_ ABCs.  The `Protocol` base class must be [explicitly present](https://mypy.readthedocs.io/en/stable/protocols.html#defining-subprotocols-and-subclassing-protocols) in order for a class to be considered a protocol.

However, there are a few cases where protocols are more useful:

1. Protocols can be used to create implicit interfaces for types you do not control.  For example, if you import a library that provides a concrete `Dog` class, you can use a protocol when type hinting to allow exchanging your own implementation:
    ```py
    from canines import Dog

    class NoiseMaker(Protocol):
        def make_noise(self) -> None:
            ...

    class MyDog:
        def make_noise(self) -> None:
            print("Woof!")

    def make_noise(thing: NoiseMaker) -> None
        thing.make_noise()
    ```

2. Protocols are also useful for type hinting functions as arguments.  For example, consider the following use case where we want to choose how to format strings before printing them:
    ```py
    def format_uppercase(s: str, prefix: str = '_') -> str:
        return (prefix + s).upper()
    
    def format_lowercase(s: str, prefix: str = '_') -> str:
        return (prefix + s).lower()

    def print_string(s: str, formatter: ...) -> None:
        formatted = formatter(s)
        print(formatted)
    ```

    How would we type hint the `formatter` argument?  One option is to use `typing.Callable`, which lets us type hint functions:

    ```py
    from typing import Callable

    def print_string(s: str, formatter: Callable[[str, str], str]) -> None:
        formatted = formatter(s)
        print(formatted)
    ```

    Notably, that provides little information about the meaning of each `str` argument, or the fact that `prefix` has a default.  Using a **callback protocol** ([docs](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)), we can improve this type hint:

    ```py
    from typing import Callable

    class Formatter(Protocol):
        def __call__(self, s: str, prefix: str = '_') -> str:
            ...
    
    def print_string(s: str, formatter: Formatter) -> None:
        formatted = formatter(s)
        print(formatted)
    ```

## Collection Abstractions

As part of SOLID design practices, it's common to [depend on abstractions](https://en.wikipedia.org/wiki/Dependency_inversion_principle) rather than details.  Collection classes like `List` and `Dict` are no different.

Python offers several useful generic collection abstractions in either the `typing` module (`<= py3.8`) or the `collections.abc` module (`> py3.9`):

See https://docs.python.org/3/library/typing.html#abstract-base-classes
```sh
Container  # has the __contains__() method
Iterable  # has the __iter__() method, can be used in for loops

Sized  # has the __len__() method, can be used in len(sized)
Collection  # a sized iterable

Sequence  # a read-only sequence (ordered collection)
MutableSequence  # a mutable sequence

Set (typing.AbstractSet)  # a read-only set (hashed collection)
MutableSet  # a mutable set

Mapping  # a read-only mapping (hashed key-value pair collection)
MutableMapping  # a mutable mapping
```
