"""Barangay repository protocol."""

from typing import Protocol

from app.domain.entities.barangay import Barangay
from app.domain.filters import BarangayFilter
from app.domain.pagination import Page, PageRequest


class BarangayRepository(Protocol):
    async def list(self, filters: BarangayFilter, page: PageRequest) -> Page[Barangay]: ...
