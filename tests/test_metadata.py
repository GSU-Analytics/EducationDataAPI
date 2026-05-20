import time
from conftest import SLEEP
from educationdata import EducationDataAPI

api = EducationDataAPI()


def test_metadata_endpoints():
    result = api.metadata_endpoints()
    assert result.count >= 0
    time.sleep(SLEEP)


def test_metadata_downloads():
    result = api.metadata_downloads()
    assert result.count >= 0
    time.sleep(SLEEP)


def test_metadata_variables():
    result = api.metadata_variables()
    assert result.count >= 0
    time.sleep(SLEEP)


def test_metadata_endpoint_varlist_structure():
    time.sleep(SLEEP)
    result = api.metadata_endpoint_varlist()
    assert isinstance(result.count, int)
    rows = result.to_dict()
    assert isinstance(rows, list)
    if rows:
        for item in rows:
            assert "endpoint_id" in item
            assert "variable" in item
            assert "label" in item
            assert "is_filter" in item
            assert "data_type" in item
            assert "format" in item
            assert "values" in item
