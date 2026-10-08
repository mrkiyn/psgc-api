"""Municipality use cases."""

from app.domain.entities.municipality import Municipality
from app.domain.filters import MunicipalityFilter
from app.domain.pagination import Page, PageRequest
from app.domain.repositories.municipality_repository import MunicipalityRepository


class ListMunicipalities:
    def __init__(self, repository: MunicipalityRepository) -> None:
        self._repository = repository

    async def execute(self, filters: MunicipalityFilter, page: PageRequest) -> Page[Municipality]:
        return await self._repository.list(filters, page)
