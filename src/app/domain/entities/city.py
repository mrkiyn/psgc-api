"""City entity."""

from dataclasses import dataclass
from enum import StrEnum


class CityClass(StrEnum):
    HIGHLY_URBANIZED = "HUC"
    INDEPENDENT_COMPONENT = "ICC"
    COMPONENT = "CC"


@dataclass(frozen=True, slots=True)
class City:
    psgc_code: str
    name: str
    correspondence_code: str | None
    city_class: CityClass
    region_code: str
    province_code: str | None
    income_classification: str | None
    is_capital: bool
    old_names: tuple[str, ...]
    population: int | None
