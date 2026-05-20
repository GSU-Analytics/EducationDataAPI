from __future__ import annotations
import requests
from educationdata._pagination import fetch_all_pages
from educationdata._result import EducationDataResult

BASE_URL = "https://educationdata.urban.org/api/v1/"

# Valid segment combos → URL path fragment (order-sensitive per API)
_RACE_SEX_COMBOS = [
    ("race", "sex"),
    ("disability", "sex"),
    ("lep", "sex"),
]
_DISCIPLINE_COMBOS = [
    ("disability", "sex"),
    ("disability", "race", "sex"),
    ("disability", "lep", "sex"),
]


def _build_segment_path(by: list[str], valid_combos: list[tuple]) -> str:
    """Return the URL path segment string for a given by= combination."""
    key = tuple(sorted(by))
    combo_map: dict[tuple, str] = {
        tuple(sorted(c)): ("/".join(c) + "/") if c else ""
        for c in valid_combos
    }
    if key not in combo_map:
        valid = [list(c) for c in valid_combos if c]
        raise ValueError(f"Invalid 'by' combination: {by!r}. Valid values: {valid}")
    return combo_map[key]


def _build_url(path: str, **kwargs) -> str:
    url = BASE_URL + path
    if kwargs:
        url += "?" + "&".join(f"{k}={v}" for k, v in kwargs.items())
    return url


