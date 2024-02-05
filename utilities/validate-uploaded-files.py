import pandas as pd
import argparse
import os

"""
Author: rae McCollum
Date: 24 Jan 24
Purpose: Search through the md5 file to pull out files for a specified subject list that were uploaded to the NDA
Last Modified: 1 Feb 24
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
        help='Path to a .txt file to save the list of uploaded files and their submission ID into. Default is cwd/uploaded_nda_files.txt'
    )
    parser.add_argument(
        '-sub', '--subject_list', dest = "sub_file", required=True,
        help=("Path to a file with subject IDs to check which of their files were uploaded. "
        "Format needs to be subject,session WITH the 'sub-' and 'ses-' prefixes and no headers.")
    )

    return parser.parse_args()

def grab_sub_ses(line):
    split_line = line.strip().split("_")
    subject = split_line[0]
    session = split_line[1]
    return subject,session

def grab_files(input_file, subjects, output_file):
    files = []
    md5_df = pd.read_csv(input_file, sep="\t", header=0, skiprows=[1], usecols=["submission_id", "file_name"])
    for _,row in md5_df.iterrows():
        name = row["file_name"]
        id = row ["submission_id"]
        if "sub" in name and "ses" in name:
            subject,session = grab_sub_ses(name)
        else:
            #print(f"This file is not a subject specific file:{name}")
            continue
        if subject in subjects and session in subjects[subject]:
            files.append(f"{id},{name}")
    with open(output_file, 'w') as output:
        output.write("\n".join(files))

def make_sub_ses_dict(subject_file):
    sub_ses_dict = dict()
    with open(subject_file, 'r') as sub_file:
        for line in sub_file:
            strip_line = line.strip().split(',')
            subject = strip_line[0]
            session = strip_line[1]
            sub_ses_dict[subject] = session
    return sub_ses_dict

def main():
    cli_args = _cli()
    input_file = cli_args.md5_values
    output_file = cli_args.output
    subject_file = cli_args.sub_file
    subject_sessions = make_sub_ses_dict(subject_file)
    grab_files(input_file, subject_sessions, output_file)

if __name__ == "__main__":
    main()

