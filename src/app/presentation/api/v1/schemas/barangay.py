"""Barangay response schemas."""

from pydantic import BaseModel, ConfigDict

from app.domain.entities.barangay import UrbanRural


class BarangayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    psgc_code: str
    name: str
    correspondence_code: str | None
    region_code: str
    province_code: str | None
    city_code: str | None
    municipality_code: str | None
    urban_rural: UrbanRural | None
    old_names: list[str]
    population: int | None
