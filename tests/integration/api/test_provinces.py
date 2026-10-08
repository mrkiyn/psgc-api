from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.province import Province
from app.infrastructure.repositories.province_repository import InMemoryProvinceRepository
from app.main import app
from app.presentation.api.v1.dependencies import get_province_repository

ILOCOS_NORTE = Province(
    psgc_code="0102800000",
    name="Ilocos Norte",
    correspondence_code="012800000",
    region_code="0100000000",
    income_classification="1st",
    population=618850,
)
PANGASINAN = Province(
    psgc_code="0105500000",
    name="Pangasinan",
    correspondence_code="015500000",
    region_code="0100000000",
    income_classification="1st",
    population=3188540,
)
ABRA = Province(
    psgc_code="1400100000",
    name="Abra",
    correspondence_code="140100000",
    region_code="1400000000",
    income_classification="1st",
    population=246948,
)

ILOCOS_NORTE_JSON = {
    "psgc_code": "0102800000",
    "name": "Ilocos Norte",
    "correspondence_code": "012800000",
    "region_code": "0100000000",
    "income_classification": "1st",
    "population": 618850,
}
PANGASINAN_JSON = {
    "psgc_code": "0105500000",
    "name": "Pangasinan",
    "correspondence_code": "015500000",
    "region_code": "0100000000",
    "income_classification": "1st",
    "population": 3188540,
}
ABRA_JSON = {
    "psgc_code": "1400100000",
    "name": "Abra",
    "correspondence_code": "140100000",
    "region_code": "1400000000",
    "income_classification": "1st",
    "population": 246948,
}


@pytest.fixture(autouse=True)
def province_repository() -> Iterator[None]:
    provinces = InMemoryProvinceRepository([ABRA, PANGASINAN, ILOCOS_NORTE])
    app.dependency_overrides[get_province_repository] = lambda: provinces
    yield
    app.dependency_overrides.pop(get_province_repository, None)


def test_list_provinces(client: TestClient) -> None:
    response = client.get("/api/v1/provinces")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Provinces retrieved successfully",
        "data": [ILOCOS_NORTE_JSON, PANGASINAN_JSON, ABRA_JSON],
        "pagination": {"page": 1, "per_page": 20, "total": 3, "total_pages": 1},
    }


def test_filter_provinces_by_psgc_code(client: TestClient) -> None:
    body = client.get("/api/v1/provinces?psgc_code=0102800000").json()

    assert body["data"] == [ILOCOS_NORTE_JSON]
    assert body["pagination"] == {"page": 1, "per_page": 20, "total": 1, "total_pages": 1}


def test_filter_provinces_by_region_code(client: TestClient) -> None:
    body = client.get("/api/v1/provinces?region_code=0100000000").json()

    assert body["data"] == [ILOCOS_NORTE_JSON, PANGASINAN_JSON]
    assert body["pagination"] == {"page": 1, "per_page": 20, "total": 2, "total_pages": 1}


def test_filters_combine(client: TestClient) -> None:
    match = client.get("/api/v1/provinces?region_code=0100000000&psgc_code=0105500000").json()
    mismatch = client.get("/api/v1/provinces?region_code=1400000000&psgc_code=0105500000").json()

    assert match["data"] == [PANGASINAN_JSON]
    assert mismatch["data"] == []


@pytest.mark.parametrize(
    "query", ["psgc_code=0199900000", "region_code=1300000000", "region_code=9900000000"]
)
def test_filters_without_matches_return_empty_list(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/provinces?{query}")

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["pagination"] == {"page": 1, "per_page": 20, "total": 0, "total_pages": 0}


@pytest.mark.parametrize("query", ["psgc_code=0128", "region_code=01"])
def test_malformed_codes_return_422(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/provinces?{query}")

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_list_provinces_paginates(client: TestClient) -> None:
    first = client.get("/api/v1/provinces?page=1&per_page=2").json()
    second = client.get("/api/v1/provinces?page=2&per_page=2").json()

    assert first["data"] == [ILOCOS_NORTE_JSON, PANGASINAN_JSON]
    assert first["pagination"] == {"page": 1, "per_page": 2, "total": 3, "total_pages": 2}
    assert second["data"] == [ABRA_JSON]
    assert second["pagination"] == {"page": 2, "per_page": 2, "total": 3, "total_pages": 2}


def test_pagination_applies_after_filtering(client: TestClient) -> None:
    body = client.get("/api/v1/provinces?region_code=0100000000&page=2&per_page=1").json()

    assert body["data"] == [PANGASINAN_JSON]
    assert body["pagination"] == {"page": 2, "per_page": 1, "total": 2, "total_pages": 2}


def test_page_past_the_end_returns_empty_data(client: TestClient) -> None:
    response = client.get("/api/v1/provinces?page=5&per_page=2")

    assert response.status_code == 200
    assert response.json()["data"] == []
    assert response.json()["pagination"] == {"page": 5, "per_page": 2, "total": 3, "total_pages": 2}


@pytest.mark.parametrize("query", ["page=0", "per_page=0", "per_page=101", "page=abc"])
def test_invalid_pagination_returns_422(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/provinces?{query}")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["data"] is None


def test_province_detail_route_is_removed(client: TestClient) -> None:
    assert client.get("/api/v1/provinces/0102800000").status_code == 404
