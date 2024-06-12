import pytest
import time
from educationdata import EducationDataAPI

api = EducationDataAPI()

SLEEP = 0.25

def test_summary_stat_functions():
    stats = ['sum', 'count', 'avg', 'median', 'min', 'max', 'variance', 'stddev']
    results = []
    for stat in stats:
        result = api.get_ccd_summary('enrollment', stat, 'school_level')
        assert 'error' not in result
        results.append(result)
        time.sleep(SLEEP)
    assert all(results)

def test_summary_var_options():
    vars = [
    'latitude', 'longitude', 'county_code', 'lowest_grade_offered', 'highest_grade_offered',
    'elem_cedp', 'middle_cedp', 'high_cedp', 'ungrade_cedp', 'teachers_fte',
    'lunch_program', 'free_lunch', 'reduced_price_lunch', 'free_or_reduced_price_lunch',
    'direct_certification', 'enrollment'
    ]
    results = []
    for var in vars:
        result = api.get_ccd_summary(var, 'avg', 'school_level')
        assert 'error' not in result
        results.append(result)
        time.sleep(SLEEP)
    assert all(results)

def test_summary_by_groupings():
    groupings = [
    'ncessch', 'ncessch_num', 'leaid', 'state_leaid', 'seasch', 'state_location',
    'fips', 'csa', 'cbsa', 'urban_centric_locale', 'congress_district_id',
    'school_level', 'school_type', 'school_status', 'bureau_indian_education',
    'title_i_status', 'title_i_eligible', 'title_i_schoolwide', 'charter', 'magnet',
    'shared_time', 'virtual'
    ]

    results = []
    for grouping in groupings:
        result = api.get_ccd_summary('enrollment', 'count', grouping)
        assert 'error' not in result
        results.append(result)
        time.sleep(SLEEP)
    assert all(results)

def test_summary_with_filters():
    filters = {
        'ncessch_num': 13,
        'charter': 1,
        'fips': 11,
        'state_leaid': 1300180, # BAKER COUNTY, GA
        'urban_centric_locale': 1,  # Assuming '1' is a valid option.
        'school_level': 2,  # Assuming '2' represents a valid school level.
        'school_type': 1,  # Assuming '1' is a valid school type.
        'school_status': 1,  # Assuming '1' represents 'Open'.
        'bureau_indian_education': 1,  # Assuming '1' means 'Yes'.
        'title_i_status': 1,  # Assuming '1' for a specific Title I status.
        'magnet': 1  # Assuming '1' means 'Yes'.
    }

    result = api.get_ccd_summary('enrollment', 'sum', 'school_type', **filters)
    assert 'error' not in result
    time.sleep(SLEEP)

def test_invalid_stat_raises_error():
    with pytest.raises(Exception):
        api.get_ccd_summary('enrollment', 'invalid_stat', 'school_level')
        time.sleep(SLEEP)
