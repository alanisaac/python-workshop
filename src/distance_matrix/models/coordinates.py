from pydantic import BaseModel, validator


class Coordinates(BaseModel):
    latitude: float
    longitude: float

    @validator('latitude')
    def latitude_must_be_valid(cls, v: float) -> float:
        if -90 <= v <= 90:
            return v
        raise ValueError('Latitude must be between -90 and 90 inclusive')

    @validator('longitude')
    def longitude_must_be_valid(cls, v: float) -> float:
        if -180 <= v <= 180:
            return v
        raise ValueError('Longitude must be between -180 and 180 inclusive')
