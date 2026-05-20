# urban-education-data

Python client for the [Urban Institute Education Data Portal API](https://educationdata.urban.org/documentation/index.html).

## Install

```bash
pip install urban-education-data
# With pandas support:
pip install urban-education-data[df]
```

## Quick start

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()

# CCD school directory — all pages fetched automatically
result = api.ccd_directory(2020, fips=13)
print(result.count)          # total records in the API
rows = result.to_dict()      # list[dict]
df = result.to_df()          # pandas DataFrame (requires [df] extra)

# CCD enrollment by grade with race/sex breakdown
result = api.ccd_enrollment(2020, grade=8, by=["race", "sex"])

# CRDC discipline (segmented)
result = api.crdc_discipline(2017, by=["disability", "race", "sex"], fips=13)

# EdFacts assessments with race segment
result = api.edfacts_assessments(2018, grade=8, by=["race"])
```

## Methods

All methods return an `EducationDataResult` with three attributes:

| Attribute | Type | Description |
|---|---|---|
| `.count` | `int` | Total records reported by the API |
| `.to_dict()` | `list[dict]` | All records as a list of dicts |
| `.to_df()` | `pd.DataFrame` | All records as a DataFrame (requires pandas) |

Pagination is automatic — you always get the complete dataset.

### Metadata

| Method | Description |
|---|---|
| `metadata_endpoints()` | Info about each API endpoint |
| `metadata_downloads()` | Downloadable data files and codebooks |
| `metadata_variables()` | All portal variables |
| `metadata_endpoint_varlist()` | Variables broken out by endpoint |

### CCD — Schools

| Method | Key parameters |
|---|---|
| `ccd_directory(year, **filters)` | |
| `ccd_summary(var, stat, by, **filters)` | `by` is a string grouping variable |
| `ccd_enrollment(year, grade, by=[], **filters)` | `by`: `[]`, `["race"]`, `["sex"]`, `["race","sex"]` |

### CRDC — Schools

| Method | Valid `by` combos |
|---|---|
| `crdc_directory(year, **filters)` | — |
| `crdc_enrollment(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_discipline(year, by=[], **filters)` | `[]` (instances), `["disability","sex"]`, `["disability","race","sex"]`, `["disability","lep","sex"]` |
| `crdc_bullying_allegations(year, **filters)` | — |
| `crdc_bullying(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_absenteeism(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_restraint(year, by=[], **filters)` | `[]` (instances), `["disability","sex"]`, `["disability","race","sex"]`, `["disability","lep","sex"]` |
| `crdc_advanced_enrollment(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_ap(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_college_exam(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_staff(year, **filters)` | — |
| `crdc_math_science_enrollment(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_algebra_enrollment(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_offenses(year, **filters)` | — |
| `crdc_dual_enrollment(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_credit_recovery(year, **filters)` | — |
| `crdc_days_suspended(year, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |
| `crdc_offerings(year, **filters)` | — |
| `crdc_school_finance(year, **filters)` | — |
| `crdc_retention(year, grade, by, **filters)` | `["race","sex"]`, `["disability","sex"]`, `["lep","sex"]` |

### EdFacts — Schools

| Method | Valid `by` combos |
|---|---|
| `edfacts_assessments(year, grade, by=[], **filters)` | `[]`, `["race"]`, `["sex"]`, `["special-populations"]` |
| `edfacts_grad_rates(year, **filters)` | — |

### NHGIS / MEPS — Schools

| Method | Notes |
|---|---|
| `nhgis_geographic_variables(endpoint, year, **filters)` | `endpoint`: `"census-2010"`, `"census-2000"`, `"census-1990"` |
| `meps_school_poverty(year, **filters)` | `year`: 2013–2020 |

## Development

```bash
uv sync           # install all deps including dev
uv run pytest     # run all tests (integration tests hit live API)
uv run pytest tests/test_unit.py   # unit tests only (no network)
uv build          # build dist/
```

## License

MIT
