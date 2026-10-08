"""Municipality endpoints, covering municipalities and sub-municipalities."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.use_cases.municipalities import ListMunicipalities
from app.domain.entities.municipality import MunicipalityType
from app.domain.filters import MunicipalityFilter
from app.domain.repositories.municipality_repository import MunicipalityRepository
from app.presentation.api.v1.dependencies import get_municipality_repository
from app.presentation.api.v1.params import (
    CityCodeFilter,
    Pagination,
    ProvinceCodeFilter,
    PsgcCodeFilter,
    RegionCodeFilter,
)
from app.presentation.api.v1.schemas.common import PaginatedResponse
from app.presentation.api.v1.schemas.municipality import MunicipalityResponse

router = APIRouter(prefix="/municipalities", tags=["municipalities"])

Repository = Annotated[MunicipalityRepository, Depends(get_municipality_repository)]
TypeFilter = Annotated[
    MunicipalityType | None,
    Query(description="Return only municipalities or only sub-municipalities"),
]


@router.get("", response_model=PaginatedResponse[MunicipalityResponse])
async def list_municipalities(
    repository: Repository,
    pagination: Pagination,
    psgc_code: PsgcCodeFilter = None,
    type: TypeFilter = None,
    region_code: RegionCodeFilter = None,
    province_code: ProvinceCodeFilter = None,
    city_code: CityCodeFilter = None,
) -> PaginatedResponse[MunicipalityResponse]:
    filters = MunicipalityFilter(
        psgc_code=psgc_code,
        type=type,
        region_code=region_code,
        province_code=province_code,
        city_code=city_code,
    )
    page = await ListMunicipalities(repository).execute(filters, pagination)
    return PaginatedResponse[MunicipalityResponse].from_page(
        page,
        message="Municipalities retrieved successfully",
        serialize=MunicipalityResponse.model_validate,
    )
