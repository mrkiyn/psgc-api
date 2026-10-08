"""In-memory implementation of `MunicipalityRepository`, backed by the PSGC datafile."""

from collections.abc import Iterable

from app.domain.entities.municipality import Municipality
from app.domain.filters import MunicipalityFilter
from app.domain.pagination import Page, PageRequest
from app.infrastructure.repositories._filtering import matches_all


class InMemoryMunicipalityRepository:
    def __init__(self, municipalities: Iterable[Municipality]) -> None:
        self._municipalities = sorted(municipalities, key=lambda municipality: municipality.psgc_code)

    async def list(self, filters: MunicipalityFilter, page: PageRequest) -> Page[Municipality]:
        matches = [m for m in self._municipalities if _matches(m, filters)]
        return Page.slice(matches, page)


def _matches(municipality: Municipality, filters: MunicipalityFilter) -> bool:
    return matches_all(
        (
            (filters.psgc_code, municipality.psgc_code),
            (filters.type, municipality.type),
            (filters.region_code, municipality.region_code),
            (filters.province_code, municipality.province_code),
            (filters.city_code, municipality.city_code),
        )
    )
