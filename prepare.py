#! /usr/bin/env python3
#
# DCAN Labs NDA BIDS preparation tool wrapper
#
# Created 04/24/2020 Natalie Alton (altonn@ohsu.edu)
# Modified 10/17/2021 Eric Earl (eric.earl@nih.gov)

import argparse
import csv 
import os
import stat
import subprocess
import sys
import pandas as pd
import shutil

HERE = os.path.dirname(os.path.realpath(__file__))


description = """
This python command-line tool is a wrapper for
the prepare scripts that are used to organize 
the provided data for NDA upload.
"""

def generate_parser():

    parser = argparse.ArgumentParser(
        prog='prepare.py',
        description=description
    )

    # "-t" and "--target" options are retained here for backward compatibility
    parser.add_argument(
        '-s', '--source', '-t', '--target', dest='source_dir', metavar='SOURCE', type=str, required=True,
        help=('The directory under which all data desired for upload is found. '
              ' This is usually the output of a pipeline like Dcm2Bids or '
              ' abcd-hcp-pipeline. It is the directory your file mapper JSONs '
              ' will be mapping from.')
    )

    parser.add_argument(
        '-d', '--destination', dest='dest', metavar='DESTINATION', type=str, required=True,
        help=('Path to the output directory where all data is staged for uploading. '
              ' This directory should also contain the directory of file mapper json '
              ' files and the lookup.csv. '
              'See the ndabids.readthedocs.io for further clarification')
    )

    parser.add_argument(
        '--subject-list', dest='subject_list', type=str, required=True,
        help=('Path to a csv containing a list of subjects and session pairs to upload '
              ' with column labels "bids_subject_id" and "bids_session_id", respectively')
    )

    parser.add_argument(
        '--datatypes', dest='datatypes', type=str, required=True,
        help=('Path to a txt file contain a list of the datatypes that should be '
              'uploaded for each subject.')
    )

    parser.add_argument(
        '-k', '--skip-filemapper', dest='skip', action='store_true', default=False,
        help=('Skip the file mapper step (only use if file-mapping is already done).')
    )

    return parser

def input_check():

    parser = generate_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.dest):
        print("The provided destination was not a directory " + args.dest + ", Exiting.")
        sys.exit(1)

    dest_dir = args.dest.rstrip('/')

    lookup_csv = os.path.join(dest_dir, "lookup.csv")
    if os.path.exists(lookup_csv):
        lookup_df = pd.read_csv(lookup_csv)
    else:
        print('ERROR: lookup.csv file should exist here: {}'.format(dest_dir))
    
    with open(args.subject_list) as f:
        reader = csv.reader(f)
        subject_list = list(reader)[1:]
        for subject_session in subject_list:
            row = lookup_df.loc[(lookup_df['bids_subject_id'] == subject_session[0]) & (lookup_df['bids_session_id'] == subject_session[1])]
            if len(row) == 1:
                continue
            else:
                print('WARNING: {} {} not found in {}'.format(subject_session[0], subject_session[1], lookup_csv))
                subject_list.remove(subject_session)

    wd = os.path.dirname(args.subject_list)
    
    with open(args.datatypes) as f:
        datatypes = [datatype.rstrip() for datatype in f.readlines()]

    manifest_dir = os.path.join(HERE, "manifest-data")
    file_mapper = os.path.join(HERE, "file-mapper")

    if not os.path.isdir(manifest_dir):
        print("Missing manifest directory " + manifest_dir + ", Exiting. Clone from https://github.com/NDAR/manifest-data")
        sys.exit(2)
    else:
        manifest_script = os.path.join(manifest_dir, "nda_manifests.py")

        # make executable
        manifest_status = os.stat(manifest_script)
        try:
            os.chmod(manifest_script, manifest_status.st_mode | stat.S_IEXEC)
        except:
            print('Warning: Unable to assign executable permissions to ' + manifest_script + ', continuing anyway.')
            pass

        if not os.path.isfile(manifest_script):
            print('Missing NDA manifest script ' + manifest_script + ', Exiting.')
            sys.exit(3)

    if not os.path.isdir(file_mapper):
        print("Missing file mapper directory " + file_mapper + ", Exiting. Clone from https://github.com/DCAN-Labs/file-mapper")
        sys.exit(4)
    else:
        mapper_script = os.path.join(file_mapper, "file_mapper_script.py")

        # make executable
        mapper_status = os.stat(mapper_script)
        try:
            os.chmod(mapper_script, mapper_status.st_mode | stat.S_IEXEC)
            print('Warning: Unable to assign executable permissions to ' + mapper_script + ', continuing anyway.')
        except:
            pass

        if not os.path.isfile(mapper_script):
            print('Missing file mapper script ' + mapper_script + ', Exiting.')
            sys.exit(5)

    if not os.path.isdir(args.source_dir):
        print("The provided source was not a directory " + args.source_dir + ", Exiting.")
        sys.exit(6)

    source_dir = args.source_dir.rstrip('/')

    return dest_dir, wd, subject_list, datatypes, mapper_script, manifest_script, source_dir, args.skip


