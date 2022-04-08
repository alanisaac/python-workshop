# Programming Styles

Python is considered a multi-paradigm language, supporting object-oriented, procedural and functional programming styles.

This workshop won't cover the general differences between _all_ of these styles, but for more information, see:

- [Python Programming Styles](https://newrelic.com/blog/nerd-life/python-programming-styles)
- [Perceiving Python Programming Paradigms](https://opensource.com/article/19/10/python-programming-paradigms)
- [Progamming Paradigms in Python](https://www.geeksforgeeks.org/programming-paradigms-in-python/)


Instead, we'll focus on the differences between two overarching ways to structure code in Python: through functions or objects.

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
    def __call__(p1: Coordinates, p2: Coordinates, earth_radius_km: float = 6371.0088) -> float:
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
    d = self.earth_radius_km * c
    return d

def calculate_distance_equirectangular(p1: Coordinates, p2: Coordinates, earth_radius_km: float = 6371.0088) -> float:
    lat1 = radians(p1.latitude)
    lng1 = radians(p1.longitude)
    lat2 = radians(p2.latitude)
    lng2 = radians(p2.longitude)

    x = lng2 - lng1 * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    d = sqrt(x * x + y * y) * self.earth_radius_km
    return d
```

## Object Oriented Approach

To implement the distance calculators as objects, we could do the following:

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

_TODO: Discussion of paradigms_