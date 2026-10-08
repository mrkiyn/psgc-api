"""Province entity."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Province:
    psgc_code: str
    name: str
    correspondence_code: str | None
    region_code: str
    income_classification: str | None
    population: int | None