def filemap_and_recordsprep(dest_dir, wd, subject_list, datatypes, mapper_script, source_dir, skip):

    if skip:
        print('Skipping file-mapping')
        lookup_csv = os.path.join(dest_dir, "lookup.csv")
    else:
        lookup_csv = os.path.join(dest_dir, "lookup.csv")
        child_check = False

        #with open(lookup_csv, 'r') as f:
        #    lookup = [row for row in csv.DictReader(f)]

        # go through all of the file_mapper json's using the current subject session pairing
        # assumes every JSON in the dest_dir is a file mapper JSON
        for datatype in datatypes:
            parent_name = datatype
            parent_dir = os.path.join(wd, datatype)
            parent_head, parent_tail = parent_name.split('_', 1) # e.g. fmriresults01 inputs.anat.T1w

            print('Starting ' + parent_name + ' file-mapping')

            for i in subject_list:
                bids_subject = i[0]
                subject = bids_subject.lstrip("sub-")
                bids_session = i[1]
                session = bids_session.lstrip("ses-")

                child_dir = os.path.join(parent_dir, bids_subject + '_' + bids_session + '.' + parent_tail)

                if os.path.isdir(parent_dir):
                    try:
                        os.mkdir(child_dir)
                    except FileExistsError:
                        print(child_dir + " exists")

                if not os.path.isdir(child_dir):
                    try:
                        os.makedirs(child_dir)
                    except FileExistsError:
                        print(child_dir + " exists")

                # calling the file mapper script.
                print('Preparing ' + bids_subject)

                # creating the string to be used in the template field of the file mapper.
                template = "'SUBJECT=" + str(subject) + ",SESSION=" + str(session) + "'"

                FM_cmd = (
                    'python3 ' + mapper_script +
                    ' -s ' +
                    ' -a symlink ' +
                    ' -sp ' + source_dir +
                    ' -dp ' + child_dir +
                    ' -t ' + template +
                    ' ' + os.path.join(dest_dir, 'filemapper_jsons', parent_name + '.json')
                    )
                #print(FM_cmd)
                subprocess.call(FM_cmd, shell=True)

                # if FM_cmd failed
                if not os.path.isdir(child_dir):
                    # go to the next iteration of this loop and skip below lines
                    continue

                child_check = False
                for child_content in os.listdir(child_dir):
                    content_path = os.path.join(child_dir, child_content)
                    if os.path.isdir(content_path):
                        child_check = True
                        break

                # Delete if content not found
                if child_check == False:  
                    for child_content in os.listdir(child_dir):
                        content_path = os.path.join(child_dir, child_content)
                        os.remove(content_path)
                    os.rmdir(child_dir)

    print('DATA PREPARED.  ATTEMPTING RECORDS PREPARATION.')

    for datatype in datatypes:
        parent_dir = os.path.join(wd, datatype)
        len_pd=os.listdir(parent_dir)
        
        if len(os.listdir(parent_dir)) == 0:
            print('{} EMPTY - DELETING.'.format(parent_dir))
            #os.rmdir(parent_dir)
            shutil.rmtree(parent_dir)
        
        else:
            RP_cmd = (
                'python3 ' + os.path.join(HERE, 'records.py') +
                ' -p ' + parent_dir +
                ' -l ' + lookup_csv +
                ' -y ' + os.path.join(dest_dir, 'prepared_yamls')
                )

            subprocess.call(RP_cmd, shell=True)

if __name__ == "__main__":
    print('Starting input check')
    dest_dir, wd, subject_list, datatypes, mapper_script, manifest_script, source_dir, skip = input_check()

    print('Starting file-mapping and records preparation')
    filemap_and_recordsprep(dest_dir, wd, subject_list, datatypes, mapper_script, source_dir, skip)

    print("Complete! Please review data prepared at: " + wd)

    sys.exit(0)
