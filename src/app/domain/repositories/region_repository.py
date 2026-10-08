"""Region repository protocol."""

from typing import Protocol

from app.domain.entities.region import Region
from app.domain.filters import RegionFilter
from app.domain.pagination import Page, PageRequest


class RegionRepository(Protocol):
    async def list(self, filters: RegionFilter, page: PageRequest) -> Page[Region]: ...
