# Programming Styles

Python is considered a multi-paradigm language, supporting object-oriented, procedural and functional programming styles.

This workshop won't cover the general differences between _all_ of these styles, but for more information, see:

- [Python Programming Styles](https://newrelic.com/blog/nerd-life/python-programming-styles)
- [Perceiving Python Programming Paradigms](https://opensource.com/article/19/10/python-programming-paradigms)
- [Progamming Paradigms in Python](https://www.geeksforgeeks.org/programming-paradigms-in-python/)


Instead, we'll focus on the differences between overarching ways to structure code in Python: through functions or objects.

Throughout this topic, we'll use two different implementations of a distance calculation formula as our example:

- **Haversine**: essentially treats the Earth as a sphere, calculates distance "as the crow flies".  Accurate, but computationally expensive (relatively speaking). 
- **Equirectangular Approximation**: essentially treats the Earth as a flat surface and uses the Pythagorean theorem to calculate distance.  Inaccurate over long distances, but computationally cheap.

The implementations of each in Python are provided below when needed.  For more on these forumulas, [see this website](https://www.movable-type.co.uk/scripts/latlong.html).

## Functional Approach

To implement the distance calculators as functions, we could do the following:

```py
from typing import Protocol
from math import radians, cos, sin, asin, sqrt, degrees, pi, atan2
from .coordinates import Coordinates

class DistanceCalculator(Protocol):
    def __call__(self, p1: Coordinates, p2: Coordinates, earth_radius_km: float = 6371.0088) -> float:
        ...

def calculate_distance_haversine(p1: Coordinates, p2: Coordinates, earth_radius_km: float = 6371.0088) -> float:
    lat1 = radians(p1.latitude)
    lng1 = radians(p1.longitude)
    lat2 = radians(p2.latitude)
    lng2 = radians(p2.longitude)

    lat = lat2 - lat1
    lng = lng2 - lng1
    a = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = earth_radius_km * c
    return d

def calculate_distance_equirectangular(p1: Coordinates, p2: Coordinates, earth_radius_km: float = 6371.0088) -> float:
    lat1 = radians(p1.latitude)
    lng1 = radians(p1.longitude)
    lat2 = radians(p2.latitude)
    lng2 = radians(p2.longitude)

    x = lng2 - lng1 * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    d = sqrt(x * x + y * y) * earth_radius_km
    return d
```

## Parametrized / Factory Function Approach

The above approach is great in isolation.  But suppose we had additional requirements to support distance calculators from APIs, say [Microsoft's Bing Maps route API](https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route).  There's a slight problem with the above approach: 
- The signature for distance calculation includes `earth_radius_km`.
- While this was a reasonable abstraction when all our calculators needed that data, web distance calculators won't need it.
- Further, they'll likely need their own parameters, like API credential information.

How can we do this with a functional approach?  The signature we _want_ looks like:

```py
class DistanceCalculator(Protocol):
    def __call__(self, p1: Coordinates, p2: Coordinates) -> float:
        ...
```

But we need to allow for data to parameterize the behavior of that function.  To do that, we can take advantage of declaring nested functions to create `Factory` functions:

```py
from typing import Protocol
from math import radians, cos, sin, asin, sqrt, degrees, pi, atan2
from .coordinates import Coordinates

class DistanceCalculator(Protocol):
    def __call__(self, p1: Coordinates, p2: Coordinates) -> float:
        ...

def haversine(earth_radius_km: float = 6371.0088) -> DistanceCalculator:
    def calculate(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = earth_radius_km * c
        return d
    
    return calculate

def equirectangular(earth_radius_km: float = 6371.0088) -> DistanceCalculator:
    def calculate(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        x = lng2 - lng1 * cos((lat1 + lat2) / 2)
        y = lat2 - lat1
        d = sqrt(x * x + y * y) * earth_radius_km
        return d

    return calculate

# signature shown just as an example of how it differs from the above calculators
def bing(credentials: ...) -> DistanceCalculator:
    ...
```

This is the approach used for the calculators in our repository

## Object Oriented Approach

We can also achieve the same characteristics as the function factory approach using objects.  To implement the distance calculators as objects, we can do the following:

```py
from abc import ABC
from math import radians, cos, sin, asin, sqrt, degrees, pi, atan2
from .coordinates import Coordinates

class DistanceCalculator(ABC):
    def calculate_distance(p1: Coordinates, p2: Coordinates) -> float:
        raise NotImplementedError()

class HaversineCalculator(DistanceCalculator):
    def __init__(
        self,
        earth_radius_km: float = 6371.0088
    ):
        self.earth_radius_km = earth_radius_km

    def calculate_distance(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        lat = lat2 - lat1
        lng = lng2 - lng1
        a = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = self.earth_radius_km * c
        return d

class EquirectangularCalculator(DistanceCalculator):
    def __init__(
        self,
        earth_radius_km: float = 6371.0088
    ):
        self.earth_radius_km = earth_radius_km

    def calculate_distance(p1: Coordinates, p2: Coordinates) -> float:
        lat1 = radians(p1.latitude)
        lng1 = radians(p1.longitude)
        lat2 = radians(p2.latitude)
        lng2 = radians(p2.longitude)

        x = lng2 - lng1 * cos((lat1 + lat2) / 2)
        y = lat2 - lat1
        d = sqrt(x * x + y * y) * self.earth_radius_km
        return d
```


## Discussion of Paradigms

An important part to consider in all of these approaches, is how we want to combine **data** (or **state**) with **behavior**.

_TODO: Discussion of paradigms_