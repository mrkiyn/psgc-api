from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.municipality import Municipality, MunicipalityType
from app.infrastructure.repositories.municipality_repository import InMemoryMunicipalityRepository
from app.main import app
from app.presentation.api.v1.dependencies import get_municipality_repository

BANGUED = Municipality(
    psgc_code="1400101000",
    name="Bangued",
    correspondence_code="140101000",
    type=MunicipalityType.MUNICIPALITY,
    region_code="1400000000",
    province_code="1400100000",
    city_code=None,
    income_classification="1st",
    is_capital=True,
    old_names=(),
    population=48331,
)
BOLINEY = Municipality(
    psgc_code="1400102000",
    name="Boliney",
    correspondence_code="140102000",
    type=MunicipalityType.MUNICIPALITY,
    region_code="1400000000",
    province_code="1400100000",
    city_code=None,
    income_classification="3rd",
    is_capital=False,
    old_names=(),
    population=3778,
)
ALFONSO_LISTA = Municipality(
    psgc_code="1402701000",
    name="Alfonso Lista",
    correspondence_code="142701000",
    type=MunicipalityType.MUNICIPALITY,
    region_code="1400000000",
    province_code="1402700000",
    city_code=None,
    income_classification="2nd",
    is_capital=False,
    old_names=("Potia",),
    population=33000,
)
TONDO = Municipality(
    psgc_code="1380601000",
    name="Tondo I/II",
    correspondence_code="133901000",
    type=MunicipalityType.SUB_MUNICIPALITY,
    region_code="1300000000",
    province_code=None,
    city_code="1380600000",
    income_classification=None,
    is_capital=False,
    old_names=(),
    population=637942,
)
PATEROS = Municipality(
    psgc_code="1381701000",
    name="Pateros",
    correspondence_code="137606000",
    type=MunicipalityType.MUNICIPALITY,
    region_code="1300000000",
    province_code=None,
    city_code=None,
    income_classification="1st",
    is_capital=False,
    old_names=(),
    population=67319,
)

ALL = [BANGUED, BOLINEY, ALFONSO_LISTA, TONDO, PATEROS]


def codes(body: dict) -> list[str]:
    return [item["psgc_code"] for item in body["data"]]


@pytest.fixture(autouse=True)
def municipality_repository() -> Iterator[None]:
    repository = InMemoryMunicipalityRepository(ALL)
    app.dependency_overrides[get_municipality_repository] = lambda: repository
    yield
    app.dependency_overrides.pop(get_municipality_repository, None)


def test_list_municipalities_sorted_by_code(client: TestClient) -> None:
    response = client.get("/api/v1/municipalities")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Municipalities retrieved successfully"
    assert codes(body) == ["1380601000", "1381701000", "1400101000", "1400102000", "1402701000"]
    assert body["pagination"] == {"page": 1, "per_page": 20, "total": 5, "total_pages": 1}


def test_municipality_fields(client: TestClient) -> None:
    body = client.get("/api/v1/municipalities?psgc_code=1402701000").json()

    assert body["data"] == [
        {
            "psgc_code": "1402701000",
            "name": "Alfonso Lista",
            "correspondence_code": "142701000",
            "type": "municipality",
            "region_code": "1400000000",
            "province_code": "1402700000",
            "city_code": None,
            "income_classification": "2nd",
            "is_capital": False,
            "old_names": ["Potia"],
            "population": 33000,
        }
    ]


def test_sub_municipality_fields(client: TestClient) -> None:
    body = client.get("/api/v1/municipalities?psgc_code=1380601000").json()

    assert body["data"] == [
        {
            "psgc_code": "1380601000",
            "name": "Tondo I/II",
            "correspondence_code": "133901000",
            "type": "sub_municipality",
            "region_code": "1300000000",
            "province_code": None,
            "city_code": "1380600000",
            "income_classification": None,
            "is_capital": False,
            "old_names": [],
            "population": 637942,
        }
    ]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("type=municipality", ["1381701000", "1400101000", "1400102000", "1402701000"]),
        ("type=sub_municipality", ["1380601000"]),
        ("region_code=1300000000", ["1380601000", "1381701000"]),
        ("province_code=1400100000", ["1400101000", "1400102000"]),
        ("city_code=1380600000", ["1380601000"]),
        ("region_code=1400000000&province_code=1402700000", ["1402701000"]),
        ("region_code=1300000000&type=municipality", ["1381701000"]),
        ("province_code=1400100000&psgc_code=1402701000", []),
        ("region_code=9900000000", []),
    ],
)
def test_filters(client: TestClient, query: str, expected: list[str]) -> None:
    response = client.get(f"/api/v1/municipalities?{query}")

    assert response.status_code == 200
    assert codes(response.json()) == expected
    assert response.json()["pagination"]["total"] == len(expected)


def test_pagination_applies_after_filtering(client: TestClient) -> None:
    body = client.get("/api/v1/municipalities?type=municipality&page=2&per_page=3").json()

    assert codes(body) == ["1402701000"]
    assert body["pagination"] == {"page": 2, "per_page": 3, "total": 4, "total_pages": 2}


@pytest.mark.parametrize(
    "query",
    ["type=city", "province_code=01028", "city_code=abc", "region_code=1", "psgc_code=14001010000"],
)
def test_invalid_filters_return_422(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/municipalities?{query}")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["data"] is None
