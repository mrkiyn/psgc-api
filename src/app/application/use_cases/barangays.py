"""Barangay use cases."""

from app.domain.entities.barangay import Barangay
from app.domain.filters import BarangayFilter
from app.domain.pagination import Page, PageRequest
from app.domain.repositories.barangay_repository import BarangayRepository


class ListBarangays:
    def __init__(self, repository: BarangayRepository) -> None:
        self._repository = repository

    async def execute(self, filters: BarangayFilter, page: PageRequest) -> Page[Barangay]:
        return await self._repository.list(filters, page)
