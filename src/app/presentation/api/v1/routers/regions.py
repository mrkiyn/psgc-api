"""Region endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.use_cases.regions import ListRegions
from app.domain.filters import RegionFilter
from app.domain.repositories.region_repository import RegionRepository
from app.presentation.api.v1.dependencies import get_region_repository
from app.presentation.api.v1.params import Pagination, PsgcCodeFilter
from app.presentation.api.v1.schemas.common import PaginatedResponse
from app.presentation.api.v1.schemas.region import RegionResponse

router = APIRouter(prefix="/regions", tags=["regions"])

Repository = Annotated[RegionRepository, Depends(get_region_repository)]


@router.get("", response_model=PaginatedResponse[RegionResponse])
async def list_regions(
    repository: Repository,
    pagination: Pagination,
    psgc_code: PsgcCodeFilter = None,
) -> PaginatedResponse[RegionResponse]:
    page = await ListRegions(repository).execute(RegionFilter(psgc_code=psgc_code), pagination)
    return PaginatedResponse[RegionResponse].from_page(
        page,
        message="Regions retrieved successfully",
        serialize=RegionResponse.model_validate,
    )
