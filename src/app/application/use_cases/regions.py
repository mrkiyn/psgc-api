"""Region use cases."""

from app.domain.entities.region import Region
from app.domain.filters import RegionFilter
from app.domain.pagination import Page, PageRequest
from app.domain.repositories.region_repository import RegionRepository


class ListRegions:
    def __init__(self, repository: RegionRepository) -> None:
        self._repository = repository

    async def execute(self, filters: RegionFilter, page: PageRequest) -> Page[Region]:
        return await self._repository.list(filters, page)
