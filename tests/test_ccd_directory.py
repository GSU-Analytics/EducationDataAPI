import time
import pytest
from conftest import SLEEP
from educationdata import EducationDataAPI

api = EducationDataAPI()


@pytest.mark.parametrize("filter_key, filter_value", [
    ("ncessch", "10000500871"),
    ("leaid", "100005"),
    ("state_leaid", "AL-001"),
])
def test_filter_by_identifiers(filter_key, filter_value):
    result = api.ccd_directory(year=2020, **{filter_key: filter_value})
    rows = result.to_dict()
    assert isinstance(rows, list)
    assert all(item.get(filter_key) == filter_value for item in rows)
    time.sleep(SLEEP)


@pytest.mark.parametrize("filter_key, filter_value, expected_value", [
    ("fips", 1, 1),
    ("state_location", "AL", "AL"),
    ("csa", 122, 122),
])
def test_geographic_filters(filter_key, filter_value, expected_value):
    result = api.ccd_directory(year=2020, **{filter_key: filter_value})
    rows = result.to_dict()
    assert all(item.get(filter_key) == expected_value for item in rows)
    time.sleep(SLEEP)


@pytest.mark.parametrize("filter_key, filter_value", [
    ("school_level", 1),
    ("school_type", 2),
    ("school_status", 1),
])
def test_school_characteristics_filters(filter_key, filter_value):
    result = api.ccd_directory(year=2020, **{filter_key: filter_value})
    rows = result.to_dict()
    assert all(item.get(filter_key) == filter_value for item in rows)
    time.sleep(SLEEP)


def test_comprehensive_filters():
    result = api.ccd_directory(year=2020, fips=4, school_level=1, title_i_status=2)
    rows = result.to_dict()
    assert all(
        item["fips"] == 4 and item["school_level"] == 1 and item["title_i_status"] == 2
        for item in rows
    )
    time.sleep(SLEEP)


def test_special_value_filters():
    result = api.ccd_directory(year=2020, enrollment=-1)
    assert result.count >= 0
    time.sleep(SLEEP)
