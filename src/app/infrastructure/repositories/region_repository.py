"""In-memory implementation of `RegionRepository`, backed by the PSGC datafile."""

from collections.abc import Iterable, Sequence

from app.domain.entities.region import Region
from app.domain.filters import RegionFilter
from app.domain.pagination import Page, PageRequest


class InMemoryRegionRepository:
    def __init__(self, regions: Iterable[Region]) -> None:
        self._regions = sorted(regions, key=lambda region: region.psgc_code)
        self._by_code = {region.psgc_code: region for region in self._regions}

    async def list(self, filters: RegionFilter, page: PageRequest) -> Page[Region]:
        matches: Sequence[Region] = self._regions
        if filters.psgc_code is not None:
            region = self._by_code.get(filters.psgc_code)
            matches = [region] if region is not None else []
        return Page.slice(matches, page)
