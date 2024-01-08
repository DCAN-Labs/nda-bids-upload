import pandas as pd 
import argparse
import datetime

"""
Author: rae McCollum
Created: 8 Nov 23
Last Modified: 8 Jan 24 (add documentation)
Purpose: Make sure that all of the subjects of a subject list made it into the lookup.csv and remove duplicate lines that have different interview dates (chooses the earliest date). Outputs a text file with any subjects that don't exist in the original lookup.csv and rewrites the lookup.csv to remove the duplicate lines. Note that this script does not handle when there are duplicate lines with different ages/sex markers.
"""


def _cli():
    """
    :return: Dictionary with all validated command-line arguments from the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--lookup_csv', required=True,
        help='Path to the lookup.csv'
    )
    parser.add_argument(
        '--subject_list', required=True,
        help='Path to subject_list.csv containing the subjects you wish to upload'
    )
    parser.add_argument(
        '--output_file', required=False, default="validation_lookupcsv.txt",
        help='Path to where you want the text file with the missing subjects to be output (including the name of the file)'
    )
    
    return vars(parser.parse_args())

def verify_subjects(lookup_df, subject_csv, out_txt_file):
	"""Takes in the lookup.csv dataframe, the subject list csv, and the output text file.
	   If a subject,session pair doesn't exist in the dataframe, write it to the output file
	   Return the length of the missing subjects list"""
    
    subjects_df = pd.read_csv(subject_csv)
    missing_subjects = []
    for index, row in subjects_df.iterrows():
        sub = row["bids_subject_id"]
        ses = row["bids_session_id"]

        match_row = lookup_df[(lookup_df['bids_subject_id'] == sub) & (lookup_df['bids_session_id'] == ses)]

        if match_row.empty:
            missing_subjects.append(sub + ',' + ses)

    with open(out_txt_file, "w") as output_file:
        for missing_subject in missing_subjects:
            output_file.write(missing_subject + "\n")

    return(len(missing_subjects))

def find_double_subjects(lookup_df, subject_csv):
	"""Takes in the lookup.csv dataframe and the subject list csv file
	   If there is a subject in multiple rows of the df, choose the earilest date and remove any other duplicate lines
	   Return the modified dataframe"""
    subjects_df = pd.read_csv(subject_csv)
    subjects = subjects_df["bids_subject_id"].tolist()
    for sub in subjects:
        sub_df = lookup_df[lookup_df["bids_subject_id"]==sub]
        if sub_df.empty:
            continue
        double_session = find_double_sessions(sub_df)
        if len(double_session) >= 1:
            for ses in double_session:
                double_sub = sub_df[sub_df["bids_session_id"]==double_session[0]]
                date = find_first_date(double_sub)
                lookup_df = remove_double_session(date, sub, double_session, lookup_df)
    return lookup_df 

def find_double_sessions(sub_df):
	"""Takes in a dataframe of a single subject
	   Returns list of sessions that are duplicate"""
    sessions = sub_df["bids_session_id"]
    unique_values = set()
    duplicates = set()
    
    for value in sessions:
        if value in unique_values:
            duplicates.add(value)
        else:
            unique_values.add(value)
    
    return list(duplicates)

def find_first_date(double_sub):
	"""Takes in a dataframe of a single subject with duplicate sessions
	   Returns the earliest data listed """
    dates = double_sub["interview_date"]
    date_objects = [datetime.datetime.strptime(date, '%m/%d/%Y') for date in dates]
    
    # Find the earliest date
    earliest_date = min(date_objects)
    
    # Convert the earliest date back to string format
    earliest_date = earliest_date.strftime('%m/%d/%Y')
    
    return earliest_date

def remove_double_session(earliest_date, subject, session, lookup_df):
	"""Takes in the earilest date, subject, session, and lookup dataframe
	   Returns a modified lookup df that removes the duplicated line that doesn't have the earliest date"""
    session = session[0]
    lookup_df = lookup_df[~((lookup_df["bids_subject_id"] == subject) & (lookup_df["bids_session_id"] == session) & (lookup_df["interview_date"] != earliest_date))]
    return lookup_df


if __name__ == "__main__":
    cli_args = _cli()
    lookup_csv = cli_args['lookup_csv']
    subject_csv = cli_args["subject_list"]
    out_txt_file = cli_args["output_file"]
    lookup_df = pd.read_csv(lookup_csv)

    new_lookup = find_double_subjects(lookup_df, subject_csv)
    new_lookup.to_csv(lookup_csv,index=False)
    fmri_subjects = verify_subjects(lookup_df, subject_csv, out_txt_file)
    
    print("There are", fmri_subjects, " missing subjects. IDs were written to", out_txt_file)
    
