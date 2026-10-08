"""Province endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.use_cases.provinces import ListProvinces
from app.domain.filters import ProvinceFilter
from app.domain.repositories.province_repository import ProvinceRepository
from app.presentation.api.v1.dependencies import get_province_repository
from app.presentation.api.v1.params import Pagination, PsgcCodeFilter, RegionCodeFilter
from app.presentation.api.v1.schemas.common import PaginatedResponse
from app.presentation.api.v1.schemas.province import ProvinceResponse

router = APIRouter(prefix="/provinces", tags=["provinces"])

Repository = Annotated[ProvinceRepository, Depends(get_province_repository)]


@router.get("", response_model=PaginatedResponse[ProvinceResponse])
async def list_provinces(
    repository: Repository,
    pagination: Pagination,
    psgc_code: PsgcCodeFilter = None,
    region_code: RegionCodeFilter = None,
) -> PaginatedResponse[ProvinceResponse]:
    filters = ProvinceFilter(psgc_code=psgc_code, region_code=region_code)
    page = await ListProvinces(repository).execute(filters, pagination)
    return PaginatedResponse[ProvinceResponse].from_page(
        page,
        message="Provinces retrieved successfully",
        serialize=ProvinceResponse.model_validate,
    )
