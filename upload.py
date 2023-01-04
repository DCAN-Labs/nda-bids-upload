#! /usr/bin/env python3

"""
DCAN Labs NDA BIDS NDA vtcmd upload tool

Created  03/09/2020  Natalie Alton (altonn@ohsu.edu)
Modified 03/18/2020  Eric Earl (earl@ohsu.edu)
"""

import argparse
import math
import os
import subprocess
import sys

from glob import glob

__doc__ = """
This python command-line tool allows the user a more
automated upload process to the NDA production environment
using the nda-tools vtcmd.
"""


def generate_parser():

    parser = argparse.ArgumentParser(
        prog='upload.py',
        description=__doc__
    )    
    parser.add_argument(
        '-c', '--collection', dest='collection_id', metavar='COLLECTION_ID', type=int, required=True,
        help=('The collection flag needs an NDA Collection ID. You can find '
              ' collection IDs in the nda.nih.gov. For instance, the ABCC is 3165, '
              ' ASD-BIDS is 1955, ADHD-BIDS years 1-8 is 2857, and ADHD-BIDS years '
              ' 9-12 is 3222.')
    )
    parser.add_argument(
        '-s', '--source', '-p', '--parent', dest='source', metavar='SOURCE_DIR', type=str, required=True,
        help=('Path to the folder that were prepared for upload (the same path as '
              'the --source specified for prepare.py). '
              ' Folder should be of the format: ".../ndastructure_type.class.subset" '
              ' containing folders called "sub-subject_ses-session.type.class.subset" '
              ' where "ndastructure" is fmriresults01 or imagingcollection01, '
              ' "subject" is the BIDS subject ID/participant label, '
              ' "session" is the BIDS session ID, "type" is either "inputs" or '
              ' "derivatives", "class" is "anat", "dwi", "fmap", "func", or something '
              ' similar, and "subset" is the user-defined "data subset type".'
              'For example: '
              ' .../imagingcollection01_inputs.anat.T1w/sub-NDARABC123_ses-baseline.inputs.anat.T1w')
    )
    parser.add_argument(
        '-vt', '--ndavtcmd', dest='vtcmd', metavar='VTCMD', type=str, required=True,
        help=('Absolute path to the vtcmd located in the virtual environment being used for the upload. '
              ' If it is in your local Python installation binaries folder: '
              '--ndavtcmd=~/.local/bin/vtcmd '
              'For installation instructions see https://github.com/NDAR/nda-tools')
    )
    return parser

def input_checks():

    
    # command line interface parse
    parser = generate_parser()
    args = parser.parse_args()

    # check if args.source is a directory
    if not os.path.isdir(args.source):
        print(args.source + ' is not a directory!  Exiting...')
        sys.exit(1)
    else:
        source = os.path.abspath(os.path.realpath(args.source))

    basename = os.path.basename(source)
    nda_struct, file_config = basename.split('_', 1)
    if not ( nda_struct == 'fmriresults01' or nda_struct == 'image03' or nda_struct == 'imagingcollection01' ):
        print(basename + ' is not a valid entry for section A.  Improper parent folder name.  Exiting...')
        sys.exit(2)

    if file_config.count('.') != 2:
        print(file_config + ' is an improper parent folder naming convention.  The parent folder MUST only contain two periods total.  Exiting...')
        sys.exit(3)
    else:
        input_deriv, subsets, types = file_config.split('.')

    if not ( input_deriv == 'inputs' or input_deriv == 'derivatives' or input_deriv == 'sourcedata' ):
        print(input_deriv + ' is not a valid entry for section X.  Section X MUST be either "inputs", "derivatives", or "sourcedata".  Improper parent folder name.  Exiting...')
        sys.exit(4)

    if subsets.count('_') != 0:
        print(subsets + ' is not a valid entry for section Y.  Section Y MUST have no underscores.  Improper parent folder name.  Exiting...')
        sys.exit(5)

    problem_child_flag = False

    for root, dirs, files in os.walk(source):
        if root == source:
            for directory in dirs:
                if not directory.startswith('sub-NDAR'):
                    problem_child_flag = True
                    print('Improper child folder name: ' + directory + '.  Child directories MUST start with "sub-NDAR".  Exiting after full check...')
                else:
                    sub_ses, sub_directory_config = directory.split('.', 1)
                    if sub_directory_config != file_config:
                        problem_child_flag = True
                        print('Improper child folder name.  Sections X.Y.Z MUST match between parent and child folders.  Exiting after full check...')

    if problem_child_flag:
        sys.exit(6)

    if not os.path.isfile(args.vtcmd):
        print(args.vtcmd + ' is not a file!  Exiting...')
        sys.exit(7)


def nda_vt():

    # command line interface parse
    parser = generate_parser()
    args = parser.parse_args()

    source = os.path.abspath(args.source)
    basename = os.path.basename(source)

    ndastructure, data_subset = basename.split('_', 1)
    complete_csv = source + '.complete_records.csv'
    glob_string = os.path.join(source, '*.' + data_subset)

    with open(complete_csv) as f:
        all_records = f.readlines()

    max_batch_size = 500 # @TODO this needs to become an integer input defaulted to 500
    total = len(all_records) - 2 # minus two because of two header lines in the complete records file
    count = int(math.ceil(float(total) / max_batch_size ))
    upload_record = source + '.uploaded_' + data_subset + '.upload'

    with open(upload_record, 'r+') as upload_file:
        file_list = [line.rstrip() for line in upload_file.readlines()]
        print(file_list)

        for i in range(1, count+1):
            batchname = '_'.join([ str(total), str(max_batch_size), str(i) ])

            description = basename + '.batch_' + batchname
            records_batch = source + '.records_' + batchname + '.csv'
            folders_batch = source + '.folders_' + batchname + '.txt'

            if records_batch in file_list:
                print("WARNING: " + records_batch + " appears in " + upload_record + " so may already have been uploaded to the NDA.")
                continue

            subprocess.call(('echo `date` Uploading: ' + description), shell=True)
            cmd = (args.vtcmd + ' ' + records_batch +
                  ' -c ' + str(args.collection_id) +
                  ' -m ' + source +
                  ' -t ' + description +
                  ' -d ' + description +
                  ' -l `cat ' + folders_batch + '` ' +
                  ' -b')

            subprocess.call(('echo ' + cmd), shell=True)
            subprocess.call(cmd, shell = True) # TODO Check for success, need to check stdout
            upload_file.write(records_batch + '\n')

    
    upload_file.close()

if __name__ == "__main__":
    input_checks()
    nda_vt()
    sys.exit(0)
