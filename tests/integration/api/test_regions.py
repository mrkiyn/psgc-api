from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.region import Region
from app.infrastructure.repositories.region_repository import InMemoryRegionRepository
from app.main import app
from app.presentation.api.v1.dependencies import get_region_repository

NCR = Region(
    psgc_code="1300000000",
    name="National Capital Region (NCR)",
    correspondence_code="130000000",
    population=14001751,
)
NIR = Region(
    psgc_code="1800000000",
    name="Negros Island Region (NIR)",
    correspondence_code=None,
    population=4904944,
)

NCR_JSON = {
    "psgc_code": "1300000000",
    "name": "National Capital Region (NCR)",
    "correspondence_code": "130000000",
    "population": 14001751,
}
NIR_JSON = {
    "psgc_code": "1800000000",
    "name": "Negros Island Region (NIR)",
    "correspondence_code": None,
    "population": 4904944,
}


@pytest.fixture(autouse=True)
def region_repository() -> Iterator[None]:
    app.dependency_overrides[get_region_repository] = lambda: InMemoryRegionRepository([NIR, NCR])
    yield
    app.dependency_overrides.pop(get_region_repository, None)


def test_list_regions(client: TestClient) -> None:
    response = client.get("/api/v1/regions")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Regions retrieved successfully",
        "data": [NCR_JSON, NIR_JSON],
        "pagination": {"page": 1, "per_page": 20, "total": 2, "total_pages": 1},
    }


def test_filter_regions_by_psgc_code(client: TestClient) -> None:
    response = client.get("/api/v1/regions?psgc_code=1300000000")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Regions retrieved successfully",
        "data": [NCR_JSON],
        "pagination": {"page": 1, "per_page": 20, "total": 1, "total_pages": 1},
    }


def test_unknown_psgc_code_returns_empty_list(client: TestClient) -> None:
    response = client.get("/api/v1/regions?psgc_code=9900000000")

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["pagination"]["total"] == 0


@pytest.mark.parametrize("code", ["13", "abcdefghij", "13000000000"])
def test_malformed_psgc_code_returns_422(client: TestClient, code: str) -> None:
    response = client.get(f"/api/v1/regions?psgc_code={code}")

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["message"].startswith("Validation failed")
    assert body["data"] is None


@pytest.mark.parametrize("path", ["/api/v1/regions/1300000000", "/api/v1/regions/1300000000/provinces"])
def test_path_parameter_routes_are_removed(client: TestClient, path: str) -> None:
    assert client.get(path).status_code == 404
