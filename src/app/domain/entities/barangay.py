"""Barangay entity."""

from dataclasses import dataclass
from enum import StrEnum


class UrbanRural(StrEnum):
    URBAN = "U"
    RURAL = "R"


@dataclass(frozen=True, slots=True)
class Barangay:
    psgc_code: str
    name: str
    correspondence_code: str | None
    region_code: str
    province_code: str | None
    city_code: str | None
    municipality_code: str | None
    urban_rural: UrbanRural | None
    old_names: tuple[str, ...]
    population: int | None
