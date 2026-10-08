"""City repository protocol."""

from typing import Protocol

from app.domain.entities.city import City
from app.domain.filters import CityFilter
from app.domain.pagination import Page, PageRequest


class CityRepository(Protocol):
    async def list(self, filters: CityFilter, page: PageRequest) -> Page[City]: ...
