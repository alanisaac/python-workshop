import pytest
from pydantic import ValidationError

from distance_matrix.models.coordinates import Coordinates


@pytest.mark.parametrize(
    "latitude,longitude",
    [
        (-1000, 0),
        (1000, 0),
        (0, -1000),
        (0, 1000)
    ]
)
def test_invalid_coordinates_raises_error(latitude, longitude):
    with pytest.raises(ValidationError):
        _ = Coordinates(latitude=latitude, longitude=longitude)
