"""Province use cases."""

from app.domain.entities.province import Province
from app.domain.filters import ProvinceFilter
from app.domain.pagination import Page, PageRequest
from app.domain.repositories.province_repository import ProvinceRepository


class ListProvinces:
    def __init__(self, repository: ProvinceRepository) -> None:
        self._repository = repository

    async def execute(self, filters: ProvinceFilter, page: PageRequest) -> Page[Province]:
        return await self._repository.list(filters, page)
