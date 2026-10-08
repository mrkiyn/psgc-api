"""Optional criteria for narrowing repository listings. `None` means "don't filter"."""

from dataclasses import dataclass

from app.domain.entities.barangay import UrbanRural
from app.domain.entities.city import CityClass
from app.domain.entities.municipality import MunicipalityType


@dataclass(frozen=True, slots=True)
class RegionFilter:
    psgc_code: str | None = None


@dataclass(frozen=True, slots=True)
class ProvinceFilter:
    psgc_code: str | None = None
    region_code: str | None = None


@dataclass(frozen=True, slots=True)
class CityFilter:
    psgc_code: str | None = None
    city_class: CityClass | None = None
    region_code: str | None = None
    province_code: str | None = None


@dataclass(frozen=True, slots=True)
class MunicipalityFilter:
    psgc_code: str | None = None
    type: MunicipalityType | None = None
    region_code: str | None = None
    province_code: str | None = None
    city_code: str | None = None


@dataclass(frozen=True, slots=True)
class BarangayFilter:
    psgc_code: str | None = None
    region_code: str | None = None
    province_code: str | None = None
    city_code: str | None = None
    municipality_code: str | None = None
    urban_rural: UrbanRural | None = None
