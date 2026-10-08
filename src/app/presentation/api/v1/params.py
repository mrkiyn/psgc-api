"""Shared query parameters."""

from typing import Annotated

from fastapi import Depends, Query

from app.domain.pagination import PageRequest

DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100

PSGC_CODE_PATTERN = r"^\d{10}$"

PsgcCodeFilter = Annotated[
    str | None,
    Query(
        pattern=PSGC_CODE_PATTERN,
        description="Return only the location with this 10-digit PSGC code",
        examples=["0100000000"],
    ),
]
RegionCodeFilter = Annotated[
    str | None,
    Query(
        pattern=PSGC_CODE_PATTERN,
        description="Return only locations in the region with this 10-digit PSGC code",
        examples=["0100000000"],
    ),
]
ProvinceCodeFilter = Annotated[
    str | None,
    Query(
        pattern=PSGC_CODE_PATTERN,
        description="Return only locations in the province with this 10-digit PSGC code",
        examples=["0102800000"],
    ),
]
CityCodeFilter = Annotated[
    str | None,
    Query(
        pattern=PSGC_CODE_PATTERN,
        description="Return only locations in the city with this 10-digit PSGC code",
        examples=["1380600000"],
    ),
]
MunicipalityCodeFilter = Annotated[
    str | None,
    Query(
        pattern=PSGC_CODE_PATTERN,
        description=(
            "Return only locations in the municipality or sub-municipality "
            "with this 10-digit PSGC code"
        ),
        examples=["1400101000"],
    ),
]


def _page_request(
    page: Annotated[int, Query(ge=1, description="Page number, starting at 1")] = 1,
    per_page: Annotated[
        int,
        Query(ge=1, le=MAX_PER_PAGE, description=f"Items per page (max {MAX_PER_PAGE})"),
    ] = DEFAULT_PER_PAGE,
) -> PageRequest:
    return PageRequest(page=page, per_page=per_page)


Pagination = Annotated[PageRequest, Depends(_page_request)]