class EducationDataAPI:
    """Python client for the Urban Institute Education Data Portal API."""

    def __init__(self) -> None:
        self.session = requests.Session()

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def metadata_endpoints(self) -> EducationDataResult:
        """General information about each API endpoint."""
        return fetch_all_pages(self.session, _build_url("api-endpoints"))

    def metadata_downloads(self) -> EducationDataResult:
        """Downloadable data files and codebooks for each endpoint."""
        return fetch_all_pages(self.session, _build_url("api-downloads"))

    def metadata_variables(self) -> EducationDataResult:
        """Information about each variable in the portal."""
        return fetch_all_pages(self.session, _build_url("api-variables"))

    def metadata_endpoint_varlist(self) -> EducationDataResult:
        """Variables in the portal broken out by endpoint."""
        return fetch_all_pages(self.session, _build_url("api-endpoint-varlist"))

    # ------------------------------------------------------------------
    # CCD — Schools
    # ------------------------------------------------------------------

    def ccd_directory(self, year: int, **kwargs) -> EducationDataResult:
        """CCD school directory for a given year.

        See https://educationdata.urban.org/documentation/schools.html#ccd_directory
        """
        url = _build_url(f"schools/ccd/directory/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ccd_summary(self, var: str, stat: str, by: str, **kwargs) -> EducationDataResult:
        """CCD summary statistics for a variable.

        Args:
            var: Variable name (e.g. "enrollment").
            stat: Statistic ("sum", "count", "avg", "median", "min", "max",
                  "variance", "stddev").
            by: Grouping variable string (e.g. "school_level"). This is an API
                query parameter, not a segment list.

        See https://educationdata.urban.org/documentation/schools.html#ccd_summary
        """
        url = _build_url(f"schools/ccd/summary/", var=var, stat=stat, by=by, **kwargs)
        return fetch_all_pages(self.session, url)

    def ccd_enrollment(
        self, year: int, grade: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CCD enrollment by grade with optional demographic breakdowns.

        Args:
            year: Academic year (1986–2022).
            grade: Grade level (-1=PreK, 0–12, 99=Total).
            by: Demographic segments. Valid combinations:
                [], ["race"], ["sex"], ["race", "sex"].

        See https://educationdata.urban.org/documentation/schools.html#ccd-enrollment-by-grade
        """
        valid: list[tuple] = [(), ("race",), ("sex",), ("race", "sex")]
        seg = _build_segment_path(by, valid)
        url = _build_url(f"schools/ccd/enrollment/{year}/grade-{grade}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # CRDC — Schools
    # ------------------------------------------------------------------

    def crdc_directory(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC school directory for a given year.

        See https://educationdata.urban.org/documentation/schools.html#crdc_directory
        """
        url = _build_url(f"schools/crdc/directory/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_enrollment(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC enrollment with required demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].

        See https://educationdata.urban.org/documentation/schools.html#crdc-enrollment-by-race-and-sex
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/enrollment/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_discipline(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC discipline data. Empty by= returns aggregate instances.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Demographic segment. Valid combinations:
                [] (aggregate), ["disability", "sex"],
                ["disability", "race", "sex"], ["disability", "lep", "sex"].

        See https://educationdata.urban.org/documentation/schools.html#crdc_discipline-incidents
        """
        if not by:
            url = _build_url(f"schools/crdc/discipline-instances/{year}/", **kwargs)
        else:
            seg = _build_segment_path(by, _DISCIPLINE_COMBOS)
            url = _build_url(f"schools/crdc/discipline/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_bullying_allegations(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC harassment/bullying allegations (school-level totals).

        See https://educationdata.urban.org/documentation/schools.html#crdc-harassment-or-bullying-allegations
        """
        url = _build_url(f"schools/crdc/harassment-or-bullying/{year}/allegations/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_bullying(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC bullying/harassment students disciplined or harassed.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].

        See https://educationdata.urban.org/documentation/schools.html#crdc-harassment-or-bullying
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/harassment-or-bullying/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_absenteeism(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC chronic absenteeism by demographic breakdown.

        Args:
            year: Academic year (2013, 2015).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/chronic-absenteeism/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_restraint(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC restraint and seclusion data. Empty by= returns instances.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Demographic segment. Valid combinations:
                [] (instances), ["disability", "sex"],
                ["disability", "race", "sex"], ["disability", "lep", "sex"].
        """
        if not by:
            url = _build_url(f"schools/crdc/restraint-and-seclusion/{year}/instances/", **kwargs)
        else:
            seg = _build_segment_path(by, _DISCIPLINE_COMBOS)
            url = _build_url(f"schools/crdc/restraint-and-seclusion/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_advanced_enrollment(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC AP/IB/gifted enrollment by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].

        See https://educationdata.urban.org/documentation/schools.html#crdc-ap-and-ib-enrollment
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/ap-ib-enrollment/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_ap(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC AP exam participation by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/ap-exams/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_college_exam(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC SAT/ACT participation by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/sat-act-participation/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_staff(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC teachers and staff data.

        See https://educationdata.urban.org/documentation/schools.html#crdc-teachers-and-staff
        """
        url = _build_url(f"schools/crdc/teachers-staff/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_math_science_enrollment(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC math and science enrollment by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/math-and-science/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_algebra_enrollment(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC Algebra I enrollment by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/algebra1/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_offenses(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC school offenses and incidents.

        See https://educationdata.urban.org/documentation/schools.html#crdc-offenses
        """
        url = _build_url(f"schools/crdc/offenses/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_dual_enrollment(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC dual enrollment by demographic breakdown.

        Args:
            year: Academic year (2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/dual-enrollment/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_credit_recovery(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC credit recovery program data.

        See https://educationdata.urban.org/documentation/schools.html#crdc-credit-recovery
        """
        url = _build_url(f"schools/crdc/credit-recovery/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_days_suspended(
        self, year: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC days lost to suspension by demographic breakdown.

        Args:
            year: Academic year (2015, 2017).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/suspensions-days/{year}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_offerings(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC course and program offerings.

        See https://educationdata.urban.org/documentation/schools.html#crdc-offerings
        """
        url = _build_url(f"schools/crdc/offerings/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_school_finance(self, year: int, **kwargs) -> EducationDataResult:
        """CRDC school-level finance data.

        See https://educationdata.urban.org/documentation/schools.html#crdc-school-finance
        """
        url = _build_url(f"schools/crdc/school-finance/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def crdc_retention(
        self, year: int, grade: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CRDC grade retention by demographic breakdown.

        Args:
            year: Academic year (2011, 2013, 2015, 2017).
            grade: Grade level (-1=PreK, 0=K, 1–12).
            by: Required demographic segment. Valid combinations:
                ["race", "sex"], ["disability", "sex"], ["lep", "sex"].
        """
        seg = _build_segment_path(by, _RACE_SEX_COMBOS)
        url = _build_url(f"schools/crdc/retention/{year}/grade-{grade}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # EdFacts — Schools
    # ------------------------------------------------------------------

    def edfacts_assessments(
        self, year: int, grade: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """EdFacts state assessments data.

        Args:
            year: Academic year (2009–2018, 2020).
            grade: EDFacts grade category (3–8, 11, etc.).
            by: Optional segment. Valid values:
                [], ["race"], ["sex"], ["special-populations"].

        See https://educationdata.urban.org/documentation/schools.html#edfacts-assessments
        """
        valid: list[tuple] = [
            (),
            ("race",),
            ("sex",),
            ("special-populations",),
        ]
        seg = _build_segment_path(by, valid)
        url = _build_url(f"schools/edfacts/assessments/{year}/grade-{grade}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def edfacts_grad_rates(self, year: int, **kwargs) -> EducationDataResult:
        """EdFacts adjusted cohort graduation rates.

        Args:
            year: Academic year (2010–2019).

        See https://educationdata.urban.org/documentation/schools.html#edfacts-grad-rates
        """
        url = _build_url(f"schools/edfacts/grad-rates/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # NHGIS / MEPS — Schools
    # ------------------------------------------------------------------

    def nhgis_geographic_variables(
        self, endpoint: str, year: int, **kwargs
    ) -> EducationDataResult:
        """NHGIS geographic variables joined to school records.

        Args:
            endpoint: Census vintage ("census-2010", "census-2000", "census-1990").
            year: Academic year (1986–2021).
        """
        valid_endpoints = {"census-2010", "census-2000", "census-1990"}
        if endpoint not in valid_endpoints:
            raise ValueError(
                f"Invalid endpoint {endpoint!r}. Valid: {sorted(valid_endpoints)}"
            )
        url = _build_url(f"schools/nhgis/{endpoint}/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def meps_school_poverty(self, year: int, **kwargs) -> EducationDataResult:
        """MEPS school poverty estimates.

        Args:
            year: Academic year (2013–2020).
        """
        if year not in range(2013, 2021):
            raise ValueError("year must be between 2013 and 2020 inclusive.")
        url = _build_url(f"schools/meps/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)
