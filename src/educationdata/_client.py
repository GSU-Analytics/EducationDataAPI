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

    # ------------------------------------------------------------------
    # School Districts — CCD
    # ------------------------------------------------------------------

    def district_directory(self, year: int, **kwargs) -> EducationDataResult:
        """CCD local education agency directory for a given year.

        Args:
            year: Academic year (1986–2024).
        """
        url = _build_url(f"school-districts/ccd/directory/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def district_enrollment(
        self, year: int, grade: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """CCD district enrollment by grade with optional demographic breakdowns.

        Args:
            year: Academic year (1986–2024).
            grade: Grade level (-1=PreK, 0–12, 99=Total).
            by: Demographic segments. Valid combinations:
                [], ["race"], ["sex"], ["race", "sex"].
        """
        valid: list[tuple] = [(), ("race",), ("sex",), ("race", "sex")]
        seg = _build_segment_path(by, valid)
        url = _build_url(f"school-districts/ccd/enrollment/{year}/grade-{grade}/{seg}", **kwargs)
        return fetch_all_pages(self.session, url)

    def district_finance(self, year: int, **kwargs) -> EducationDataResult:
        """CCD district finance data.

        Args:
            year: Academic year (1991, 1994–2020).
        """
        url = _build_url(f"school-districts/ccd/finance/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # School Districts — SAIPE
    # ------------------------------------------------------------------

    def district_poverty(self, year: int, **kwargs) -> EducationDataResult:
        """SAIPE district poverty estimates.

        Args:
            year: Academic year (1995, 1997, 1999–2024).
        """
        url = _build_url(f"school-districts/saipe/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # School Districts — EdFacts
    # ------------------------------------------------------------------

    def district_edfacts_assessments(
        self, year: int, grade: int, by: list[str] = [], **kwargs
    ) -> EducationDataResult:
        """EdFacts district-level state assessments.

        Args:
            year: Academic year (2009–2018, 2020).
            grade: EDFacts grade category (e.g. 3–8, 11).
            by: Optional segment. Valid values:
                [], ["race"], ["sex"], ["special-populations"].
        """
        valid: list[tuple] = [
            (),
            ("race",),
            ("sex",),
            ("special-populations",),
        ]
        seg = _build_segment_path(by, valid)
        url = _build_url(
            f"school-districts/edfacts/assessments/{year}/grade-{grade}/{seg}", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def district_edfacts_grad_rates(self, year: int, **kwargs) -> EducationDataResult:
        """EdFacts district adjusted cohort graduation rates.

        Args:
            year: Academic year (2010–2019).
        """
        url = _build_url(f"school-districts/edfacts/grad-rates/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # Colleges — IPEDS
    # ------------------------------------------------------------------

    def ipeds_directory(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS postsecondary institution directory.

        Args:
            year: Academic year (1980, 1984–2024).
        """
        url = _build_url(f"college-university/ipeds/directory/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_institutional_characteristics(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS institutional characteristics.

        Args:
            year: Academic year (1980, 1984–2024).
        """
        url = _build_url(
            f"college-university/ipeds/institutional-characteristics/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_admissions_enrollment(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS applications, admissions, and enrollments.

        Args:
            year: Academic year (2001–2022).
        """
        url = _build_url(
            f"college-university/ipeds/admissions-enrollment/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_admissions_requirements(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS admissions requirements.

        Args:
            year: Academic year (1990–2022).
        """
        url = _build_url(
            f"college-university/ipeds/admissions-requirements/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_academic_year_tuition(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS tuition and fees (academic-year programs).

        Args:
            year: Academic year (1986–2021).
        """
        url = _build_url(
            f"college-university/ipeds/academic-year-tuition/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_academic_year_tuition_prof_program(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS tuition and fees by professional degree program.

        Args:
            year: Academic year (1986–2008, 2010–2021).
        """
        url = _build_url(
            f"college-university/ipeds/academic-year-tuition-prof-program/{year}/",
            **kwargs,
        )
        return fetch_all_pages(self.session, url)

    def ipeds_academic_year_room_board_other(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS room, board, and other expenses (academic-year programs).

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(
            f"college-university/ipeds/academic-year-room-board-other/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_program_year_tuition_cip(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS tuition and fees by CIP code (program-year programs).

        Args:
            year: Academic year (1987–2021).
        """
        url = _build_url(
            f"college-university/ipeds/program-year-tuition-cip/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_program_year_room_board_other(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS room, board, and other expenses (program-year programs).

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(
            f"college-university/ipeds/program-year-room-board-other/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_fall_enrollment(
        self,
        year: int,
        by: list[str],
        level: str | None = None,
        **kwargs,
    ) -> EducationDataResult:
        """IPEDS fall enrollment with required demographic breakdown.

        Args:
            year: Academic year.
            by: Required segment. Valid combinations:
                ["race", "sex"] (requires level),
                ["age", "sex"] (requires level),
                ["residence"] (no level needed).
            level: Level of study for race/sex and age/sex breakdowns
                   (e.g. "undergraduate", "graduate", "1", "2").

        Years available:
            race/sex — 1986–2022
            age/sex  — 1991, 1993, 1995, 1997, 1999–2020
            residence — 1986, 1988, 1992, 1994, 1996, 1998, 2000–2020
        """
        key = tuple(sorted(by))
        if key == ("race", "sex"):
            if level is None:
                raise ValueError("level is required for by=['race', 'sex']")
            url = _build_url(
                f"college-university/ipeds/fall-enrollment/{year}/{level}/race/sex/",
                **kwargs,
            )
        elif key == ("age", "sex"):
            if level is None:
                raise ValueError("level is required for by=['age', 'sex']")
            url = _build_url(
                f"college-university/ipeds/fall-enrollment/{year}/{level}/age/sex/",
                **kwargs,
            )
        elif key == ("residence",):
            url = _build_url(
                f"college-university/ipeds/fall-enrollment/{year}/residence/", **kwargs
            )
        else:
            raise ValueError(
                f"Invalid 'by': {by!r}. Valid: ['race','sex'], ['age','sex'], ['residence']"
            )
        return fetch_all_pages(self.session, url)

    def ipeds_enrollment_full_time_equivalent(
        self, year: int, level: int | str, **kwargs
    ) -> EducationDataResult:
        """IPEDS full-time-equivalent enrollment by level of study.

        Args:
            year: Academic year (1997–2021).
            level: Level of study (integer code, e.g. 2).
        """
        url = _build_url(
            f"college-university/ipeds/enrollment-full-time-equivalent/{year}/{level}/",
            **kwargs,
        )
        return fetch_all_pages(self.session, url)

    def ipeds_enrollment_headcount(
        self, year: int, level: int | str, **kwargs
    ) -> EducationDataResult:
        """IPEDS enrollment headcount by level of study.

        Args:
            year: Academic year (1996–2021).
            level: Level of study (integer code, e.g. 1).
        """
        url = _build_url(
            f"college-university/ipeds/enrollment-headcount/{year}/{level}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_fall_retention(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS fall retention rates.

        Args:
            year: Academic year (2003–2020).
        """
        url = _build_url(f"college-university/ipeds/fall-retention/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_finance(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS institutional finance data.

        Args:
            year: Academic year (1979, 1983–2017).
        """
        url = _build_url(f"college-university/ipeds/finance/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_student_faculty_ratio(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS student-to-faculty ratio.

        Args:
            year: Academic year (2009–2020).
        """
        url = _build_url(
            f"college-university/ipeds/student-faculty-ratio/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_sfa_grants_and_net_price(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS student financial aid: grants and net price.

        Args:
            year: Academic year (2008–2021).
        """
        url = _build_url(
            f"college-university/ipeds/sfa-grants-and-net-price/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_sfa_by_living_arrangement(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS student financial aid by living arrangement.

        Args:
            year: Academic year (2008–2021).
        """
        url = _build_url(
            f"college-university/ipeds/sfa-by-living-arrangement/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_sfa_by_tuition_type(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS student financial aid by tuition type.

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(
            f"college-university/ipeds/sfa-by-tuition-type/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_sfa_all_undergraduates(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS student financial aid for all undergraduates.

        Args:
            year: Academic year (2007–2021).
        """
        url = _build_url(
            f"college-university/ipeds/sfa-all-undergraduates/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_sfa_ftft(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS student financial aid for first-time, full-time undergraduates.

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(f"college-university/ipeds/sfa-ftft/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_grad_rates(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS graduation rates (150 percent of normal time).

        Args:
            year: Academic year (1996–2022).
        """
        url = _build_url(f"college-university/ipeds/grad-rates/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_grad_rates_200pct(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS graduation rates (200 percent of normal time).

        Args:
            year: Academic year (2007–2022).
        """
        url = _build_url(f"college-university/ipeds/grad-rates-200pct/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_grad_rates_pell(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS graduation rates by type of federal aid (Pell recipients).

        Args:
            year: Academic year (2015–2017).
        """
        url = _build_url(f"college-university/ipeds/grad-rates-pell/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_outcome_measures(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS outcome measures for non-traditional students.

        Args:
            year: Academic year (2015–2021).
        """
        url = _build_url(f"college-university/ipeds/outcome-measures/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_completers(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS number of completers by award level.

        Args:
            year: Academic year (2011–2021).
        """
        url = _build_url(f"college-university/ipeds/completers/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def ipeds_completions_cip_2(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS completions by 2-digit CIP code.

        Args:
            year: Academic year (1991–2022).
        """
        url = _build_url(
            f"college-university/ipeds/completions-cip-2/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_completions_cip_6(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS completions by 6-digit CIP code.

        Args:
            year: Academic year (1983–2022).
        """
        url = _build_url(
            f"college-university/ipeds/completions-cip-6/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_academic_libraries(self, year: int, **kwargs) -> EducationDataResult:
        """IPEDS academic library data.

        Args:
            year: Academic year (2013–2020).
        """
        url = _build_url(
            f"college-university/ipeds/academic-libraries/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_salaries_instructional_staff(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS instructional staff salaries.

        Args:
            year: Academic year (1980, 1984–1999, 2001–2022).
        """
        url = _build_url(
            f"college-university/ipeds/salaries-instructional-staff/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def ipeds_salaries_noninstructional_staff(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """IPEDS noninstructional staff salaries.

        Args:
            year: Academic year (2012–2022).
        """
        url = _build_url(
            f"college-university/ipeds/salaries-noninstructional-staff/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # Colleges — Scorecard
    # ------------------------------------------------------------------

    def scorecard_institutional_characteristics(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """College Scorecard institutional characteristics.

        Args:
            year: Academic year (1996–2020).
        """
        url = _build_url(
            f"college-university/scorecard/institutional-characteristics/{year}/",
            **kwargs,
        )
        return fetch_all_pages(self.session, url)

    def scorecard_student_characteristics(
        self, year: int, variant: str, **kwargs
    ) -> EducationDataResult:
        """College Scorecard student characteristics.

        Args:
            year: Academic year (1997–2016).
            variant: Sub-endpoint. Valid values:
                "aid-applicants", "home-neighborhood".
        """
        valid = {"aid-applicants", "home-neighborhood"}
        if variant not in valid:
            raise ValueError(
                f"Invalid variant {variant!r}. Valid: {sorted(valid)}"
            )
        url = _build_url(
            f"college-university/scorecard/student-characteristics/{year}/{variant}/",
            **kwargs,
        )
        return fetch_all_pages(self.session, url)

    def scorecard_earnings(self, year: int, **kwargs) -> EducationDataResult:
        """College Scorecard post-enrollment earnings.

        Args:
            year: Academic year (2003–2014, 2018).
        """
        url = _build_url(f"college-university/scorecard/earnings/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def scorecard_default(self, year: int, **kwargs) -> EducationDataResult:
        """College Scorecard student loan default rates.

        Args:
            year: Academic year (1996–2020).
        """
        url = _build_url(f"college-university/scorecard/default/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def scorecard_repayment(self, year: int, **kwargs) -> EducationDataResult:
        """College Scorecard student loan repayment rates.

        Args:
            year: Academic year (2007–2016).
        """
        url = _build_url(f"college-university/scorecard/repayment/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # Colleges — NHGIS
    # ------------------------------------------------------------------

    def college_nhgis_geographic_variables(
        self, endpoint: str, year: int, **kwargs
    ) -> EducationDataResult:
        """NHGIS geographic variables joined to college records.

        Args:
            endpoint: Census vintage. Valid values:
                "census-1990", "census-2000", "census-2010", "census-2020".
            year: Academic year (1980, 1984–2023).
        """
        valid_endpoints = {"census-1990", "census-2000", "census-2010", "census-2020"}
        if endpoint not in valid_endpoints:
            raise ValueError(
                f"Invalid endpoint {endpoint!r}. Valid: {sorted(valid_endpoints)}"
            )
        url = _build_url(f"college-university/nhgis/{endpoint}/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # Colleges — FSA
    # ------------------------------------------------------------------

    def fsa_financial_responsibility(self, year: int, **kwargs) -> EducationDataResult:
        """FSA financial responsibility composite scores.

        Args:
            year: Academic year (2006–2016).
        """
        url = _build_url(
            f"college-university/fsa/financial-responsibility/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def fsa_grants(self, year: int, **kwargs) -> EducationDataResult:
        """FSA federal grant aid disbursements.

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(f"college-university/fsa/grants/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def fsa_loans(self, year: int, **kwargs) -> EducationDataResult:
        """FSA federal loan disbursements.

        Args:
            year: Academic year (1999–2021).
        """
        url = _build_url(f"college-university/fsa/loans/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def fsa_campus_based_volume(self, year: int, **kwargs) -> EducationDataResult:
        """FSA campus-based federal aid award volumes.

        Args:
            year: Academic year (2001–2021).
        """
        url = _build_url(
            f"college-university/fsa/campus-based-volume/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def fsa_90_10_revenue(self, year: int, **kwargs) -> EducationDataResult:
        """FSA 90/10 revenue percentages for for-profit institutions.

        Args:
            year: Academic year (2014–2021).
        """
        url = _build_url(
            f"college-university/fsa/90-10-revenue-percentages/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    # ------------------------------------------------------------------
    # Colleges — NACUBO / NCCS / EADA / Campus Crime / PSEO
    # ------------------------------------------------------------------

    def nacubo_endowments(self, year: int, **kwargs) -> EducationDataResult:
        """NACUBO college and university endowments.

        Args:
            year: Academic year (2012–2022).
        """
        url = _build_url(f"college-university/nacubo/endowments/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def nccs_990_forms(self, year: int, **kwargs) -> EducationDataResult:
        """NCCS IRS Form 990 data for nonprofit institutions.

        Args:
            year: Academic year (1993–2016).
        """
        url = _build_url(f"college-university/nccs/990-forms/{year}/", **kwargs)
        return fetch_all_pages(self.session, url)

    def eada_institutional_characteristics(
        self, year: int, **kwargs
    ) -> EducationDataResult:
        """EADA equity in athletics data by institution.

        Args:
            year: Academic year (2002–2021).
        """
        url = _build_url(
            f"college-university/eada/institutional-characteristics/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def campus_crime_hate_crimes(self, year: int, **kwargs) -> EducationDataResult:
        """Campus Safety and Security hate crime incidents.

        Args:
            year: Academic year (2005–2021).
        """
        url = _build_url(
            f"college-university/campus-crime/hate-crimes/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)

    def pseo_earnings_and_flows(self, year: int, **kwargs) -> EducationDataResult:
        """PSEO post-secondary employment outcomes: earnings and flows.

        Args:
            year: Academic year (2001–2021).
        """
        url = _build_url(
            f"college-university/pseo/earnings-and-flows/{year}/", **kwargs
        )
        return fetch_all_pages(self.session, url)
