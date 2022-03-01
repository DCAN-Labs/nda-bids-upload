#! /usr/bin/env python3

"""
DCAN Labs DICOM to TAR.GZ conversion utility

Created  12/19/2021 by Eric Earl
"""

import argparse   # For command line arguments
import csv        # For CSV file handling
import os         # For file system operations
import pydicom    # For DICOM file handling
import subprocess # For calling external programs

from datetime import datetime # For timestamping
from glob import glob # For globbing file names


HERE = os.path.dirname(os.path.realpath(__file__))

__doc__ = """
This command-line tool allows the user to easily convert a directory of only 
DICOM files into a TAR.GZ archive in a rough approximation of a BIDS hierarchy.
"""

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-i', '--input-csv', metavar='CSV' , required=True,
                    help='dicoms.csv file with paths to unique series folder per '
                    'subject session in the first column followed by: '
                     'nda_bids_subject, bids_session, bids_name, bids_modality')

parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', required=True,
                    help='Output directory to deposit TAR.GZ files in a '
                         'BIDS-like hierarchy')

args = parser.parse_args()

input_csv = os.path.abspath(args.input_csv)
output_dir = os.path.abspath(args.output_dir)

subjects = []
sessions = []
combos = []

with open(input_csv, 'r') as f:
    reader = csv.DictReader(f)
    for series in reader:
        # read columns from CSV file
        source = series['source'] # e.g. /path/to/dicom/series/4-REST2/
        nda_bids_subject = series['nda_bids_subject'] # e.g. sub-01
        bids_session = series['bids_session'] # e.g. ses-01
        bids_name = series['bids_name'] # e.g. task-rest
        bids_modality = series['bids_modality'] # e.g. func

        # append to lists
        subjects.append(nda_bids_subject)
        sessions.append(bids_session)
        combos.append((bids_modality, bids_name))

        # grab any one DICOM file from source directory (index 0)
        dicom_file = glob(os.path.join(source, '*'))[0]

        # grab the series number for the DICOM file
        series_number = str(pydicom.dcmread(dicom_file).SeriesNumber)

        # create output TAR.GZ file
        output_basename = '_'.join([nda_bids_subject, bids_session, bids_name, 
                                    'series-' + series_number + '.tar.gz'])
        output = os.path.join(output_dir, 'sourcedata', nda_bids_subject, 
                              bids_session, bids_modality, output_basename)

        # create output directories
        os.makedirs(os.path.dirname(output), exist_ok=True)

        print(datetime.now(), 'Creating TAR.GZ file: ' + output)
        subprocess.run(['tar', '-czf', output, '-C', source, '.'])

# report back to user
print('DICOM to TAR.GZ conversion complete!' + '\n')
print('Output directory: ' + output_dir)

print('Subjects:')
print('\t' + ', '.join(list(set(subjects))) + '\n')

print('Sessions:')
print('\t' + ', '.join(list(set(sessions))) + '\n')

print('Combinations:')
for combo in list(set(combos)):
    print('\t' + ', '.join(combo))
