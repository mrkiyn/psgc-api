"""City endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.use_cases.cities import ListCities
from app.domain.entities.city import CityClass
from app.domain.filters import CityFilter
from app.domain.repositories.city_repository import CityRepository
from app.presentation.api.v1.dependencies import get_city_repository
from app.presentation.api.v1.params import (
    Pagination,
    ProvinceCodeFilter,
    PsgcCodeFilter,
    RegionCodeFilter,
)
from app.presentation.api.v1.schemas.city import CityResponse
from app.presentation.api.v1.schemas.common import PaginatedResponse

router = APIRouter(prefix="/cities", tags=["cities"])

Repository = Annotated[CityRepository, Depends(get_city_repository)]
CityClassFilter = Annotated[
    CityClass | None,
    Query(
        description=(
            "Return only cities of this class: HUC (highly urbanized), "
            "ICC (independent component), or CC (component)"
        ),
    ),
]


@router.get("", response_model=PaginatedResponse[CityResponse])
async def list_cities(
    repository: Repository,
    pagination: Pagination,
    psgc_code: PsgcCodeFilter = None,
    city_class: CityClassFilter = None,
    region_code: RegionCodeFilter = None,
    province_code: ProvinceCodeFilter = None,
) -> PaginatedResponse[CityResponse]:
    filters = CityFilter(
        psgc_code=psgc_code,
        city_class=city_class,
        region_code=region_code,
        province_code=province_code,
    )
    page = await ListCities(repository).execute(filters, pagination)
    return PaginatedResponse[CityResponse].from_page(
        page,
        message="Cities retrieved successfully",
        serialize=CityResponse.model_validate,
    )
