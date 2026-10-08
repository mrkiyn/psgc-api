"""Municipality entity, covering both municipalities and sub-municipalities."""

from dataclasses import dataclass
from enum import StrEnum


class MunicipalityType(StrEnum):
    MUNICIPALITY = "municipality"
    SUB_MUNICIPALITY = "sub_municipality"


@dataclass(frozen=True, slots=True)
class Municipality:
    psgc_code: str
    name: str
    correspondence_code: str | None
    type: MunicipalityType
    region_code: str
    province_code: str | None
    city_code: str | None
    income_classification: str | None
    is_capital: bool
    old_names: tuple[str, ...]
    population: int | None
