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

### Forward References

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

## Abstractions

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
mypy modules/module-2/animals.py
modules\module-2\animals.py:11: error: Cannot instantiate abstract class "Dog" with abstract attribute "make_noise"
Found 1 error in 1 file (checked 1 source file)
```

> Extension: try removing the line `d = Dog()` in `animals.py` and run `mypy` again.  Note how it does not complain without the instantiation line.  Why not?

### Protocols

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

## Domain Modeling

In object-oriented languages like Python, it's common to create objects to represent a particular business domain.  This is a practice known as [domain modeling](https://en.wikipedia.org/wiki/Domain_model).

While there are many techniques to model domains, what this workshop will cover is common ways to code domain models in practice in Python.

### Dataclasses

With the addition of type hints and variable annotations in Python, it became possible to create simple objects with type-annotated attributes.  This would become the foundation of **dataclasses** ([PEP-557](https://peps.python.org/pep-0557/)): a concise syntax to describe classes whose primary function is to store data attributes.

Dataclasses are defined using the `@dataclass` decorator, along with annotated class attributes:

```py
from dataclasses import dataclass

@dataclass
class Coordinates:
    latitude: float
    longitude: float

c = Coordinates(42.2808, 83.7430)
```

At their most basic, dataclasses help to remove the boilerplate of creating `__init__` methods for simple objects.  But dataclasses come with several additional features, including:

- **Immutability** through the `frozen` argument
- **Automatic equality members** including `__eq__` and `__hash__` (depending on settings)
- **Helper functions** including conversion to dicts (`asdict`) and tuples (`astuple`)

### Pydantic Models

Another popular way to create domain models is the `pydantic` library ([GitHub](https://github.com/samuelcolvin/pydantic)).  Pydantic has grown in popularity and whose use cases include embedding in popular web frameworks like FastAPI as the main mechanism for defining API models.

Pydantic models offer additional behaviors beyond dataclasses, and are particularly good for validating data and serializing data.  

> `pydantic` isn't the only library that provides additional functionality for defining domain models.  Another popular choice is the `attrs` ([GitHub](https://github.com/python-attrs/attrs)) package.

For example, say we want our previous coordinates class to be an [always-valid entity](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-model-layer-validations).  Latitudes must be between -90 and 90 degrees, while longitudes must be between -180 and 180 degrees.  With a Pydantic model, we can define our `Coordinates` class as:

```py
from pydantic import BaseModel, validator

class Coordinates(BaseModel):
    latitude: float
    longitude: float

    @validator('latitude')
    def latitude_must_be_valid(cls, v: float) -> float:
        if -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90 inclusive')
        return v

    @validator('longitude')
    def longitude_must_be_valid(cls, v: float) -> float:
        if -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180 inclusive')
        return v
```

When creating an instance of `Coordinates` that violates these validations, a Pydantic `ValidationError` will be raised.  To see the output, run:

```py
python ./modules/module-2/coordinates.py
```

Similarly to dataclasses, Pydantic models support creating dictionaries with `.dict()`, but also have the ability to serialize to JSON directly with `.json()`.

### "Named" Objects

It's not uncommon when working with Python codebases to work with models that use `Tuple` or `Dict` objects as data models.  After all, Python makes working with these structues as data models incredibly easy, and they are perfectly valid ways of passing data around.

Sometimes, however, you may find that for readability purposes or the ability to validate type correctness, you'd like to convert these to objects with attribute names and types.  Creating new classes for these models can be difficult, if they are instantiated and passed around in many places.

In this situtuation, Python offers a couple useful types for slowly migrating `Tuple`s `Dict`s and to "named" objects:

`NamedTuple` is an object that allows you to give `Tuple`s semantic information.  For example, suppose we had initially defined our Coordinates class using a basic tuple of `(lat, long)`:

```py
def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    # do some math with p1[0], p1[1], p2[0], p2[1]
    ...

ann_arbor = (42.2808, -83.7430)
pleasant_grove = (40.3641, -111.7385)
d = distance(ann_arbor, pleasant_grove)
```

Converting this code to a `Coordinates` class would give us semantic meaning to `p1[0]` and `p1[1]`, plus type hinting.  But that conversion means changing both how the structure is constructed and how its values are accessed.  As an interim step, you can more easily create a `NamedTuple` without having to change access:

```py
from typing import NamedTuple

class Coordinates(NamedTuple):
    latitude: float
    longitude: float
```

`TypedDict` ([PEP-589](https://peps.python.org/pep-0589/)) is the equivalent for dictionaries.  Suppose we have existing code that represents our coordinates as dictionaries instead:

```py
def distance(p1: Dict[str, float], p2: Dict[str, float]) -> float:
    # do some math with p1['lat'], p1['lon'], p2['lat'], p2['lon']
    ...

ann_arbor = {
    'lat': 42.2808,
    'lon': -83.7430,
}
pleasant_grove = {
    'lat': 40.3641, 
    'lon': -111.7385,
)
d = distance(ann_arbor, pleasant_grove)
```

The existing code above uses dictionaries as data models, but assumes a certain structure for them (a fixed set of keys).  Again, we could replace them with classes, but that would change how values are accessed.  An interim step is to use a `TypedDict`:

```py
from typing import TypedDict

class Coordinates(TypedDict):
    lat: float
    lon: float
```
