"""In-memory implementation of `BarangayRepository`, backed by the PSGC datafile."""

from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence

from app.domain.entities.barangay import Barangay
from app.domain.filters import BarangayFilter
from app.domain.pagination import Page, PageRequest
from app.infrastructure.repositories._filtering import matches_all

Key = Callable[[Barangay], str | None]

_INDEXED: dict[str, Key] = {
    "psgc_code": lambda b: b.psgc_code,
    "municipality_code": lambda b: b.municipality_code,
    "city_code": lambda b: b.city_code,
    "province_code": lambda b: b.province_code,
    "region_code": lambda b: b.region_code,
}


class InMemoryBarangayRepository:
    """Indexes barangays by every code so a filtered request only scans its smallest matching group."""

    def __init__(self, barangays: Iterable[Barangay]) -> None:
        self._barangays = sorted(barangays, key=lambda barangay: barangay.psgc_code)
        self._indexes: dict[str, dict[str, list[Barangay]]] = {}
        for field, key in _INDEXED.items():
            index: dict[str, list[Barangay]] = defaultdict(list)
            for barangay in self._barangays:
                if (value := key(barangay)) is not None:
                    index[value].append(barangay)
            self._indexes[field] = dict(index)

    async def list(self, filters: BarangayFilter, page: PageRequest) -> Page[Barangay]:
        candidates: Sequence[Barangay] = self._barangays
        for field in _INDEXED:
            wanted = getattr(filters, field)
            if wanted is not None:
                group = self._indexes[field].get(wanted, [])
                if len(group) < len(candidates):
                    candidates = group
        matches = [b for b in candidates if _matches(b, filters)]
        return Page.slice(matches, page)


def _matches(barangay: Barangay, filters: BarangayFilter) -> bool:
    return matches_all(
        (
            (filters.psgc_code, barangay.psgc_code),
            (filters.region_code, barangay.region_code),
            (filters.province_code, barangay.province_code),
            (filters.city_code, barangay.city_code),
            (filters.municipality_code, barangay.municipality_code),
            (filters.urban_rural, barangay.urban_rural),
        )
    )
