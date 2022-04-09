from dataclasses import dataclass


@dataclass
class Output:
    origin: str
    destination: str
    distance: float
