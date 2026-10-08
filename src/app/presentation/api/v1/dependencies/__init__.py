"""FastAPI dependencies that wire repositories into routers."""

from functools import cache

from app.domain.repositories.barangay_repository import BarangayRepository
from app.domain.repositories.city_repository import CityRepository
from app.domain.repositories.municipality_repository import MunicipalityRepository
from app.domain.repositories.province_repository import ProvinceRepository
from app.domain.repositories.region_repository import RegionRepository
from app.infrastructure.psgc.reader import get_dataset
from app.infrastructure.repositories.barangay_repository import InMemoryBarangayRepository
from app.infrastructure.repositories.city_repository import InMemoryCityRepository
from app.infrastructure.repositories.municipality_repository import InMemoryMunicipalityRepository
from app.infrastructure.repositories.province_repository import InMemoryProvinceRepository
from app.infrastructure.repositories.region_repository import InMemoryRegionRepository


@cache
def get_region_repository() -> RegionRepository:
    return InMemoryRegionRepository(get_dataset().regions)


@cache
def get_province_repository() -> ProvinceRepository:
    return InMemoryProvinceRepository(get_dataset().provinces)


@cache
def get_city_repository() -> CityRepository:
    return InMemoryCityRepository(get_dataset().cities)


@cache
def get_municipality_repository() -> MunicipalityRepository:
    return InMemoryMunicipalityRepository(get_dataset().municipalities)


@cache
def get_barangay_repository() -> BarangayRepository:
    return InMemoryBarangayRepository(get_dataset().barangays)
