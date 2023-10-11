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
        help=('Path to the directory from which files are being sourced.')
    )

    parser.add_argument(
        '-d', '--destination', dest='dest', metavar='DESTINATION', type=str, required=True,
        help=('Path to the directory holding all of the file mapper json files, the lookup.csv '
              'and the subdirectory that contains the NDA python manifest script.')
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
    manifest_dir = os.path.join(dest_dir, "manifest-data")
    file_mapper = os.path.join(dest_dir, "file-mapper")

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

    return dest_dir, mapper_script, manifest_script, source_dir, args.skip


def filemap_and_recordsprep(dest_dir, mapper_script, source_dir, skip):

    if skip:
        print('Skipping file-mapping')
    else:
        lookup_csv = os.path.join(dest_dir, "lookup.csv")
        child_check = False

        with open(lookup_csv, 'r') as f:
            lookup = [row for row in csv.DictReader(f)]

        # go through all of the file_mapper json's using the current subject session pairing
        # assumes every JSON in the dest_dir is a file mapper JSON
        for filename in os.listdir(dest_dir):
            if filename.endswith('.json'):

                # creating the parent and child directory for the files to get mapped to
                parent_name = filename.rstrip('.json')
                parent_dir = os.path.join(dest_dir, parent_name)
                parent_head, parent_tail = parent_name.split('_', 1)

                print('Starting ' + parent_name + ' file-mapping')

                for i in range(len(lookup)):
                    sub_ses = lookup[i]['bids_subject_session']

                    if ('_' in sub_ses) and ('_ses-' not in sub_ses):
                        print('Improperly formatted "bids_subject_session": ' + sub_ses + '. Requires "_ses-" between subject and session. Exiting.')
                        sys.exit(7)

                    char_count = sub_ses.count('_')
                    if char_count > 1:
                        print('Improperly formatted "bids_subject_session": ' + sub_ses + '. Requires no more than one "_" (underscore). Exiting.')
                        sys.exit(8)

                    if "_ses-" in sub_ses:
                        bids_subject, bids_session = sub_ses.split("_")
                        subject = bids_subject.lstrip("sub-")
                        session = bids_session.lstrip("ses-")
                        subject_and_session_flag = True
                    else:
                        bids_subject = sub_ses
                        subject = bids_subject.lstrip("sub-")
                        subject_and_session_flag = False

                    if subject_and_session_flag:
                        child_dir = os.path.join(parent_dir, bids_subject + '_' + bids_session + '.' + parent_tail)
                    else:
                        child_dir = os.path.join(parent_dir, bids_subject + '.' + parent_tail)

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
                    if subject_and_session_flag:
                        template = "'SUBJECT=" + str(subject) + ",SESSION=" + str(session) + "'"
                    else:
                        template = "'SUBJECT=" + str(subject) + "'"

                    FM_cmd = (
                        'python3 ' + mapper_script +
                        ' -s ' +
                        ' -a symlink ' +
                        ' -sp ' + source_dir +
                        ' -dp ' + child_dir +
                        ' -t ' + template +
                        ' ' + os.path.join(dest_dir, filename)
                        )

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

    for filename in os.listdir(dest_dir):
        if filename.endswith('.json'):

            # creating the parent and child directory for the files to get mapped to
            parent_name = filename.rstrip('.json')
            parent_dir = os.path.join(dest_dir, parent_name)

            RP_cmd = (
                'python3 ' + os.path.join(HERE, 'records.py') +
                ' -p ' + parent_dir
                )

            subprocess.call(RP_cmd, shell=True)


if __name__ == "__main__":
    print('Starting input check')
    dest_dir, mapper_script, manifest_script, source_dir, skip = input_check()

    print('Starting file-mapping and records preparation')
    filemap_and_recordsprep(dest_dir, mapper_script, source_dir, skip)

    print("Complete! Please review data prepared at: " + dest_dir)

    sys.exit(0)
