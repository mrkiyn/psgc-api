"""Region entity."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Region:
    psgc_code: str
    name: str
    correspondence_code: str | None
    population: int | None
