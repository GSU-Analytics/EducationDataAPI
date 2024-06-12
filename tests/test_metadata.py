# test_metadata.py

import time
from educationdata import EducationDataAPI

api = EducationDataAPI()

SLEEP = 0.25

def test_metadata_endpoints():
    data = api.get_metadata_endpoints()
    assert 'error' not in data
    time.sleep(SLEEP)

def test_metadata_downloads():
    data = api.get_metadata_downloads()
    assert 'error' not in data
    time.sleep(SLEEP)

def test_metadata_variables():
    data = api.get_metadata_variables()
    assert 'error' not in data
    time.sleep(SLEEP)

def test_metadata_endpoint_varlist_structure():
    time.sleep(0.25)
    response = api.get_metadata_endpoint_varlist()
    assert 'count' in response
    assert 'next' in response
    assert 'previous' in response
    assert isinstance(response['results'], list)
    if response['results']:
        for item in response['results']:
            assert 'endpoint_id' in item
            assert 'variable' in item
            assert 'label' in item
            assert 'is_filter' in item
            assert 'data_type' in item
            assert 'format' in item
            assert 'values' in item