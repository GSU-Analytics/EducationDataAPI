
# test_ccd_directory.py

import time
import pytest
from setup import SLEEP
from educationdata import EducationDataAPI

api = EducationDataAPI()

@pytest.mark.parametrize("filter_key, filter_value", [
    ('ncessch', '10000500871'),
    ('leaid', '100005'),
    ('state_leaid', 'AL-001'),
])
def test_filter_by_identifiers(filter_key, filter_value):
    result = api.get_ccd_directory(year=2020, **{filter_key: filter_value})
    
    # Check if the result is a string and try to parse it as JSON
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            assert False, f"Failed to parse JSON response: {result}"
    
    # Check if the 'results' key exists in the response
    assert 'results' in result, "The 'results' key is missing from the response"
    assert isinstance(result['results'], list), "The 'results' key should contain a list"

    # Now check that each item in 'results' matches the filter criteria
    assert all(item.get(filter_key) == filter_value for item in result['results']), "Not all items matched the filter criteria"

# Test geographic filters
@pytest.mark.parametrize("filter_key, filter_value, expected_value", [
    ('fips', 1, 1),
    ('state_location', 'AL', 'AL'),
    ('csa', 122, None),
])
def test_geographic_filters(filter_key, filter_value, expected_value):
    result = api.get_ccd_directory(year=2020, **{filter_key: filter_value})
    assert 'error' not in result
    assert all(item.get(filter_key) == expected_value for item in result['results']), "Not all items matched the filter criteria"
    time.sleep(SLEEP)

# Test school characteristics filters
@pytest.mark.parametrize("filter_key, filter_value", [
    ('school_level', 1),
    ('school_type', 2),
    ('school_status', 1),
])
def test_school_characteristics_filters(filter_key, filter_value):
    result = api.get_ccd_directory(year=2020, **{filter_key: filter_value})
    assert 'error' not in result
    assert all(item.get(filter_key) == filter_value for item in result['results']), "Not all items matched the filter criteria"
    time.sleep(SLEEP)

# Comprehensive filter test
def test_comprehensive_filters():
    filters = {
        'fips': 4,
        'school_level': 1,
        'title_i_status': 2,
    }
    result = api.get_ccd_directory(year=2020, **filters)
    assert 'error' not in result
    assert all(item['fips'] == 4 and item['school_level'] == 1 and item['title_i_status'] == 2 for item in result['results']), "Not all items matched the comprehensive filter criteria"
    time.sleep(SLEEP)

# Check handling of special values
def test_special_value_filters():
    result = api.get_ccd_directory(year=2020, enrollment=-1)
    assert 'error' not in result
    assert all(item.get('enrollment') == -1 for item in result['results'] if item.get('enrollment') is not None), "Not all items matched the special value filter criteria"
    time.sleep(SLEEP)
