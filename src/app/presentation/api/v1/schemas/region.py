"""Region response schemas."""

from pydantic import BaseModel, ConfigDict


class RegionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    psgc_code: str
    name: str
    correspondence_code: str | None
    population: int | None
