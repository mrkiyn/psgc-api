"""Province response schemas."""

from pydantic import BaseModel, ConfigDict


class ProvinceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    psgc_code: str
    name: str
    correspondence_code: str | None
    region_code: str
    income_classification: str | None
    population: int | None
