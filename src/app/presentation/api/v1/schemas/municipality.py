"""Municipality response schemas."""

from pydantic import BaseModel, ConfigDict

from app.domain.entities.municipality import MunicipalityType


class MunicipalityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    psgc_code: str
    name: str
    correspondence_code: str | None
    type: MunicipalityType
    region_code: str
    province_code: str | None
    city_code: str | None
    income_classification: str | None
    is_capital: bool
    old_names: list[str]
    population: int | None
