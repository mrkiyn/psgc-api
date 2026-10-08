"""City use cases."""

from app.domain.entities.city import City
from app.domain.filters import CityFilter
from app.domain.pagination import Page, PageRequest
from app.domain.repositories.city_repository import CityRepository


class ListCities:
    def __init__(self, repository: CityRepository) -> None:
        self._repository = repository

    async def execute(self, filters: CityFilter, page: PageRequest) -> Page[City]:
        return await self._repository.list(filters, page)
