"""In-memory implementation of `ProvinceRepository`, backed by the PSGC datafile."""

from collections import defaultdict
from collections.abc import Iterable, Sequence

from app.domain.entities.province import Province
from app.domain.filters import ProvinceFilter
from app.domain.pagination import Page, PageRequest


class InMemoryProvinceRepository:
    def __init__(self, provinces: Iterable[Province]) -> None:
        self._provinces = sorted(provinces, key=lambda province: province.psgc_code)
        self._by_code = {province.psgc_code: province for province in self._provinces}
        self._by_region: dict[str, list[Province]] = defaultdict(list)
        for province in self._provinces:
            self._by_region[province.region_code].append(province)

    async def list(self, filters: ProvinceFilter, page: PageRequest) -> Page[Province]:
        matches: Sequence[Province] = self._provinces
        if filters.psgc_code is not None:
            province = self._by_code.get(filters.psgc_code)
            matches = [province] if province is not None else []
        if filters.region_code is not None:
            if filters.psgc_code is None:
                matches = self._by_region.get(filters.region_code, [])
            else:
                matches = [p for p in matches if p.region_code == filters.region_code]
        return Page.slice(matches, page)
