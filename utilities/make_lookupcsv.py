import csv 
import pandas as pd
import argparse

"""
Author: Luci Moore
Created:
Last Modified: 8 Jan 24 by rae McCollum (add documentation)
Purpose: Creates a lookup.csv needed for NDA uploads
"""


def _cli():
    """
    :return: Dictionary with all validated command-line arguments from the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--info_file', required=True,
        help='Path to the reference file that contains the information needed for the lookup csv '
    )
    parser.add_argument(
        '--lookup_csv', required=True,
        help='Path to where you want the lookup.csv to go '
    )
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--fasttrack', action="store_true",
        help='Specify if using abcdfasttrack QC file.'
    )

    group.add_argument(
        '--abcdmri', action="store_true",
        help='Specify if using abcdmri01 text file.'
    )
    
    return vars(parser.parse_args())

def remove_duplicates_ignore_case(df):
	"""Takes in the lookupcsv dataframe
	   Returns a modified dataframe that doesn't have any duplicate subject IDs"""
    # Convert relevant columns to lowercase
    df = df.apply(lambda x: x.astype(str).str.upper() if x.name in ["src_subject_id", "bids_subject_id"] else x)

    # Remove duplicates while ignoring case
    df = df.drop_duplicates()

    return df

def replace_sub(df):
	"""Takes in the lookupcsv dataframe
	   Returns a modified dataframe that has the correct lowercase "sub" prefix"""
    df["bids_subject_id"] = df["bids_subject_id"].str.replace('SUB', 'sub')
    return df


def make_lookupcsv(ref_txt_file, lookup_csv, file_type):
	"""Takes in the information file, the lookup.csv, and the file type (ft or mri)
	   No return, creates csv"""
    # Create DataFrame from LUT file
    LUT_df=pd.read_csv(ref_txt_file, sep="\t")

    # Remove 2nd row with extraneous metadata
    LUT_df=LUT_df.drop([0, 0])

    #strip "_" from src_subject_id in LUT for bids_subject_id in output lookup.csv and prepend with 'sub-'
    LUT_df['src_subject_id_strip'] = LUT_df['src_subject_id'].str.replace('_', '')
    LUT_df['src_subject_id_strip'] = 'sub-' + LUT_df['src_subject_id_strip'].astype(str)

    #modify eventname from LUT for bids_session_id in lookup.csv
    if file_type == "ft":
        LUT_df['bids_session_id'] = LUT_df['visit'].str.replace('baseline_year_1_arm_1', 'ses-baselineYear1Arm1')
    elif file_type == "mri":
        LUT_df['bids_session_id'] = LUT_df['eventname'].str.replace('baseline_year_1_arm_1', 'ses-baselineYear1Arm1')
    LUT_df['bids_session_id'] = LUT_df['bids_session_id'].str.replace('2_year_follow_up_y_arm_1', 'ses-2YearFollowUpYArm1')

    #LUT_df['bids_session_id'] = LUT_df['eventname'].str.replace('_', '')
    #LUT_df['bids_session_id'] = 'ses-' + LUT_df['bids_session_id'].astype(str)

    # Create output lookup csv dataframe
    lookup_df = pd.DataFrame({'bids_subject_id': LUT_df['src_subject_id_strip'],
                          'bids_session_id': LUT_df['bids_session_id'],
                          'subjectkey': LUT_df['subjectkey'],
                          'src_subject_id': LUT_df['src_subject_id'],
                          'interview_date': LUT_df['interview_date'],
                          'interview_age': LUT_df['interview_age'],
                          'sex': LUT_df['sex']})
    
    lookup_df = remove_duplicates_ignore_case(lookup_df)
    lookup_df = replace_sub(lookup_df)
    
    lookup_df.bids_subject_id = lookup_df.bids_subject_id.astype(str)
    lookup_df.to_csv(lookup_csv, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    
if __name__ == "__main__":
    cli_args = _cli()
    ref_file = cli_args["info_file"]
    lookup_csv = cli_args["lookup_csv"]

    if cli_args["fasttrack"]:
        file_type = "ft"
    elif cli_args["abcdmri"]:
        file_type = "mri"
        
    make_lookupcsv(ref_file, lookup_csv, file_type)
