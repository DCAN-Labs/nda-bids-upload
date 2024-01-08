import os
import csv
import glob
import argparse

"""
Author: rae McCollum
Date: Sept 2023
Last Modified: 8 Jan 24 (finds if subject is missing everywhere, not only for each individual datatype dir)
Purpose: Validates that prepare.py created at least one datatype folder for all the expected subjects. Outputs missing subjects to a text file.
"""

def _cli():
    """
    :return: Dictionary with all validated command-line arguments from the user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--upload_dir', required=True,
        help='Path to upload working directory containing the datatype folders created after running prepare.py'
    )
    parser.add_argument(
        '--subject_list', required=True, 
        help='Path to subject_list.csv containing the subjects you wish to upload'
    )
    parser.add_argument(
        '--output_file', required=False, default = "prepare_validation.txt" 
        help='Path to where you want the text file with the missing subjects to be output (including the name of the file). Default is cwd/prepare_validation.txt.'
    )
    
    return vars(parser.parse_args())


def find_fmri_subjects(main_directory, csv_path, txt_file):
	"""Takes in the upload directory path, the csv file, and the output file
	   Returns the length of the missing subjects list"""
	fmri_subjects = set()
	missing_subjects = []
	# Grab all datatype directories and loop through them
	fmri_directories = glob.glob(os.path.join(main_directory, "fmriresults*"))
	for dirs in fmri_directories:
		search_dir = glob.glob(os.path.join(dirs, "sub-*"))
		# Grab all the subject ID's from each datatype directory
		for sub_folder in search_dir:
			sub_id = sub_folder.split("/")[-1].split("_")[0]
			fmri_subjects.add(sub_id)
		
	# Read in the subject list csv 
	with open(csv_path, "r") as csv_file:
		csv_reader = csv.DictReader(csv_file)
		# For every subject in the csv, if that doesn't exist anywhere in the upload dir, add it to list
		for row in csv_reader:
			subject = row["bids_subject_id"]
			if subject not in fmri_subjects:
				missing_subjects.append(subject)
	unique_subjects = set(missing_subjects)
	
	# Write missing subjects to file
	with open(txt_file, "w") as output_file:
		for missing_subject in unique_subjects:
			output_file.write(missing_subject + "\n")

	return len(unique_subjects)

if __name__ == "__main__":
    cli_args = _cli()
    upload_dir = cli_args['upload_dir']
    subject_csv = cli_args["subject_list"]
    out_txt_file = cli_args["output_file"]

    fmri_subjects = find_fmri_subjects(upload_dir, subject_csv, out_txt_file)
    
    print("There are", fmri_subjects, " missing subjects. IDs were written to", out_txt_file)
