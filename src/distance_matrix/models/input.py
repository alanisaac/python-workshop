from pandera import Field, SchemaModel
from pandera.typing import Series


class InputSchema(SchemaModel):
    City: Series[str] = Field()
    Latitude: Series[float] = Field(ge=-90, le=90)
    Longitude: Series[float] = Field(ge=-180, le=180)
