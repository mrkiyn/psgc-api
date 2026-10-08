from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.barangay import Barangay, UrbanRural
from app.infrastructure.repositories.barangay_repository import InMemoryBarangayRepository
from app.main import app
from app.presentation.api.v1.dependencies import get_barangay_repository

AGTANGAO = Barangay(
    psgc_code="1400101001",
    name="Agtangao",
    correspondence_code="140101001",
    region_code="1400000000",
    province_code="1400100000",
    city_code=None,
    municipality_code="1400101000",
    urban_rural=UrbanRural.RURAL,
    old_names=(),
    population=2528,
)
AGBANNAWAG = Barangay(
    psgc_code="1403213001",
    name="Agbannawag",
    correspondence_code="143213001",
    region_code="1400000000",
    province_code="1403200000",
    city_code="1403213000",
    municipality_code=None,
    urban_rural=UrbanRural.URBAN,
    old_names=(),
    population=6047,
)
APUGAN_LOAKAN = Barangay(
    psgc_code="1430300001",
    name="Apugan-Loakan",
    correspondence_code="141102001",
    region_code="1400000000",
    province_code=None,
    city_code="1430300000",
    municipality_code=None,
    urban_rural=UrbanRural.URBAN,
    old_names=(),
    population=3172,
)
TONDO_BARANGAY_1 = Barangay(
    psgc_code="1380601001",
    name="Barangay 1",
    correspondence_code="133901001",
    region_code="1300000000",
    province_code=None,
    city_code="1380600000",
    municipality_code="1380601000",
    urban_rural=UrbanRural.URBAN,
    old_names=(),
    population=3119,
)
CALOOCAN_176_A = Barangay(
    psgc_code="1380100189",
    name="Barangay 176-A",
    correspondence_code=None,
    region_code="1300000000",
    province_code=None,
    city_code="1380100000",
    municipality_code=None,
    urban_rural=None,
    old_names=("Barangay 176",),
    population=48719,
)

ALL = [AGTANGAO, AGBANNAWAG, APUGAN_LOAKAN, TONDO_BARANGAY_1, CALOOCAN_176_A]


def codes(body: dict) -> list[str]:
    return [item["psgc_code"] for item in body["data"]]


@pytest.fixture(autouse=True)
def barangay_repository() -> Iterator[None]:
    repository = InMemoryBarangayRepository(ALL)
    app.dependency_overrides[get_barangay_repository] = lambda: repository
    yield
    app.dependency_overrides.pop(get_barangay_repository, None)


def test_list_barangays_sorted_by_code(client: TestClient) -> None:
    response = client.get("/api/v1/barangays")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Barangays retrieved successfully"
    assert codes(body) == ["1380100189", "1380601001", "1400101001", "1403213001", "1430300001"]
    assert body["pagination"] == {"page": 1, "per_page": 20, "total": 5, "total_pages": 1}


def test_barangay_fields(client: TestClient) -> None:
    body = client.get("/api/v1/barangays?psgc_code=1380601001").json()

    assert body["data"] == [
        {
            "psgc_code": "1380601001",
            "name": "Barangay 1",
            "correspondence_code": "133901001",
            "region_code": "1300000000",
            "province_code": None,
            "city_code": "1380600000",
            "municipality_code": "1380601000",
            "urban_rural": "U",
            "old_names": [],
            "population": 3119,
        }
    ]


def test_barangay_with_old_name_and_no_urban_rural(client: TestClient) -> None:
    item = client.get("/api/v1/barangays?psgc_code=1380100189").json()["data"][0]

    assert item["old_names"] == ["Barangay 176"]
    assert item["urban_rural"] is None
    assert item["correspondence_code"] is None


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("region_code=1400000000", ["1400101001", "1403213001", "1430300001"]),
        ("province_code=1400100000", ["1400101001"]),
        ("municipality_code=1400101000", ["1400101001"]),
        ("city_code=1403213000", ["1403213001"]),
        ("city_code=1380600000", ["1380601001"]),
        ("municipality_code=1380601000", ["1380601001"]),
        ("urban_rural=U", ["1380601001", "1403213001", "1430300001"]),
        ("urban_rural=R", ["1400101001"]),
        ("region_code=1400000000&urban_rural=U", ["1403213001", "1430300001"]),
        ("city_code=1430300000&province_code=1400100000", []),
        ("municipality_code=9999999000", []),
    ],
)
def test_filters(client: TestClient, query: str, expected: list[str]) -> None:
    response = client.get(f"/api/v1/barangays?{query}")

    assert response.status_code == 200
    assert codes(response.json()) == expected
    assert response.json()["pagination"]["total"] == len(expected)


def test_pagination_applies_after_filtering(client: TestClient) -> None:
    body = client.get("/api/v1/barangays?urban_rural=U&page=2&per_page=2").json()

    assert codes(body) == ["1430300001"]
    assert body["pagination"] == {"page": 2, "per_page": 2, "total": 3, "total_pages": 2}


@pytest.mark.parametrize(
    "query", ["urban_rural=urban", "urban_rural=u", "municipality_code=1400101", "city_code=abc"]
)
def test_invalid_filters_return_422(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/barangays?{query}")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["data"] is None
