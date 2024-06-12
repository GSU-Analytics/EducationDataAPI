import requests

class EducationDataAPI:
    """
    A Python client for accessing the Urban Institute's Education Data Portal API.
    See https://educationdata.urban.org/documentation/index.html#how_to_use for more information.

    This client provides methods to access various data endpoints from the API.
    Data returned from methods are in JSON format, which can be further processed
    and transformed into Pandas data frames.
    """

    BASE_URL = "https://educationdata.urban.org/api/v1/"

    def __init__(self):
        """
        Initializes the EducationDataAPI client.
        """
        self.session = requests.Session()

    def get_ccd_directory(self, year, **kwargs):
        """
        Fetches the Common Core of Data (CCD) school directory information for a given year.
        For a list of available specifiers and disaggregators, see the API documentation at
        https://educationdata.urban.org/documentation/schools.html#ccd_directory.

        Args:
            year (int): The year for which data is requested.
            ncessch (str): NCES school ID.
            ncessch_num (int): Numeric NCES school ID.
            school_id (str): School identification number (NCES).
            leaid (str): Local education agency ID.
            state_leaid (str): State-specific local education agency ID.
            seasch (str): State-specific school ID.
            state_location (str): State of location.
            fips (int): Federal Information Processing Standards state code.
            csa (int): Combined statistical area.
            cbsa (int): Core-based statistical area.
            urban_centric_locale (int): Degree of urbanization (urban-centric locale).
            congress_district_id (int): Congressional district ID.
            state_leg_district_lower (str): State legislative district—lower.
            state_leg_district_upper (str): State legislative district—upper.
            school_level (int): School level.
            school_type (int): School type.
            school_status (int): Status at start of school year.
            bureau_indian_education (int): Bureau of Indian Education school.
            title_i_status (int): Title I status.
            title_i_eligible (int): Title I eligibility.
            title_i_schoolwide (int): Schoolwide Title I eligibility.
            charter (int): Charter school status.
            magnet (int): Magnet school status.
            shared_time (int): Shared time status.
            virtual (int): Virtual school status.
            **kwargs: Additional specifiers or disaggregators as keyword arguments.

        Returns:
            dict: The JSON response containing the CCD directory data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_ccd_directory(2013, charter=1, fips=11)
            >>> print(data)  # JSON response
        """
        # Construct the URL with predefined topic, source, and endpoint
        url = f"{self.BASE_URL}schools/ccd/directory/{year}/"
        # If there are any keyword arguments, add them as query parameters
        if kwargs:
            url += '?' + '&'.join(f"{key}={value}" for key, value in kwargs.items())

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_ccd_summary(self, var, stat, by, **kwargs):
        """
        Fetches summary statistics for specified variables from the CCD directory.

        Args:
            var (str): Variable to summarize. Possible values include:
                - latitude
                - longitude
                - county_code
                - lowest_grade_offered
                - highest_grade_offered
                - elem_cedp (Elementary school indicator)
                - middle_cedp (Middle school indicator)
                - high_cedp (High school indicator)
                - ungrade_cedp (Ungraded school indicator)
                - teachers_fte (Full-time equivalent teachers)
                - lunch_program (National School Lunch Program status)
                - free_lunch (Students eligible for free lunch)
                - reduced_price_lunch (Students eligible for reduced-price lunch)
                - free_or_reduced_price_lunch (Students eligible for free or reduced-price lunch)
                - direct_certification (Students eligible for free lunch by direct certification)
                - enrollment (Student enrollment)
            stat (str): Statistical measure to calculate. Possible values include:
                - sum
                - count
                - avg (average)
                - median
                - min (minimum)
                - max (maximum)
                - variance
                - stddev (standard deviation)
            by (str): Categorization or grouping variable. Possible values include:
                - ncessch (NCES school ID)
                - ncessch_num (Numeric NCES school ID)
                - leaid (Local education agency ID)
                - state_leaid (State-specific local education agency ID)
                - seasch (State-specific school ID)
                - state_location
                - fips (Federal Information Processing Standards state code)
                - csa (Combined statistical area)
                - cbsa (Core-based statistical area)
                - urban_centric_locale (Degree of urbanization)
                - congress_district_id
                - school_level
                - school_type
                - school_status
                - bureau_indian_education
                - title_i_status
                - title_i_eligible
                - title_i_schoolwide
                - charter
                - magnet
                - shared_time
                - virtual
            **kwargs: Additional filters or specifiers for refining the summary query. The keys and values are the same as those listed for 'by'.

        Returns:
            dict: The JSON response containing the summary statistics.

        Example:
            # Example 1: Get the standard deviation of student enrollment, categorized by virtual school status.
            >>> api = EducationDataAPI()
            >>> summary1 = api.get_ccd_summary('enrollment', 'stddev', 'virtual')
            >>> print(summary1)

            # Example 2: Calculate the sum of students eligible for free lunch, grouped by state location.
            >>> summary2 = api.get_ccd_summary('free_lunch', 'sum', 'state_location')
            >>> print(summary2)

            # Example 3: Fetch the average number of full-time equivalent teachers, grouped by school level, refining by charter school status.
            >>> summary3 = api.get_ccd_summary('teachers_fte', 'avg', 'school_level', charter=1)
            >>> print(summary3)

            # Example 4: Determine the median of latitude values for schools, categorized by the type of school.
            >>> summary4 = api.get_ccd_summary('latitude', 'median', 'school_type')
            >>> print(summary4)

            # Example 5: Get the maximum number of students eligible for reduced-price lunch, grouped by bureau of Indian education school status.
            >>> summary5 = api.get_ccd_summary('reduced_price_lunch', 'max', 'bureau_indian_education')
            >>> print(summary5)
        """
        # Construct the base URL for summary statistics
        url = f"{self.BASE_URL}schools/ccd/directory/summaries?"
        
        # Add the primary query parameters
        query_params = f"var={var}&stat={stat}&by={by}"
        
        # If there are any keyword arguments, add them as additional query parameters
        if kwargs:
            additional_params = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            query_params += '&' + additional_params
        
        # Finalize the URL
        url += query_params

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_ccd_enrollment(self, year, grade, race=False, sex=False, **kwargs):
        """
        Fetches enrollment data by grade for a specified year, optionally including race and sex segments in the API endpoint,
        and further filtering the data based on additional keyword arguments.

        Args:
            year (int): The academic year (e.g., 2014). Values available from 1986 to 2022.
            grade (int): The grade level (e.g., 8). Special values include -1 for Pre-K through 15 for Ungraded, and 99 for Total.
            race (bool, optional): Include race segment in the API endpoint if True.
            sex (bool, optional): Include sex segment in the API endpoint if True.
            **kwargs: Additional filtering options including:
                - ncessch (str): National Center for Education Statistics (NCES) school ID.
                - ncessch_num (int): Numeric NCES school ID.
                - leaid (str): Local education agency identification number (NCES).
                - fips (int): Federal Information Processing Standards state code. Values range from 1 (Alabama) to 79 (Wake Island), including special categories like 58 for Department of Defense Schools.
                - race (int): Filter by race/ethnicity. Values from 1 (White) to 9 (Unknown), including 20 (Other) and 99 (Total).
                - sex (int): Filter by sex. Values are 1 (Male), 2 (Female), 3 (Gender), 9 (Unknown), and 99 (Total).
                - enrollment (int): Filter by student enrollment count. Special values include -1 (Missing/not reported), -2 (Not applicable), and -3 (Suppressed data).
            
            For a full list of available filters and more detailed information, visit:
            https://educationdata.urban.org/documentation/schools.html#ccd-enrollment-by-grade

        Returns:
            dict: The JSON response containing the enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> enrollment_data = api.get_ccd_enrollment(2014, 8)
            >>> print(enrollment_data)
            >>> filtered_data = api.get_ccd_enrollment(2014, 8, race=True, sex=True, race=1, sex=1)
            >>> print(filtered_data)
        """
        # Construct the URL based on provided arguments
        url = f"{self.BASE_URL}schools/ccd/enrollment/{year}/grade-{grade}/"
        if race and sex:
            url += "race/sex/"
        elif race:
            url += "race/"
        elif sex:
            url += "sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_directory(self, year, **kwargs):
        """
        Fetches the CRDC directory data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2013). Valid years: 2011, 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - school_name_crdc (str): Office of Civil Rights school name.
                - schoolid_crdc (str): 5-digit school ID code.
                - lea_name (str): Local education agency name.
                - leaid_crdc (str): Local education agency ID.
                - lea_state (str): Local education agency state.
                - prek, k, g1, ..., g12, ug (int): Filters for grades from Pre-K to 12 and ungraded.
                - primarily_serve_students_w_dis (int): School primarily serves students with disabilities.
                - charter_crdc (int): Charter school indicator.
                - magnet_crdc (int): Magnet school indicator.
                - entire_school_magnet (int): Entire school is a magnet school.
                - alt_school (int): Alternative school indicator.
                - alt_school_focus (int): Focus of the alternative school.
                - ability_grouped_math_or_eng (int): Students' ability grouped for math or English.
                - ug_elementary_school, ug_middle_school, ug_high_school (int): Ungraded students at different school levels.

                For a full list of available filters and more detailed information, visit:
                https://educationdata.urban.org/documentation/schools.html#crdc_directory
        
        Returns:
            dict: The JSON response containing the directory data.

        Example:
            >>> api = EducationDataAPI()
            >>> directory_data = api.get_crdc_directory(2013, charter_crdc=1)
            >>> print(directory_data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/directory/{year}/"
        
        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_enrollment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC enrollment data for a specified year with optional filters.

        Only the following combinations of boolean flags are allowed:
        - race_segment and sex_segment
        - disability_segment and sex_segment
        - lep_segment and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2013). Valid years: 2011, 2013, 2015, 2017.
            race_segment (bool): Include race segment in the API endpoint if True.
            sex_segment (bool): Include sex segment in the API endpoint if True.
            disability_segment (bool): Include disability segment in the API endpoint if True.
            lep_segment (bool): Include limited English proficiency segment in the API endpoint if True.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - sex (int): Filter by sex. Values are 1 (Male), 2 (Female), 3 (Gender), 9 (Unknown).
                - race (int): Filter by race/ethnicity. Values from 1 (White) to 4 (Asian) and others.
                - disability (int): Filter by students with disabilities. Values from 0 (Students without disabilities) to 3 (Students not served under IDEA).
                - lep (int): Filter by students with limited English proficiency. Values are 1 (Students who are limited English proficient) and 99 (All students).
                - enrollment_crdc (int): Filter by student enrollment count.
                - psenrollment_crdc (int): Number of students enrolled in preschool programs.

                For a full list of available filters and more detailed information, visit:
                https://educationdata.urban.org/documentation/schools.html#crdc-enrollment-by-race-and-sex

        Returns:
            dict: The JSON response containing the enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> enrollment_data = api.get_crdc_enrollment(2013, race_segment=True, sex_segment=True)
            >>> print(enrollment_data)
            >>> filtered_data = api.get_crdc_enrollment(2013, lep_segment=True, sex_segment=True, lep=1, sex=1)
            >>> print(filtered_data)
        """
        # Validate combinations of boolean flags
        if race_segment and not sex_segment:
            raise ValueError("Race can only be combined with sex.")
        if disability_segment and not sex_segment:
            raise ValueError("Disability can only be combined with sex.")
        if lep_segment and not sex_segment:
            raise ValueError("LEP can only be combined with sex.")
        if (race_segment and disability_segment) or (race_segment and lep_segment) or (disability_segment and lep_segment):
            raise ValueError("Only the combinations (race and sex), (disability and sex), and (lep and sex) are allowed.")

        # Construct the URL based on provided arguments
        url = f"{self.BASE_URL}schools/crdc/enrollment/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"
        elif sex_segment:
            url += "sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_discipline(self, year, **kwargs):
        """
        Fetches the CRDC discipline instances data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - disability (int): Filter by students with disabilities. Values are 0 (Students without disabilities), 1 (Students with disabilities served under IDEA), 2 (Students with disabilities served under Section 504 only), 3 (Students not served under IDEA).
                - suspensions_instances (float): Filter by instances of suspensions.
                - suspensions_instances_preschool (float): Filter by instances of suspensions in preschool.
                - corpinstances (float): Filter by instances of corporal punishment.
                - corpinstances_preschool (float): Filter by instances of corporal punishment in preschool.

                For a full list of available filters and more detailed information, visit:
                https://educationdata.urban.org/documentation/schools.html#crdc_discipline-incidents

        Returns:
            dict: The JSON response containing the discipline data.

        Example:
            >>> api = EducationDataAPI()
            >>> discipline_data = api.get_crdc_discipline(2017, fips=1, disability=1)
            >>> print(discipline_data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/discipline-instances/{year}/"
        
        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_discipline_segment(self, year, disability_segment=False, sex_segment=False, race_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC discipline data for a specified year with optional segments and filters.

        Only the following combinations of boolean flags are allowed:
        - disability_segment and sex_segment
        - disability_segment, race_segment, and sex_segment
        - disability_segment, lep_segment, and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2013). Valid years: 2011, 2013, 2015, 2017.
            disability_segment (bool): Include disability segment in the API endpoint if True.
            sex_segment (bool): Include sex segment in the API endpoint if True.
            race_segment (bool): Include race segment in the API endpoint if True.
            lep_segment (bool): Include limited English proficiency segment in the API endpoint if True.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - sex (int): Filter by sex. Values are 1 (Male), 2 (Female), 3 (Gender), 9 (Unknown).
                - race (int): Filter by race/ethnicity. Values from 1 (White) to 4 (Asian) and others.
                - disability (int): Filter by students with disabilities. Values from 0 (Students without disabilities) to 3 (Students not served under IDEA).
                - lep (int): Filter by students with limited English proficiency. Values are 1 (Students who are limited English proficient) and 99 (All students).
                - students_susp_in_sch (int): Students who received one or more in-school suspensions.
                - students_susp_out_sch_single (int): Students who received one out-of-school suspension.
                - students_susp_out_sch_multiple (int): Students who received more than one out-of-school suspension.
                - expulsions_no_ed_serv (int): Number of students expelled without educational services.
                - expulsions_with_ed_serv (int): Number of students expelled with educational services.
                - expulsions_zero_tolerance (int): Number of students expelled under zero-tolerance policies.
                - students_corporal_punish (int): Number of students who received corporal punishment.
                - students_arrested (int): Students who received a school-related arrest.
                - students_referred_law_enforce (int): Students who were referred to a law enforcement agency or official.
                - transfers_alt_sch_disc (float): Students who were transferred to an alternative school for disciplinary reasons.
                - revised_flag (int): Flag indicating if arrests variable has been revised by Office of Civil Rights.

        Returns:
            dict: The JSON response containing the discipline data.

        Example:
            >>> api = EducationDataAPI()
            >>> discipline_data = api.get_crdc_discipline_segment(2013, disability_segment=True, sex_segment=True)
            >>> print(discipline_data)
            >>> filtered_data = api.get_crdc_discipline_segment(2013, disability_segment=True, race_segment=True, sex_segment=True, fips=1)
            >>> print(filtered_data)
        """
        # Validate combinations of boolean flags
        if disability_segment and not sex_segment:
            raise ValueError("Disability can only be combined with sex.")
        if race_segment and not (disability_segment and sex_segment):
            raise ValueError("Race can only be combined with disability and sex.")
        if lep_segment and not (disability_segment and sex_segment):
            raise ValueError("LEP can only be combined with disability and sex.")
        if (race_segment and lep_segment):
            raise ValueError("Race and LEP cannot be combined together.")
        if not (disability_segment and sex_segment):
            raise ValueError("At least disability and sex must be combined.")

        # Construct the URL based on provided arguments
        url = f"{self.BASE_URL}schools/crdc/discipline/{year}/"
        if disability_segment and sex_segment and race_segment:
            url += "disability/race/sex/"
        elif disability_segment and sex_segment and lep_segment:
            url += "disability/lep/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()