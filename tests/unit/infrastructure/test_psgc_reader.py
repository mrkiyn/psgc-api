from pathlib import Path

import pytest

from app.domain.entities.barangay import Barangay, UrbanRural
from app.domain.entities.city import City, CityClass
from app.domain.entities.municipality import Municipality, MunicipalityType
from app.domain.entities.province import Province
from app.domain.entities.region import Region
from app.infrastructure.psgc.reader import PsgcDataset, read_dataset

DATAFILE = Path(__file__).parents[3] / "data" / "raw" / "PSGC-2Q-2026-Publication-Datafile.xlsx"

pytestmark = pytest.mark.skipif(not DATAFILE.exists(), reason="PSGC datafile not present")


@pytest.fixture(scope="module")
def dataset() -> PsgcDataset:
    return read_dataset(DATAFILE)


@pytest.fixture(scope="module")
def regions(dataset: PsgcDataset) -> dict[str, Region]:
    return {region.psgc_code: region for region in dataset.regions}


@pytest.fixture(scope="module")
def provinces(dataset: PsgcDataset) -> dict[str, Province]:
    return {province.psgc_code: province for province in dataset.provinces}


@pytest.fixture(scope="module")
def cities(dataset: PsgcDataset) -> dict[str, City]:
    return {city.psgc_code: city for city in dataset.cities}


@pytest.fixture(scope="module")
def municipalities(dataset: PsgcDataset) -> dict[str, Municipality]:
    return {municipality.psgc_code: municipality for municipality in dataset.municipalities}


def test_reads_all_18_regions(regions: dict[str, Region]) -> None:
    assert len(regions) == 18
    assert all(len(code) == 10 and code.isdigit() for code in regions)


def test_restores_leading_zeros_lost_by_excel(regions: dict[str, Region]) -> None:
    assert regions["0100000000"] == Region(
        psgc_code="0100000000",
        name="Region I (Ilocos Region)",
        correspondence_code="010000000",
        population=5342453,
    )


def test_keeps_missing_correspondence_code_as_none(regions: dict[str, Region]) -> None:
    assert regions["1800000000"].name == "Negros Island Region (NIR)"
    assert regions["1800000000"].correspondence_code is None


def test_reads_all_82_provinces(provinces: dict[str, Province]) -> None:
    assert len(provinces) == 82
    assert all(len(code) == 10 and code.isdigit() for code in provinces)


def test_reads_province_fields(provinces: dict[str, Province]) -> None:
    assert provinces["0102800000"] == Province(
        psgc_code="0102800000",
        name="Ilocos Norte",
        correspondence_code="012800000",
        region_code="0100000000",
        income_classification="1st",
        population=618850,
    )


def test_assigns_region_by_psgc_code_not_correspondence_code(provinces: dict[str, Province]) -> None:
    negros_occidental = provinces["1804500000"]
    assert negros_occidental.correspondence_code == "064500000"
    assert negros_occidental.region_code == "1800000000"


def test_every_province_belongs_to_a_known_region(
    regions: dict[str, Region], provinces: dict[str, Province]
) -> None:
    assert {province.region_code for province in provinces.values()} <= regions.keys()
    assert not any(province.region_code == "1300000000" for province in provinces.values())


def test_reads_municipalities_and_sub_municipalities(municipalities: dict[str, Municipality]) -> None:
    types = [municipality.type for municipality in municipalities.values()]
    assert types.count(MunicipalityType.MUNICIPALITY) == 1493
    assert types.count(MunicipalityType.SUB_MUNICIPALITY) == 14


