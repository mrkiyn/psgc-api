"""Province repository protocol."""

from typing import Protocol

from app.domain.entities.province import Province
from app.domain.filters import ProvinceFilter
from app.domain.pagination import Page, PageRequest


class ProvinceRepository(Protocol):
    async def list(self, filters: ProvinceFilter, page: PageRequest) -> Page[Province]: ...
