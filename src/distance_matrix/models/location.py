from dataclasses import dataclass

from .coordinates import Coordinates


@dataclass
class Location:
    name: str
    coordinates: Coordinates