def test_reads_municipality_fields(municipalities: dict[str, Municipality]) -> None:
    assert municipalities["1400101000"] == Municipality(
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


def test_sub_municipalities_belong_to_manila(municipalities: dict[str, Municipality]) -> None:
    subs = [m for m in municipalities.values() if m.type is MunicipalityType.SUB_MUNICIPALITY]
    assert {m.city_code for m in subs} == {"1380600000"}
    assert all(m.province_code is None and m.region_code == "1300000000" for m in subs)
    assert all(m.income_classification is None for m in subs)


def test_municipalities_without_a_province(municipalities: dict[str, Municipality]) -> None:
    no_province = {
        m.name for m in municipalities.values()
        if m.type is MunicipalityType.MUNICIPALITY and m.province_code is None
    }
    assert len(no_province) == 9
    assert {"Pateros", "Kapalawan", "Old Kaabakan"} <= no_province


def test_dash_income_classification_becomes_none(municipalities: dict[str, Municipality]) -> None:
    kapalawan = next(m for m in municipalities.values() if m.name == "Kapalawan")
    assert kapalawan.income_classification is None
    assert kapalawan.region_code == "1900000000"


def test_capitals_and_old_names(municipalities: dict[str, Municipality]) -> None:
    assert sum(m.is_capital for m in municipalities.values()) == 37
    alfonso_lista = next(m for m in municipalities.values() if m.name == "Alfonso Lista")
    assert alfonso_lista.old_names == ("Potia",)
    assert sum(bool(m.old_names) for m in municipalities.values()) == 75


def test_municipality_parents_exist(
    regions: dict[str, Region],
    provinces: dict[str, Province],
    municipalities: dict[str, Municipality],
) -> None:
    assert {m.region_code for m in municipalities.values()} <= regions.keys()
    assert {m.province_code for m in municipalities.values()} - {None} <= provinces.keys()


def test_reads_all_149_cities(cities: dict[str, City]) -> None:
    classes = [city.city_class for city in cities.values()]
    assert len(cities) == 149
    assert classes.count(CityClass.HIGHLY_URBANIZED) == 33
    assert classes.count(CityClass.INDEPENDENT_COMPONENT) == 5
    assert classes.count(CityClass.COMPONENT) == 111


def test_reads_city_fields(cities: dict[str, City]) -> None:
    manila = cities["1380600000"]
    assert manila.name == "City of Manila"
    assert manila.correspondence_code == "133900000"
    assert manila.city_class is CityClass.HIGHLY_URBANIZED
    assert manila.region_code == "1300000000"
    assert manila.province_code is None
    assert manila.population == 1902590


def test_highly_urbanized_cities_have_no_province(cities: dict[str, City]) -> None:
    hucs = [c for c in cities.values() if c.city_class is CityClass.HIGHLY_URBANIZED]
    assert all(city.province_code is None for city in hucs)
    assert cities["1430300000"].name == "City of Baguio"


def test_isabela_province_follows_its_code(cities: dict[str, City]) -> None:
    isabela = cities["0990101000"]
    assert isabela.city_class is CityClass.COMPONENT
    assert isabela.region_code == "0900000000"
    assert isabela.province_code is None


def test_city_parents_exist(
    regions: dict[str, Region],
    provinces: dict[str, Province],
    cities: dict[str, City],
    municipalities: dict[str, Municipality],
) -> None:
    assert {c.region_code for c in cities.values()} <= regions.keys()
    assert {c.province_code for c in cities.values()} - {None} <= provinces.keys()
    assert {m.city_code for m in municipalities.values()} - {None} <= cities.keys()
    assert sum(c.province_code is not None for c in cities.values()) == 115
    assert sum(c.is_capital for c in cities.values()) == 45


# Barangays per region, from the datafile's "National Summary" sheet.
NATIONAL_SUMMARY_BARANGAYS = {
    "1300000000": 1715, "1400000000": 1178, "0100000000": 3267, "0200000000": 2311,
    "0300000000": 3105, "0400000000": 3992, "1700000000": 1460, "0500000000": 3471,
    "0600000000": 3389, "1800000000": 1353, "0700000000": 2312, "0800000000": 4365,
    "0900000000": 2314, "1000000000": 2022, "1100000000": 1162, "1200000000": 1097,
    "1600000000": 1312, "1900000000": 2185,
}


@pytest.fixture(scope="module")
def barangays(dataset: PsgcDataset) -> dict[str, Barangay]:
    return {barangay.psgc_code: barangay for barangay in dataset.barangays}


def test_barangay_counts_match_national_summary(barangays: dict[str, Barangay]) -> None:
    per_region: dict[str, int] = {}
    for barangay in barangays.values():
        per_region[barangay.region_code] = per_region.get(barangay.region_code, 0) + 1
    assert len(barangays) == 42010
    assert per_region == NATIONAL_SUMMARY_BARANGAYS


def test_barangay_parents_follow_the_code(
    provinces: dict[str, Province],
    cities: dict[str, City],
    municipalities: dict[str, Municipality],
    barangays: dict[str, Barangay],
) -> None:
    for code, barangay in barangays.items():
        lgu = code[:7] + "000"
        parent = code[:5] + "00000"
        assert barangay.region_code == code[:2] + "00000000"
        assert barangay.province_code == (parent if parent in provinces else None)
        if lgu in cities:
            assert (barangay.city_code, barangay.municipality_code) == (lgu, None)
        elif municipalities[lgu].type is MunicipalityType.SUB_MUNICIPALITY:
            assert (barangay.city_code, barangay.municipality_code) == (parent, lgu)
        else:
            assert (barangay.city_code, barangay.municipality_code) == (None, lgu)


def test_barangay_parent_groups(barangays: dict[str, Barangay]) -> None:
    values = barangays.values()
    assert sum(b.municipality_code is not None and b.city_code is None for b in values) == 34007
    assert sum(b.city_code is not None and b.municipality_code is None for b in values) == 7106
    assert sum(b.city_code == "1380600000" for b in values) == 897


def test_reads_barangay_fields(barangays: dict[str, Barangay]) -> None:
    assert barangays["1400101001"] == Barangay(
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


def test_barangay_urban_rural_and_old_names(barangays: dict[str, Barangay]) -> None:
    values = list(barangays.values())
    assert sum(b.urban_rural is UrbanRural.URBAN for b in values) == 7918
    assert sum(b.urban_rural is UrbanRural.RURAL for b in values) == 34054
    assert sum(b.urban_rural is None for b in values) == 38
    assert sum(bool(b.old_names) for b in values) == 1618
    assert barangays["1380100189"].old_names == ("Barangay 176",)
