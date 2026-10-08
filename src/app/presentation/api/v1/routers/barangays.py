"""Barangay endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.use_cases.barangays import ListBarangays
from app.domain.entities.barangay import UrbanRural
from app.domain.filters import BarangayFilter
from app.domain.repositories.barangay_repository import BarangayRepository
from app.presentation.api.v1.dependencies import get_barangay_repository
from app.presentation.api.v1.params import (
    CityCodeFilter,
    MunicipalityCodeFilter,
    Pagination,
    ProvinceCodeFilter,
    PsgcCodeFilter,
    RegionCodeFilter,
)
from app.presentation.api.v1.schemas.barangay import BarangayResponse
from app.presentation.api.v1.schemas.common import PaginatedResponse

router = APIRouter(prefix="/barangays", tags=["barangays"])

Repository = Annotated[BarangayRepository, Depends(get_barangay_repository)]
UrbanRuralFilter = Annotated[
    UrbanRural | None,
    Query(description="Return only urban (U) or rural (R) barangays"),
]


@router.get("", response_model=PaginatedResponse[BarangayResponse])
async def list_barangays(
    repository: Repository,
    pagination: Pagination,
    psgc_code: PsgcCodeFilter = None,
    region_code: RegionCodeFilter = None,
    province_code: ProvinceCodeFilter = None,
    city_code: CityCodeFilter = None,
    municipality_code: MunicipalityCodeFilter = None,
    urban_rural: UrbanRuralFilter = None,
) -> PaginatedResponse[BarangayResponse]:
    filters = BarangayFilter(
        psgc_code=psgc_code,
        region_code=region_code,
        province_code=province_code,
        city_code=city_code,
        municipality_code=municipality_code,
        urban_rural=urban_rural,
    )
    page = await ListBarangays(repository).execute(filters, pagination)
    return PaginatedResponse[BarangayResponse].from_page(
        page,
        message="Barangays retrieved successfully",
        serialize=BarangayResponse.model_validate,
    )
