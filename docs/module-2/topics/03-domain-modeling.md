# Domain Modeling

In object-oriented languages like Python, it's common to create objects to represent a particular business domain.  This is a practice known as [domain modeling](https://en.wikipedia.org/wiki/Domain_model).

While there are many techniques to model domains, what this workshop will cover is common ways to code domain models in practice in Python.

## Dataclasses

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

## Pydantic Models

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
python ./docs/module-2/coordinates.py
```

Similarly to dataclasses, Pydantic models support creating dictionaries with `.dict()`, but also have the ability to serialize to JSON directly with `.json()`.

## "Named" and "Typed" Objects

It's not uncommon when working with Python codebases to work with models that use `Tuple` or `Dict` objects as data models.  After all, Python makes working with these structures as data models incredibly easy, and they are perfectly valid ways of passing data around.

Sometimes, however, you may find that for readability purposes or the ability to validate type correctness, you'd like to convert these to objects with attribute names and types.  Creating new classes for these models can be difficult, if they are instantiated and passed around in many places.

In this situation, Python offers a couple useful types for slowly migrating `Tuple`s `Dict`s and to "named" objects:

### NamedTuple
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

### TypedDict
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
