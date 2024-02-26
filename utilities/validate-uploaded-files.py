import pandas as pd
import argparse
import os

"""
Author: rae McCollum
Date: 24 Jan 24
Purpose: Search through the md5 file to pull out files for a specified subject list that were uploaded to the NDA
Last Modified: 30 Jan 24 by Greg Conan
"""

def _cli():
    """
    :return: argparse.Namespace with all validated command-line arguments
             from the user via the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-in', '--md5', dest = "md5_values", required=True,
        help=('Valid path to existing readable md5_values.txt file in '
              'tab-separated format (like a .tsv)')
    )
    parser.add_argument(
        '-out', '--output', '--output-file', dest = "output",
        default=os.path.join(os.getcwd(), "uploaded_nda_files.txt"),
        help=('Valid path to file to save the list of uploaded files and their submission ID into. Default is cwd/uploaded_nda_files.txt.'
              "Format of output file is file_name, submission_id, subject, session.")
    )
    parser.add_argument(
        '-sub', '--subject_list', dest = "sub_file", required=True,
        help=("Path to a file with subject IDs to check which of their files were uploaded. "
        "Format needs to be subject,session WITH the 'sub-' and 'ses-' prefixes and no headers.")
    )

    return parser.parse_args()

def grab_sub_ses(line):
    """
    Grab subject and session from filename
    :param line: filename
    :return subject,session
    """
    split_line = line.strip().split("_")
    subject = split_line[0]
    session = split_line[1]
    return subject,session

def select_rows(name):
    """
    If filename has subject/session information, grab it. 
    Otherwise, assign subject/session to None
    :param name (filename)
    :return [subject,session]
    """
    if "sub" in name and "ses" in name:
        subject,session = grab_sub_ses(name)
    else:
        subject = None
        session = None
    return [subject,session]

def grab_files(input_file, subject_file, output_file):
    """
    Reads in files as dataframes, merges to select lines that exist in the subject file
    Outputs to file
    :param input_file (md5 file) 
    :param subject_file
    :param output_file
    """
    subjects_df = pd.read_csv(subject_file, names=["subject", "session"])
    sub_ses_cols = ["subject","session"]
    md5_df = pd.read_csv(input_file, sep="\t", header=0, skiprows=[1], usecols=["submission_id", "file_name"])
    # Grab subject session information and add as columns 
    md5_df["sub_ses"] = md5_df["file_name"].apply(select_rows)
    md5_df[sub_ses_cols] = pd.DataFrame(md5_df.sub_ses.tolist(), index= md5_df.index)
    # Drop empty rows and unneeded column
    md5_df.dropna(subset=sub_ses_cols, inplace=True)
    md5_df.drop(columns=["sub_ses"], inplace=True)
    # Only grab columns whos subject/session columns exist in the subjects_df
    md5_df.merge(subjects_df, how="inner", on=sub_ses_cols).to_csv(output_file, index=False)

def main():
    cli_args = _cli()
    input_file = cli_args.md5_values
    output_file = cli_args.output
    subject_file = cli_args.sub_file
    grab_files(input_file, subject_file, output_file)

if __name__ == "__main__":
    main()

