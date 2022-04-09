import pytest
from pydantic import ValidationError

from distance_matrix.models.coordinates import Coordinates


@pytest.mark.parametrize(
    "latitude,longitude", [(-1000, 0), (1000, 0), (0, -1000), (0, 1000)]
)
def test_invalid_coordinates_raises_error(latitude, longitude):
    with pytest.raises(ValidationError):
        _ = Coordinates(latitude=latitude, longitude=longitude)


@pytest.mark.parametrize("latitude,longitude", [(0, 0), (90, 180), (-90, -180)])
def test_valid_coordinates_are_constructed_correctly(latitude, longitude):
    coordinates = Coordinates(latitude=latitude, longitude=longitude)

    assert coordinates.latitude == latitude
    assert coordinates.longitude == longitude
