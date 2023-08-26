import csv 
import pandas as pd
import argparse

#This script was written to generate a lookup.csv file from this spreadsheet: 
#/home/rando149/shared/data/Collection_3165_Supporting_Documentation/abcd_mri01_20230407/abcd_mri01.txt

parser = argparse.ArgumentParser()
parser.add_argument("ref_txt_file")
args = parser.parse_args()

def make_lookupcsv(ref_txt_file):
    # Create DataFrame from LUT file
    LUT_df=pd.read_csv(ref_txt_file, sep="\t")

    # Remove 2nd row with extraneous metadata
    LUT_df=LUT_df.drop([0, 0])

    #strip "_" from src_subject_id in LUT for bids_subject_id in output lookup.csv and prepend with 'sub-'
    LUT_df['src_subject_id_strip'] = LUT_df['src_subject_id'].str.replace('_', '')
    LUT_df['src_subject_id_strip'] = 'sub-' + LUT_df['src_subject_id_strip'].astype(str)

    #modify eventname from LUT for bids_session_id in lookup.csv
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
    
    lookup_df.bids_subject_id = lookup_df.bids_subject_id.astype(str)
    lookup_df.to_csv('lookup.csv', index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    
if __name__ == "__main__":
    make_lookupcsv(args.ref_txt_file)