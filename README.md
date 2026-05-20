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

### School Districts — CCD / SAIPE / EdFacts

| Method | Key parameters |
|---|---|
| `district_directory(year, **filters)` | |
| `district_enrollment(year, grade, by=[], **filters)` | `by`: `[]`, `["race"]`, `["sex"]`, `["race","sex"]` |
| `district_finance(year, **filters)` | |
| `district_poverty(year, **filters)` | SAIPE poverty estimates |
| `district_edfacts_assessments(year, grade, by=[], **filters)` | `by`: `[]`, `["race"]`, `["sex"]`, `["special-populations"]` |
| `district_edfacts_grad_rates(year, **filters)` | |

### Colleges — IPEDS

| Method | Key parameters |
|---|---|
| `ipeds_directory(year, **filters)` | |
| `ipeds_institutional_characteristics(year, **filters)` | |
| `ipeds_admissions_enrollment(year, **filters)` | |
| `ipeds_admissions_requirements(year, **filters)` | |
| `ipeds_fall_enrollment(year, by, level=None, **filters)` | `by`: `["race","sex"]`, `["age","sex"]`, `["residence"]`; `level` required for race/sex and age/sex |
| `ipeds_enrollment_full_time_equivalent(year, level, **filters)` | |
| `ipeds_enrollment_headcount(year, level, **filters)` | |
| `ipeds_fall_retention(year, **filters)` | |
| `ipeds_academic_year_tuition(year, **filters)` | |
| `ipeds_academic_year_tuition_prof_program(year, **filters)` | |
| `ipeds_academic_year_room_board_other(year, **filters)` | |
| `ipeds_program_year_tuition_cip(year, **filters)` | |
| `ipeds_program_year_room_board_other(year, **filters)` | |
| `ipeds_sfa_grants_and_net_price(year, **filters)` | |
| `ipeds_sfa_by_living_arrangement(year, **filters)` | |
| `ipeds_sfa_by_tuition_type(year, **filters)` | |
| `ipeds_sfa_all_undergraduates(year, **filters)` | |
| `ipeds_sfa_ftft(year, **filters)` | First-time full-time undergrads |
| `ipeds_finance(year, **filters)` | |
| `ipeds_student_faculty_ratio(year, **filters)` | |
| `ipeds_grad_rates(year, **filters)` | 150% normal time |
| `ipeds_grad_rates_200pct(year, **filters)` | 200% normal time |
| `ipeds_grad_rates_pell(year, **filters)` | By federal aid type |
| `ipeds_outcome_measures(year, **filters)` | |
| `ipeds_completers(year, **filters)` | |
| `ipeds_completions_cip_2(year, **filters)` | By 2-digit CIP |
| `ipeds_completions_cip_6(year, **filters)` | By 6-digit CIP |
| `ipeds_academic_libraries(year, **filters)` | |
| `ipeds_salaries_instructional_staff(year, **filters)` | |
| `ipeds_salaries_noninstructional_staff(year, **filters)` | |

### Colleges — Scorecard

| Method | Key parameters |
|---|---|
| `scorecard_institutional_characteristics(year, **filters)` | |
| `scorecard_student_characteristics(year, variant, **filters)` | `variant`: `"aid-applicants"`, `"home-neighborhood"` |
| `scorecard_earnings(year, **filters)` | |
| `scorecard_default(year, **filters)` | |
| `scorecard_repayment(year, **filters)` | |

### Colleges — NHGIS / FSA / NACUBO / NCCS / EADA / Campus Crime / PSEO

| Method | Key parameters |
|---|---|
| `college_nhgis_geographic_variables(endpoint, year, **filters)` | `endpoint`: `"census-1990"` … `"census-2020"` |
| `fsa_financial_responsibility(year, **filters)` | |
| `fsa_grants(year, **filters)` | |
| `fsa_loans(year, **filters)` | |
| `fsa_campus_based_volume(year, **filters)` | |
| `fsa_90_10_revenue(year, **filters)` | For-profit institutions |
| `nacubo_endowments(year, **filters)` | |
| `nccs_990_forms(year, **filters)` | IRS Form 990 |
| `eada_institutional_characteristics(year, **filters)` | Equity in athletics |
| `campus_crime_hate_crimes(year, **filters)` | |
| `pseo_earnings_and_flows(year, **filters)` | Post-secondary employment |

## Development

```bash
uv sync           # install all deps including dev
uv run pytest     # run all tests (integration tests hit live API)
uv run pytest tests/test_unit.py   # unit tests only (no network)
uv build          # build dist/
```

## License

MIT
