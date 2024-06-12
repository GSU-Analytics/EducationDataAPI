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

    def get_metadata_endpoints(self):
        """
        Fetches the general information about each endpoint.

        Returns:
            dict: The JSON response containing information about each endpoint.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_metadata_endpoints()
            >>> print(data)
        """
        url = f"{self.BASE_URL}api-endpoints"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_metadata_downloads(self):
        """
        Fetches information about downloadable data files and codebooks for each endpoint.

        Returns:
            dict: The JSON response containing information about downloadable data files and codebooks.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_metadata_downloads()
            >>> print(data)
        """
        url = f"{self.BASE_URL}api-downloads"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_metadata_variables(self):
        """
        Fetches information about each variable in the portal.

        Returns:
            dict: The JSON response containing information about each variable in the portal.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_metadata_variables()
            >>> print(data)
        """
        url = f"{self.BASE_URL}api-variables"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_metadata_endpoint_varlist(self):
        """
        Fetches information about each variable in the portal, broken out by endpoint.

        Returns:
            dict: The JSON response containing information about each variable broken out by endpoint.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_metadata_endpoint_varlist()
            >>> print(data)
        """
        url = f"{self.BASE_URL}api-endpoint-varlist"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

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
    
    def get_crdc_bullying_allegations(self, year, **kwargs):
        """
        Fetches the CRDC allegations of harassment or bullying data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2015). Valid years: 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - allegations_harass_sex (int): Number of allegations of harassment or bullying on the basis of sex.
                - allegations_harass_race (int): Number of allegations of harassment or bullying on the basis of race, color, or national origin.
                - allegations_harass_disability (int): Number of allegations of harassment or bullying on the basis of disability.
                - allegations_harass_orientation (int): Number of allegations of harassment or bullying on the basis of sexual orientation.
                - allegations_harass_religion (int): Number of allegations of harassment or bullying on the basis of religion.

                For a full list of available filters and more detailed information, visit:
                https://educationdata.urban.org/documentation/schools.html#crdc-harassment-or-bullying-allegations

        Returns:
            dict: The JSON response containing the allegations data.

        Example:
            >>> api = EducationDataAPI()
            >>> bullying_data = api.get_crdc_bullying_allegations(2015, fips=1, allegations_harass_sex=10)
            >>> print(bullying_data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/harassment-or-bullying/{year}/allegations/"
        
        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status() 
        return response.json()
    
    def get_crdc_bullying_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC bullying and harassment data for a specified year with optional segments and filters.

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
                - students_disc_harass_dis (int): Number of students disciplined for bullying or harassment on the basis of disability.
                - students_disc_harass_race (int): Number of students disciplined for bullying or harassment on the basis of race, color, or national origin.
                - students_disc_harass_sex (int): Number of students disciplined for bullying or harassment on the basis of sex.
                - students_report_harass_dis (int): Number of students harassed or bullied on the basis of disability.
                - students_report_harass_race (int): Number of students harassed or bullied on the basis of race, color, or national origin.
                - students_report_harass_sex (int): Number of students harassed or bullied on the basis of sex.

        Returns:
            dict: The JSON response containing the bullying and harassment data.

        Example:
            >>> api = EducationDataAPI()
            >>> bullying_data = api.get_crdc_bullying_segment(2013, race_segment=True, sex_segment=True)
            >>> print(bullying_data)
            >>> filtered_data = api.get_crdc_bullying_segment(2013, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/harassment-or-bullying/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_absenteeism_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC chronic absenteeism data for a specified year with optional segments and filters.

        Only the following combinations of boolean flags are allowed:
        - race_segment and sex_segment
        - disability_segment and sex_segment
        - lep_segment and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2013). Valid years: 2013, 2015.
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
                - students_chronically_absent (int): Number of chronically absent students.

        Returns:
            dict: The JSON response containing the chronic absenteeism data.

        Example:
            >>> api = EducationDataAPI()
            >>> absenteeism_data = api.get_crdc_absenteeism_segment(2013, race_segment=True, sex_segment=True)
            >>> print(absenteeism_data)
            >>> filtered_data = api.get_crdc_absenteeism_segment(2015, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/chronic-absenteeism/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_restraint_instances(self, year, **kwargs):
        """
        Fetches the CRDC restraint and seclusion instances data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2015). Valid years: 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - disability (int): Filter by students with disabilities. Values are 0 (Students without disabilities), 1 (Students with disabilities served under IDEA), 2 (Students with disabilities served under Section 504 only), 3 (Students not served under IDEA).
                - instances_mech_restraint (int): Number of instances of mechanical restraint.
                - instances_phys_restraint (int): Number of instances of physical restraint.
                - instances_seclusion (int): Number of instances of seclusion.

        Returns:
            dict: The JSON response containing the restraint and seclusion data.

        Example:
            >>> api = EducationDataAPI()
            >>> restraint_data = api.get_crdc_restraint_instances(2015, fips=1, disability=1)
            >>> print(restraint_data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/restraint-and-seclusion/{year}/instances/"
        
        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_restraint_segment(self, year, disability_segment=False, sex_segment=False, race_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC restraint and seclusion data for a specified year with optional segments and filters.

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
                - students_mech_restraint (int): Number of students subjected to mechanical restraint.
                - students_phys_restraint (int): Number of students subjected to physical restraint.
                - students_seclusion (int): Number of students subjected to seclusion.

        Returns:
            dict: The JSON response containing the restraint and seclusion data.

        Example:
            >>> api = EducationDataAPI()
            >>> restraint_data = api.get_crdc_restraint_segment(2013, disability_segment=True, sex_segment=True)
            >>> print(restraint_data)
            >>> filtered_data = api.get_crdc_restraint_segment(2015, disability_segment=True, race_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/restraint-and-seclusion/{year}/"
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
    
    def get_crdc_advanced_enrollment_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC advanced enrollment data for a specified year with optional segments and filters.

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
                - enrl_IB (int): Students enrolled in the International Baccalaureate Diploma Program.
                - enrl_gifted_talented (int): Students who are enrolled in the gifted and talented programs.
                - enrl_AP (int): Students enrolled in at least one Advanced Placement (AP) course.
                - enrl_AP_science (int): Students enrolled in at least one AP science course.
                - enrl_AP_math (int): Students enrolled in at least one AP mathematics course.
                - enrl_AP_other (int): Students enrolled in at least one 'other' AP course (e.g., foreign language, computer science).
                - enrl_AP_language (int): Students enrolled in one or more AP language courses.

        Returns:
            dict: The JSON response containing the advanced enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> advanced_enrollment_data = api.get_crdc_advanced_enrollment_segment(2013, race_segment=True, sex_segment=True)
            >>> print(advanced_enrollment_data)
            >>> filtered_data = api.get_crdc_advanced_enrollment_segment(2015, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/ap-ib-enrollment/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_ap_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC AP exam data for a specified year with optional segments and filters.

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
                - students_AP_exam_none (int): Students who took no AP exams.
                - students_AP_pass_none (int): Students who did not receive a qualifying score on any AP exams.
                - students_AP_exam_oneormore (int): Students who took one or more AP exams.
                - students_AP_pass_oneormore (int): Students who received a qualifying score on one or more AP exams.
                - students_AP_exam_all (int): Students who took exams for all AP courses enrolled.
                - students_AP_pass_all (int): Students who received a qualifying score in all AP exams.

        Returns:
            dict: The JSON response containing the AP exam data.

        Example:
            >>> api = EducationDataAPI()
            >>> ap_data = api.get_ap_segment(2013, race_segment=True, sex_segment=True)
            >>> print(ap_data)
            >>> filtered_data = api.get_ap_segment(2015, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/ap-exams/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_college_exam_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC college exam data for a specified year with optional segments and filters.

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
                - students_SAT_ACT (int): Students participating in the SAT and ACT tests.

        Returns:
            dict: The JSON response containing the college exam data.

        Example:
            >>> api = EducationDataAPI()
            >>> college_exam_data = api.get_crdc_collage_exam_segment(2013, race_segment=True, sex_segment=True)
            >>> print(college_exam_data)
            >>> filtered_data = api.get_crdc_collage_exam_segment(2015, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/sat-act-participation/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_staff(self, year, **kwargs):
        """
        Fetches the CRDC teachers and staff data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2015). Valid years: 2011, 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - teachers_fte_crdc (int): Number of full-time equivalent teachers (Civil Rights Data Collection).
                - teachers_certified_fte (float): Number of full-time equivalent certified teachers.
                - teachers_uncertified_fte (float): Number of full-time equivalent uncertified teachers.
                - teachers_first_year_fte (float): Number of full-time equivalent first-year teachers.
                - teachers_second_year_fte (float): Number of full-time equivalent second-year teachers.
                - teachers_current_sy (float): Number of current school year teachers.
                - teachers_previous_sy (float): Number of previous school year teachers.
                - teachers_absent_fte (float): Number of full-time equivalent teachers absent more than 10 school days.
                - counselors_fte (float): Number of full-time equivalent school counselors.
                - social_workers_fte (float): Number of full-time equivalent social workers.
                - psychologists_fte (float): Number of full-time equivalent psychologists.
                - nurses_fte (float): Number of full-time equivalent nurses.
                - law_enforcement_fte (float): Number of full-time equivalent sworn law enforcement officers.
                - security_guard_fte (float): Number of full-time equivalent security guards.
                - law_enforcement_ind (int): Sworn law enforcement officers indicator (0—No, 1—Yes).

        Returns:
            dict: The JSON response containing the teachers and staff data.

        Example:
            >>> api = EducationDataAPI()
            >>> staff_data = api.get_crdc_staff(2015, fips=1)
            >>> print(staff_data)
        """
        # Construct the URL based on provided arguments
        url = f"{self.BASE_URL}schools/crdc/teachers-staff/{year}/"
        
        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_math_science_enrollment_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC math and science enrollment data for a specified year with optional segments and filters.

        Only the following combinations of boolean flags are allowed:
        - race_segment and sex_segment
        - disability_segment and sex_segment
        - lep_segment and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2011, 2013, 2015, 2017.
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
                - enrl_biology (int): Students enrolled in biology.
                - enrl_chemistry (int): Students enrolled in chemistry.
                - enrl_advanced_math (int): Students enrolled in advanced mathematics.
                - enrl_calculus (int): Students enrolled in calculus.
                - enrl_algebra2 (int): Students enrolled in algebra II.
                - enrl_physics (int): Students enrolled in physics.
                - enrl_geometry (int): Students enrolled in geometry.

        Returns:
            dict: The JSON response containing the math and science enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> math_science_data = api.get_crdc_math_science_enrollment_segment(2017, race_segment=True, sex_segment=True)
            >>> print(math_science_data)
            >>> filtered_data = api.get_crdc_math_science_enrollment_segment(2017, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/math-and-science/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_crdc_algebra_enrollment_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC Algebra I enrollment data for a specified year with optional segments and filters.

        Only the following combinations of boolean flags are allowed:
        - race_segment and sex_segment
        - disability_segment and sex_segment
        - lep_segment and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2011, 2013, 2015, 2017.
            race_segment (bool): Include race segment in the API endpoint if True.
            sex_segment (bool): Include sex segment in the API endpoint if True.
            disability_segment (bool): Include disability segment in the API endpoint if True.
            lep_segment (bool): Include limited English proficiency segment in the API endpoint if True.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - grade_crdc (int): Grade. Values are 20 (Grades 7 and 8), 21 (Grades 9 and 10), 22 (Grades 11 and 12), 99 (Total).
                - race (int): Filter by race/ethnicity. Values from 1 (White) to 4 (Asian) and others.
                - sex (int): Filter by sex. Values are 1 (Male), 2 (Female), 3 (Gender), 9 (Unknown).
                - disability (int): Filter by students with disabilities. Values from 0 (Students without disabilities) to 3 (Students not served under IDEA).
                - lep (int): Filter by students with limited English proficiency. Values are 1 (Students who are limited English proficient) and 99 (All students).
                - enrl_algebra1 (int): Students enrolled in Algebra I.
                - students_passing_algebra1 (int): Students passing Algebra I.

        Returns:
            dict: The JSON response containing the Algebra I enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> algebra_data = api.get_crdc_algebra_enrollment_segment(2017, race_segment=True, sex_segment=True)
            >>> print(algebra_data)
            >>> filtered_data = api.get_crdc_algebra_enrollment_segment(2017, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/algebra1/{year}/"
        if race_segment and sex_segment:
            url += "race/sex/"
        elif disability_segment and sex_segment:
            url += "disability/sex/"
        elif lep_segment and sex_segment:
            url += "lep/sex/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_offenses(self, year, **kwargs):
        """
        Fetches the CRDC offenses data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - firearm_incident_ind (int): At least one incident at the school involved a shooting. Values: 0 (No), 1 (Yes).
                - homicide_ind (int): A student, faculty, or staff member died as a result of a homicide committed at the school. Values: 0 (No), 1 (Yes).
                - rape_incidents (float): Incidents of rape or attempted rape.
                - sexual_battery_incidents (float): Incidents of sexual assault (other than rape).
                - robbery_w_weapon_incidents (float): Incidents of robbery with a weapon.
                - robbery_w_firearm_incidents (float): Incidents of robbery with a firearm or explosive device.
                - robbery_no_weapon_incidents (float): Incidents of robbery without a weapon.
                - attack_w_weapon_incidents (float): Incidents of physical attack or fight with a weapon.
                - attack_w_firearm_incidents (float): Incidents of physical attack or fight with a firearm or explosive device.
                - attack_no_weapon_incidents (float): Incidents of physical attack or fight without a weapon.
                - threats_w_weapon_incidents (float): Incidents of threats of physical attack with a weapon.
                - threats_w_firearm_incidents (float): Incidents of threats of physical attack with a firearm or explosive device.
                - threats_no_weapon_incidents (float): Incidents of threats of physical attack without a weapon.
                - possession_firearm_incidents (float): Incidents of possession of a firearm or explosive device.

        Returns:
            dict: The JSON response containing the offenses data.

        Example:
            >>> api = EducationDataAPI()
            >>> offenses_data = api.get_crdc_offenses(2017, fips=1, firearm_incident_ind=1)
            >>> print(offenses_data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/offenses/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_crdc_dual_enrollment_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC dual enrollment data for a specified year with optional segments and filters.

        Only the following combinations of boolean flags are allowed:
        - race_segment and sex_segment
        - disability_segment and sex_segment
        - lep_segment and sex_segment

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2015, 2017.
            race_segment (bool): Include race segment in the API endpoint if True.
            sex_segment (bool): Include sex segment in the API endpoint if True.
            disability_segment (bool): Include disability segment in the API endpoint if True.
            lep_segment (bool): Include limited English proficiency segment in the API endpoint if True.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Filter by race/ethnicity. Values from 1 (White) to 4 (Asian) and others.
                - sex (int): Filter by sex. Values are 1 (Male), 2 (Female), 3 (Gender), 9 (Unknown).
                - disability (int): Filter by students with disabilities. Values from 0 (Students without disabilities) to 3 (Students not served under IDEA).
                - lep (int): Filter by students with limited English proficiency. Values are 1 (Students who are limited English proficient) and 99 (All students).
                - enrl_dual_enrollment (float): Number of students enrolled in a dual enrollment or dual credit program.

        Returns:
            dict: The JSON response containing the dual enrollment data.

        Example:
            >>> api = EducationDataAPI()
            >>> dual_enrollment_data = api.get_crdc_dual_enrollment_segment(2017, race_segment=True, sex_segment=True)
            >>> print(dual_enrollment_data)
            >>> filtered_data = api.get_crdc_dual_enrollment_segment(2017, disability_segment=True, sex_segment=True, fips=1)
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
        url = f"{self.BASE_URL}schools/crdc/dual-enrollment/{year}/"
        if race_segment and sex_segment:
            url += "race/sex"
        elif disability_segment and sex_segment:
            url += "disability/sex"
        elif lep_segment and sex_segment:
            url += "lep/sex"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_credit_recovery(self, year, **kwargs):
        """
        Fetches the CRDC credit recovery data for a specified year with optional filters.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - credit_recovery_offered (int): School has students who participate in credit recovery programs. Values: 0 (No), 1 (Yes).
                - enrl_credit_recovery (float): Number of students who participate in credit recovery programs.

        Returns:
            dict: The JSON response containing the credit recovery data.

        Example:
            >>> api = EducationDataAPI()
            >>> credit_recovery_data = api.get_crdc_credit_recovery(2017, fips=1)
            >>> print(credit_recovery_data)
        """
        # Construct the URL based on provided arguments
        url = f"{self.BASE_URL}schools/crdc/credit-recovery/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_days_suspended_segment(self, year, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC days suspended data for a specified year segmented by the specified segments.

        The possible segment combinations are:
        - race and sex
        - disability and sex
        - LEP and sex

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2015, 2017.
            race_segment (bool): Segment by race.
            sex_segment (bool): Segment by sex.
            disability_segment (bool): Segment by disability.
            lep_segment (bool): Segment by limited English proficiency (LEP).
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Race/ethnicity filter.
                - sex (int): Sex filter.
                - disability (int): Students with disabilities filter.
                - lep (int): Limited English proficiency filter.
                - days_suspended (float): Number of days missed due to suspension.

        Returns:
            dict: The JSON response containing the days suspended data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_crdc_days_suspended_segment(2017, race_segment=True, sex_segment=True, fips=1)
            >>> print(data)
        """
        # Validate segment combinations
        if (race_segment and sex_segment and not disability_segment and not lep_segment) or \
           (disability_segment and sex_segment and not race_segment and not lep_segment) or \
           (lep_segment and sex_segment and not race_segment and not disability_segment):
            if race_segment and sex_segment:
                segments = "race/sex"
            elif disability_segment and sex_segment:
                segments = "disability/sex"
            elif lep_segment and sex_segment:
                segments = "lep/sex"
        else:
            raise ValueError("Invalid segment combination. Valid combinations are: race and sex, disability and sex, LEP and sex.")

        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/suspensions-days/{year}/{segments}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_crdc_offerings(self, year, **kwargs):
        """
        Fetches the CRDC offerings data for a specified year.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2011, 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - num_classes_algebra1 (float): Number of algebra I classes.
                - num_taught_certified_algebra1 (float): Number of algebra I classes taught by a certified teacher.
                - num_classes_algebra2 (float): Number of algebra II classes.
                - num_taught_certified_algebra2 (float): Number of algebra II classes taught by a certified teacher.
                - num_classes_advanced_math (float): Number of advanced math classes.
                - num_taught_certified_adv_math (float): Number of advanced math classes taught by a certified teacher.
                - num_classes_calculus (float): Number of calculus classes.
                - num_taught_certified_calculus (float): Number of calculus classes taught by a certified teacher.
                - num_classes_biology (float): Number of biology classes.
                - num_taught_certified_biology (float): Number of biology classes taught by a certified teacher.
                - num_classes_chemistry (float): Number of chemistry classes.
                - num_taught_certified_chemistry (float): Number of chemistry classes taught by a certified teacher.
                - num_classes_geometry (float): Number of geometry classes.
                - num_taught_certified_geometry (float): Number of geometry classes taught by a certified teacher.
                - num_classes_physics (float): Number of physics classes.
                - num_taught_certified_physics (float): Number of physics classes taught by a certified teacher.
                - ap_courses_indicator (int): Advanced Placement program indicator.
                - num_courses_ap (float): Number of Advanced Placement courses.
                - students_select_ap_indicator (int): Advanced Placement course self-selection indicator.
                - ap_courses_math_indicator (int): Advanced Placement mathematics enrollment indicator.
                - ap_courses_science_indicator (int): Advanced Placement science enrollment indicator.
                - ap_courses_other_indicator (int): Advanced Placement other subjects enrollment indicator.
                - sch_dual_indicator (int): School has students participating in a dual enrollment program.
                - gifted_talented_indicator (int): Gifted and talented education program indicator.
                - sports_single_sex_indicator (int): Single-sex interscholastic athletics indicator.
                - sports_single_sex_m (int): Number of male-only interscholastic sports.
                - sports_single_sex_f (int): Number of female-only interscholastic sports.
                - teams_single_sex_m (int): Number of male-only interscholastic sports teams.
                - teams_single_sex_f (int): Number of female-only interscholastic sports teams.
                - participants_single_sex_sports_m (int): Number of male participants in single-sex interscholastic athletics.
                - participants_single_sex_sports_f (int): Number of female participants in single-sex interscholastic athletics.
                - participants_single_sex_sports (int): Number of participants in single-sex interscholastic athletics.
                - classes_single_sex_indicator (int): Single-sex academic classes indicator.
                - classes_single_sex_alg_geom_m (int): Number of algebra I, geometry, and algebra II classes for males only.
                - classes_single_sex_alg_geom_f (int): Number of algebra I, geometry, and algebra II classes for females only.
                - classes_single_sex_alg_geom (int): Number of single-sex algebra I, geometry, and algebra II classes.
                - classes_single_sex_othermath_m (int): Number of other mathematics classes for males only.
                - classes_single_sex_othermath_f (int): Number of other mathematics classes for females only.
                - classes_single_sex_othermath (int): Number of other single-sex mathematics classes.
                - classes_single_sex_science_m (int): Number of science classes for males only.
                - classes_single_sex_science_f (int): Number of science classes for females only.
                - classes_single_sex_science (int): Number of single-sex science classes.
                - classes_single_sex_english_m (int): Number of English classes for males only.
                - classes_single_sex_english_f (int): Number of English classes for females only.
                - classes_single_sex_english (int): Number of single-sex English classes.
                - classes_single_sex_other_m (int): Number of other classes for males only.
                - classes_single_sex_other_f (int): Number of other classes for females only.
                - classes_single_sex_other (int): Number of other single-sex classes.

        Returns:
            dict: The JSON response containing the offerings data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_crdc_offerings(2017, fips=1, num_classes_algebra1=5)
            >>> print(data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/offerings/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()

    def get_crdc_school_finance(self, year, **kwargs):
        """
        Fetches the CRDC school finance data for a specified year.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2011, 2013, 2015, 2017.
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - salaries_teachers (int): Personnel salaries at school level— teachers only—amount.
                - salaries_total (float): Total salary amount.
                - salaries_instruc_staff (int): Personnel salaries at school level—instructional staff only.
                - salaries_instructional_aides (float): Salary expenditure for instructional aides funded with state and local funds.
                - salaries_support (float): Salary expenditure for support staff funded with state and local funds.
                - salaries_administration (float): Salary expenditure for administration staff funded with state and local funds.
                - expenditures_nonpersonnel (int): Non-personnel expenditures at school level.
                - instructional_aides_fte (float): Number of full-time equivalent instructional aides or paraprofessionals.
                - support_fte (float): Number of support staff.
                - administration_fte (float): Number of school administration staff.

        Returns:
            dict: The JSON response containing the school finance data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_crdc_school_finance(2017, fips=1, salaries_teachers=500000)
            >>> print(data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/school-finance/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_crdc_retention_segment(self, year, grade, race_segment=False, sex_segment=False, disability_segment=False, lep_segment=False, **kwargs):
        """
        Fetches the CRDC retention data for a specified year and grade, segmented by race, sex, disability, and LEP.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2011, 2013, 2015, 2017.
            grade (int): The grade for which data is requested. Special values: -1—Pre-K, 0—Kindergarten, 1—1, 2—2, etc.
            race_segment (bool): Whether to segment by race.
            sex_segment (bool): Whether to segment by sex.
            disability_segment (bool): Whether to segment by disability.
            lep_segment (bool): Whether to segment by limited English proficiency (LEP).
            **kwargs: Additional filtering options including:
                - crdc_id (str): Office of Civil Rights school ID.
                - ncessch (str): NCES school ID.
                - leaid (str): Local education agency ID (NCES).
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Race/ethnicity of students.
                - sex (int): Sex of students.
                - disability (int): Disability status of students.
                - lep (int): Limited English proficiency status of students.

        Returns:
            dict: The JSON response containing the retention data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_crdc_retention_segment(2017, 3, race_segment=True, sex_segment=True)
            >>> print(data)
        """
        # Check for valid segment combinations
        if race_segment and sex_segment and not (disability_segment or lep_segment):
            segments = "race/sex"
        elif disability_segment and sex_segment and not (race_segment or lep_segment):
            segments = "disability/sex"
        elif lep_segment and sex_segment and not (race_segment or disability_segment):
            segments = "lep/sex"
        else:
            raise ValueError("Invalid segment combination. Valid combinations are: race and sex, disability and sex, LEP and sex.")

        # Construct the URL
        url = f"{self.BASE_URL}schools/crdc/retention/{year}/grade-{grade}/{segments}"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_edfacts_state_assessments(self, year, grade_edfacts, **kwargs):
        """
        Fetches the EDFacts state assessments data for a specified year and grade.

        Args:
            year (int): The academic year for which data is requested (e.g., 2014). Valid years: 2009–2018, 2020.
            grade_edfacts (int): The grade category as reported in EDFacts. Special values: 3—3, 4—4, 5—5, 6—6, etc.
            **kwargs: Additional filtering options including:
                - ncessch (str): NCES school ID.
                - ncessch_num (int): NCES school ID (numeric).
                - school_name (str): School name.
                - leaid (str): Local education agency ID (NCES).
                - leaid_num (int): Local education agency ID (NCES) (numeric).
                - lea_name (str): Local education agency name.
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Race/ethnicity of students.
                - sex (int): Sex of students.
                - lep (int): Limited English proficiency status of students.
                - homeless (int): Homeless status of students.
                - migrant (int): Migrant status of students.
                - disability (int): Disability status of students.
                - econ_disadvantaged (int): Economic disadvantage status of students.
                - foster_care (int): Foster care status of students.
                - military_connected (int): Military connection status of students.
                - read_test_num_valid (int): Number of students who completed a reading or language arts assessment.
                - read_test_pct_prof_midpt (float): Midpoint of the proficiency share range for reading or language arts assessment.
                - read_test_pct_prof_high (int): High end of the proficiency share range for reading or language arts assessment.
                - read_test_pct_prof_low (int): Low end of the proficiency share range for reading or language arts assessment.
                - math_test_num_valid (int): Number of students who completed a mathematics assessment.
                - math_test_pct_prof_midpt (float): Midpoint of the proficiency share range for mathematics assessment.
                - math_test_pct_prof_high (int): High end of the proficiency share range for mathematics assessment.
                - math_test_pct_prof_low (int): Low end of the proficiency share range for mathematics assessment.

        Returns:
            dict: The JSON response containing the state assessments data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_edfacts_state_assessments(2014, 8, fips=1, race=1)
            >>> print(data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/edfacts/assessments/{year}/grade-{grade_edfacts}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_edfacts_state_assessment_segment(self, year, grade_edfacts, segment, **kwargs):
        """
        Fetches the EDFacts state assessments data for a specified year, grade, and segment.

        Args:
            year (int): The academic year for which data is requested (e.g., 2014). Valid years: 2009-2018, 2020.
            grade_edfacts (int): The grade category as reported in EDFacts.
            segment (str): The segment for the data. Possible values: "race", "sex", "special-populations".
            **kwargs: Additional filtering options including:
                - ncessch (str): NCES school ID.
                - ncessch_num (int): NCES school ID (numeric).
                - school_name (str): School name.
                - leaid (str): Local education agency ID (NCES).
                - leaid_num (int): Local education agency ID (NCES) (numeric).
                - lea_name (str): Local education agency name.
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Race/ethnicity of students.
                - sex (int): Sex of students.
                - lep (int): Limited English proficiency status of students.
                - homeless (int): Homeless status of students.
                - migrant (int): Migrant status of students.
                - disability (int): Disability status of students.
                - econ_disadvantaged (int): Economic disadvantage status of students.
                - foster_care (int): Foster care status of students.
                - military_connected (int): Military connection status of students.
                - read_test_num_valid (int): Number of students who completed a reading or language arts assessment.
                - read_test_pct_prof_midpt (float): Midpoint of the proficiency share range for reading or language arts assessment.
                - read_test_pct_prof_high (int): High end of the proficiency share range for reading or language arts assessment.
                - read_test_pct_prof_low (int): Low end of the proficiency share range for reading or language arts assessment.
                - math_test_num_valid (int): Number of students who completed a mathematics assessment.
                - math_test_pct_prof_midpt (float): Midpoint of the proficiency share range for mathematics assessment.
                - math_test_pct_prof_high (int): High end of the proficiency share range for mathematics assessment.
                - math_test_pct_prof_low (int): Low end of the proficiency share range for mathematics assessment.

        Returns:
            dict: The JSON response containing the state assessments data.

        Raises:
            ValueError: If the segment is not one of "race", "sex", or "special-populations".

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_edfacts_state_assessment_segment(2014, 8, "race", fips=1, race=1)
            >>> print(data)
        """
        valid_segments = ["race", "sex", "special-populations"]
        if segment not in valid_segments:
            raise ValueError(f"Invalid segment: {segment}. Valid segments are: {', '.join(valid_segments)}")

        # Construct the URL
        url = f"{self.BASE_URL}schools/edfacts/assessments/{year}/grade-{grade_edfacts}/{segment}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_edfacts_adjust_grad_rates(self, year, **kwargs):
        """
        Fetches the EDFacts adjusted cohort graduation rates data for a specified year.

        Args:
            year (int): The academic year for which data is requested (e.g., 2014). Valid years: 2010–2019.
            **kwargs: Additional filtering options including:
                - ncessch (str): NCES school ID.
                - ncessch_num (int): NCES school ID (numeric).
                - school_name (str): School name.
                - leaid (str): Local education agency ID (NCES).
                - leaid_num (int): Local education agency ID (NCES) (numeric).
                - lea_name (str): Local education agency name.
                - fips (int): Federal Information Processing Standards state code.
                - race (int): Race/ethnicity of students.
                - lep (int): Limited English proficiency status of students.
                - homeless (int): Homeless status of students.
                - disability (int): Disability status of students.
                - econ_disadvantaged (int): Economic disadvantage status of students.
                - foster_care (int): Foster care status of students.
                - cohort_num (int): Students in the adjusted cohort graduation rate cohort.
                - grad_rate_low (int): Low end of the high school graduation rate range (0–100 scale).
                - grad_rate_high (int): High end of the high school graduation rate range (0–100 scale).
                - grad_rate_midpt (int): Midpoint of the high school graduation rate range (0–100 scale).

        Returns:
            dict: The JSON response containing the adjusted cohort graduation rates data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_edfacts_adjust_grad_rates(2014, fips=1, race=1)
            >>> print(data)
        """
        # Construct the URL
        url = f"{self.BASE_URL}schools/edfacts/grad-rates/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_nhgis_geographic_variables(self, endpoint, year, **kwargs):
        """
        Fetches the NHGIS geographic variables data for a specified year and endpoint.

        Args:
            endpoint (str): The NHGIS endpoint to use (e.g., 'census-2010', 'census-2000', 'census-1990').
            year (int): The academic year for which data is requested (e.g., 2016). Valid years: 1986–2021.
            **kwargs: Additional filtering options including:
                - ncessch (str): NCES school ID.
                - fips (int): Federal Information Processing Standards state code.
                - school_id (str): School identification number (NCES).
                - school_name (str): School name.
                - leaid (str): Local education agency identification number (NCES).
                - street_mailing (str): Street of mailing address.
                - city_mailing (str): City of mailing address.
                - state_mailing (str): State of mailing address.
                - zip_mailing (str): Zip code of mailing address.
                - street_location (str): Street of location.
                - city_location (str): City of location.
                - state_location (str): State of location.
                - zip_location (str): Zip code of location.
                - latitude (float): Latitude of institution.
                - longitude (float): Longitude of institution.
                - county_code (int): County code.
                - congress_district_id (int): State and 114th congressional district identification number.
                - gleaid (str): Geographic local education agency identification number.
                - geo_longitude (float): Geocoded longitude of institution.
                - geo_latitude (float): Geocoded latitude of institution.
                - geocode_accuracy (int): Accuracy of geocode match.
                - geocode_accuracy_detailed (int): Type of geocode match.
                - state_fips_geo (int): Federal Information Processing Standards state code.
                - county_fips_geo (int): Federal Information Processing Standards county code.
                - puma (str): Public Use Microdata Area identifier.
                - tract (int): Census tract.
                - block_group (int): Block group number.
                - geoid_block (str): Block identifier.
                - census_region (int): Census Bureau region.
                - census_division (int): Census Bureau division.
                - csa (int): Combined statistical area.
                - cbsa (int): Core-based statistical area.
                - cbsa_name (str): Core-based statistical area name.
                - cbsa_type (int): Core-based statistical area type: Metropolitan or micropolitan.
                - cbsa_city (int): Metropolitan or micropolitan statistical area (yes/no).
                - place_fips (int): Federal Information Processing Standards place code.
                - geoid_place (str): Place identifier.
                - place_name (str): Place name.
                - class_code (int): Federal Information Processing Standards class code.
                - upper_chamber (str): State legislative district upper chamber code.
                - state_leg_district_upper (str): State legislative district—upper.
                - upper_chamber_name (str): State upper chamber name.
                - lower_chamber (str): State legislative district lower chamber code.
                - state_leg_district_lower (str): State legislative district—lower.
                - lower_chamber_name (str): State lower chamber name.
                - lower_chamber_type (int): Legal or statistical area description code for state legislative district lower chamber.

        Returns:
            dict: The JSON response containing the NHGIS geographic variables data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_nhgis_geographic_variables('census-2010', 2016, fips=1)
            >>> print(data)
        """
        # Validate endpoint
        valid_endpoints = ['census-2010', 'census-2000', 'census-1990']
        if endpoint not in valid_endpoints:
            raise ValueError(f"Invalid endpoint. Valid endpoints are: {valid_endpoints}")

        # Construct the URL
        url = f"{self.BASE_URL}schools/nhgis/{endpoint}/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()
    
    def get_meps_school_poverty(self, year, **kwargs):
        """
        Fetches the MEPS school poverty data for a specified year.

        Args:
            year (int): The academic year for which data is requested (e.g., 2017). Valid years: 2013–2020.
            **kwargs: Additional filtering options including:
                - ncessch (str): NCES school ID.
                - ncessch_num (int): NCES school ID (numeric).
                - leaid (str): Local education agency identification number (NCES).
                - gleaid (str): Geographic local education agency identification number.
                - fips (int): Federal Information Processing Standards state code.

        Returns:
            dict: The JSON response containing the MEPS school poverty data.

        Example:
            >>> api = EducationDataAPI()
            >>> data = api.get_meps_school_poverty(2017, fips=1)
            >>> print(data)
        """
        # Validate year
        if year not in range(2013, 2021):
            raise ValueError("Invalid year. Valid years are from 2013 to 2020.")

        # Construct the URL
        url = f"{self.BASE_URL}schools/meps/{year}/"

        # Append additional query parameters
        if kwargs:
            query_string = '&'.join(f"{key}={value}" for key, value in kwargs.items())
            url += f"?{query_string}"

        # Make the request
        response = self.session.get(url)
        response.raise_for_status()  
        return response.json()