import time
import pytest
from conftest import SLEEP
from educationdata import EducationDataAPI

api = EducationDataAPI()


def test_summary_stat_functions():
    stats = ["sum", "count", "avg", "median", "min", "max", "variance", "stddev"]
    for stat in stats:
        result = api.ccd_summary("enrollment", stat, "school_level")
        assert result.count >= 0
        time.sleep(SLEEP)


def test_summary_var_options():
    vars_ = [
        "latitude", "longitude", "county_code", "lowest_grade_offered",
        "highest_grade_offered", "elem_cedp", "middle_cedp", "high_cedp",
        "ungrade_cedp", "teachers_fte", "lunch_program", "free_lunch",
        "reduced_price_lunch", "free_or_reduced_price_lunch",
        "direct_certification", "enrollment",
    ]
    for var in vars_:
        result = api.ccd_summary(var, "avg", "school_level")
        assert result.count >= 0
        time.sleep(SLEEP)


def test_summary_by_groupings():
    groupings = [
        "ncessch", "ncessch_num", "leaid", "state_leaid", "seasch",
        "state_location", "fips", "csa", "cbsa", "urban_centric_locale",
        "congress_district_id", "school_level", "school_type", "school_status",
        "bureau_indian_education", "title_i_status", "title_i_eligible",
        "title_i_schoolwide", "charter", "magnet", "shared_time", "virtual",
    ]
    for grouping in groupings:
        result = api.ccd_summary("enrollment", "count", grouping)
        assert result.count >= 0
        time.sleep(SLEEP)


def test_summary_with_filters():
    result = api.ccd_summary(
        "enrollment", "sum", "school_type",
        ncessch_num=13, charter=1, fips=11,
        state_leaid=1300180, urban_centric_locale=1,
        school_level=2, school_type=1, school_status=1,
        bureau_indian_education=1, title_i_status=1, magnet=1,
    )
    assert result.count >= 0
    time.sleep(SLEEP)


def test_invalid_stat_raises_error():
    with pytest.raises(Exception):
        api.ccd_summary("enrollment", "invalid_stat", "school_level")
