import json
import argparse
import os
from datetime import datetime
from educationdata import EducationDataAPI

def main():
    parser = argparse.ArgumentParser(description="Fetch CRDC discipline data and optionally write to a file.")
    parser.add_argument('--output', action='store_true', help='If provided, the JSON response will be written to a file.')
    args = parser.parse_args()

    api = EducationDataAPI()
    # data = api.get_ccd_directory(2013, charter=1, fips=11)
    # data = api.get_ccd_enrollment(2014, 8, race=3, sex=1)
    # data = api.get_crdc_directory(2013, fips=13, charter_crdc=1)
    # data = api.get_crdc_enrollment(2013, race_segment=True, sex_segment=True, race=3, sex=1)
    # data = api.get_crdc_discipline(2017, fips=1, disability=1)
    # data = api.get_crdc_discipline_segment(2013, disability_segment=True, sex_segment=True, fips=1)
    # data = api.get_crdc_bullying_allegations(2015, fips=1, allegations_harass_sex=10)
    # data = api.get_crdc_bullying_segment(2013, race_segment=True, sex_segment=True, race=1, sex=1)
    # data = api.get_crdc_absenteeism_segment(2013, race_segment=True, sex_segment=True, race=1, sex=1)
    # data = api.get_crdc_restraint_instances(2015, fips=1, disability=1)
    # data = api.get_crdc_restraint_segment(2013, disability_segment=True, sex_segment=True, fips=1, disability=1)
    data = api.get_crdc_advanced_enrollment_segment(2013, race_segment=True, sex_segment=True, race=1, sex=1)


    if args.output:
        # Ensure the 'json' directory exists
        output_dir = 'json'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate the filename with a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'response_{timestamp}.json'
        filepath = os.path.join(output_dir, filename)
        
        # Write the data to the file
        with open(filepath, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        print(f"Data written to {filepath}")

    else:
        formatted_data = json.dumps(data, indent=4)
        print(formatted_data)

if __name__ == "__main__":
    main()



