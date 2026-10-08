from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.city import City, CityClass
from app.infrastructure.repositories.city_repository import InMemoryCityRepository
from app.main import app
from app.presentation.api.v1.dependencies import get_city_repository

MANILA = City(
    psgc_code="1380600000",
    name="City of Manila",
    correspondence_code="133900000",
    city_class=CityClass.HIGHLY_URBANIZED,
    region_code="1300000000",
    province_code=None,
    income_classification="1st",
    is_capital=False,
    old_names=(),
    population=1902590,
)
BAGUIO = City(
    psgc_code="1430300000",
    name="City of Baguio",
    correspondence_code="141102000",
    city_class=CityClass.HIGHLY_URBANIZED,
    region_code="1400000000",
    province_code=None,
    income_classification="1st",
    is_capital=False,
    old_names=(),
    population=366358,
)
TABUK = City(
    psgc_code="1403213000",
    name="City of Tabuk",
    correspondence_code="143213000",
    city_class=CityClass.COMPONENT,
    region_code="1400000000",
    province_code="1403200000",
    income_classification="4th",
    is_capital=True,
    old_names=(),
    population=121033,
)
SANTIAGO = City(
    psgc_code="0203135000",
    name="City of Santiago",
    correspondence_code="023135000",
    city_class=CityClass.INDEPENDENT_COMPONENT,
    region_code="0200000000",
    province_code="0203100000",
    income_classification="1st",
    is_capital=False,
    old_names=(),
    population=148580,
)
ISABELA = City(
    psgc_code="0990101000",
    name="City of Isabela",
    correspondence_code="099701000",
    city_class=CityClass.COMPONENT,
    region_code="0900000000",
    province_code=None,
    income_classification="3rd",
    is_capital=False,
    old_names=(),
    population=151297,
)

ALL = [MANILA, BAGUIO, TABUK, SANTIAGO, ISABELA]


def codes(body: dict) -> list[str]:
    return [item["psgc_code"] for item in body["data"]]


@pytest.fixture(autouse=True)
def city_repository() -> Iterator[None]:
    repository = InMemoryCityRepository(ALL)
    app.dependency_overrides[get_city_repository] = lambda: repository
    yield
    app.dependency_overrides.pop(get_city_repository, None)


def test_list_cities_sorted_by_code(client: TestClient) -> None:
    response = client.get("/api/v1/cities")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Cities retrieved successfully"
    assert codes(body) == ["0203135000", "0990101000", "1380600000", "1403213000", "1430300000"]
    assert body["pagination"] == {"page": 1, "per_page": 20, "total": 5, "total_pages": 1}


def test_city_fields(client: TestClient) -> None:
    body = client.get("/api/v1/cities?psgc_code=1403213000").json()

    assert body["data"] == [
        {
            "psgc_code": "1403213000",
            "name": "City of Tabuk",
            "correspondence_code": "143213000",
            "city_class": "CC",
            "region_code": "1400000000",
            "province_code": "1403200000",
            "income_classification": "4th",
            "is_capital": True,
            "old_names": [],
            "population": 121033,
        }
    ]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("city_class=HUC", ["1380600000", "1430300000"]),
        ("city_class=ICC", ["0203135000"]),
        ("city_class=CC", ["0990101000", "1403213000"]),
        ("region_code=1400000000", ["1403213000", "1430300000"]),
        ("province_code=1403200000", ["1403213000"]),
        ("region_code=1400000000&city_class=HUC", ["1430300000"]),
        ("province_code=1900700000", []),
        ("psgc_code=9999999999", []),
    ],
)
def test_filters(client: TestClient, query: str, expected: list[str]) -> None:
    response = client.get(f"/api/v1/cities?{query}")

    assert response.status_code == 200
    assert codes(response.json()) == expected
    assert response.json()["pagination"]["total"] == len(expected)


def test_pagination_applies_after_filtering(client: TestClient) -> None:
    body = client.get("/api/v1/cities?region_code=1400000000&page=2&per_page=1").json()

    assert codes(body) == ["1430300000"]
    assert body["pagination"] == {"page": 2, "per_page": 1, "total": 2, "total_pages": 2}


@pytest.mark.parametrize(
    "query", ["city_class=huc", "city_class=MUN", "province_code=0103", "region_code=x"]
)
def test_invalid_filters_return_422(client: TestClient, query: str) -> None:
    response = client.get(f"/api/v1/cities?{query}")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["data"] is None
