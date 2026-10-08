"""Municipality repository protocol."""

from typing import Protocol

from app.domain.entities.municipality import Municipality
from app.domain.filters import MunicipalityFilter
from app.domain.pagination import Page, PageRequest


class MunicipalityRepository(Protocol):
    async def list(self, filters: MunicipalityFilter, page: PageRequest) -> Page[Municipality]: ...
