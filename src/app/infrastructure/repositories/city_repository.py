"""In-memory implementation of `CityRepository`, backed by the PSGC datafile."""

from collections.abc import Iterable

from app.domain.entities.city import City
from app.domain.filters import CityFilter
from app.domain.pagination import Page, PageRequest
from app.infrastructure.repositories._filtering import matches_all


class InMemoryCityRepository:
    def __init__(self, cities: Iterable[City]) -> None:
        self._cities = sorted(cities, key=lambda city: city.psgc_code)

    async def list(self, filters: CityFilter, page: PageRequest) -> Page[City]:
        matches = [city for city in self._cities if _matches(city, filters)]
        return Page.slice(matches, page)


def _matches(city: City, filters: CityFilter) -> bool:
    return matches_all(
        (
            (filters.psgc_code, city.psgc_code),
            (filters.city_class, city.city_class),
            (filters.region_code, city.region_code),
            (filters.province_code, city.province_code),
        )
    )
