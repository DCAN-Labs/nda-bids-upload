#! /usr/bin/env python3

"""
DCAN Labs NDA BIDS preparation tool

Created  02/20/2020  Eric Earl (earl@ohsu.edu)
"""

import argparse
import csv
import math
import os
import subprocess
import sys
import yaml

from glob import glob


HERE = os.path.dirname(os.path.realpath(__file__))

__doc__ = """
This python command-line tool allows the user to do 
more automated NDA BIDS data upload preparation 
given an input folder structure hierarchy that obeys 
the DCAN Labs NDA BIDS preparation standard.
"""


def generate_parser():

    parser = argparse.ArgumentParser(
        prog='records.py',
        description=__doc__
    )

    parser.add_argument(
        '-p', '--parent', dest='parent', metavar='PARENT_DIR', type=str, required=True,
        help=('Path to the "parent" folder to be prepared for upload. "Parent" '
              'folder should be of the format: ".../ndastructure_type.class.subset" '
              'containing subfolders called "sub-subject_ses-session.type.class.subset" '
              'where "ndastructure" is fmriresults01, image03, or imagingcollection01, '
              '"subject" is the BIDS subject ID/participant label, '
              '"session" is the BIDS session ID, "type" is either "inputs" or '
              '"derivatives", "class" is "anat", "dwi", "fmap", "func", or something '
              'similar, and "subset" is the user-defined "data subset type".'
              'For example: "image03_inputs.anat.T1w" containing subfolders like '
              '"sub-NDARABC123_ses-baseline.inputs.anat.T1w"')
    )

    return parser


# Sanity check against user inputs
def records_sanity_check(input):

    # check if input is a directory
    if not os.path.isdir(input):
        print(input + ' is not a directory!  Exiting...')
        sys.exit(1)
    else:
        parent = os.path.abspath(os.path.realpath(input))

    dest_dir = os.path.dirname(parent)
    lookup_csv = os.path.join(dest_dir, 'lookup.csv')
    manifest_script = os.path.join(dest_dir, 'manifest-data', 'nda_manifests.py')

    # check if manifest_script exists
    if not os.path.isfile(manifest_script):
        print(manifest_script + ' is not a file, contained a directory above "parent" in a directory called manifest-data.  Exiting...')
        sys.exit(2)

    # check if lookup_csv exists
    if not os.path.isfile(lookup_csv):
        print(lookup_csv + ' is not a file, contained a directory above "parent" called "lookup.csv".  Exiting...')
        sys.exit(3)

    # grab parent's basename
    basename = os.path.basename(parent)
    nda_struct, file_config = basename.split('_', 1)
    if not ( nda_struct == 'fmriresults01' or nda_struct == 'image03' or nda_struct == 'imagingcollection01' ):
        print(basename + ' is not a valid entry for section A.  Improper parent folder name.  Exiting...')
        sys.exit(4)

    if file_config.count('.') != 2:
        print(file_config + ' is an improper parent folder naming convention.  The parent folder MUST only contain two periods total.  Exiting...')
        sys.exit(5)
    else:
        input_deriv, subsets, types = file_config.split('.')

    if not ( input_deriv == 'inputs' or input_deriv == 'derivatives' or input_deriv == 'sourcedata' ):
        print(input_deriv + ' is not a valid entry for section X.  Section X MUST be either "inputs", "derivatives", or "sourcedata".  Improper parent folder name.  Exiting...')
        sys.exit(6)

    if subsets.count('_') != 0:
        print(subsets + ' is not a valid entry for section Y.  Section Y MUST have no underscores.  Improper parent folder name.  Exiting...')
        sys.exit(7)

    problem_child_flag = False

    for root, dirs, files in os.walk(parent):
        if root == parent:
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
        sys.exit(8)

    # compare basename to available "content" YAML files
    content_yamls = [content for content in glob( os.path.join(dest_dir, '*.yaml') ) 
                     if os.path.basename(content) == basename + '.yaml' ]

    if not len(content_yamls) == 1:

        if len(content_yamls) > 1:
            print('More than one content file matches your parent directory\'s basename (' + basename + '):')
            for content in content_yamls:
                print('  ' + content)
            print('This should never happen.  Please debug records.py.')

        elif len(content_yamls) == 0:
            print('No content .yaml files in ' + dest_dir + ' match the basename: ' + basename)
            print('Make sure a matching content .yaml file exists in the folder above the parent folder you provided.')

        print('Exiting...')
        sys.exit(9)
    else:
        content_yaml = content_yamls[0]

    # sanity-check entries in correct content YAML file
    print('Sanity-checking: ' + content_yaml)
    with open(content_yaml, 'r') as f:
        content = yaml.load(f, Loader=yaml.CLoader)

    badflag = False
    for key in content:
        value = content[key]
        if len(value) == 0:
            badflag = True
            print('Empty field in ' + content_yaml + ':')
            print('    ' + key + ': "' + value + '"')

    if badflag:
        print('No empty fields allowed in content .yaml files.  Exiting...')
        sys.exit(10)
    

def cli(input):

    # setting easy use variables from argparse
    parent = os.path.abspath(os.path.realpath(input))
    dest_dir = os.path.dirname(parent)
    manifest_script = os.path.join(dest_dir, 'manifest-data', 'nda_manifests.py')
    lookup_csv = os.path.join(dest_dir, 'lookup.csv')

    # grab parent's basename
    basename = os.path.basename(parent)

    # start an empty data template
    if basename.startswith('fmriresults01'):
        ndaheader = '"fmriresults","01"'
        with open(os.path.join(HERE, 'templates', 'fmriresults01_template.csv'), 'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader):
                if i==1:
                    header = row
    elif basename.startswith('imagingcollection01'):
        ndaheader = '"imagingcollection","01"'
        with open(os.path.join(HERE, 'templates', 'imagingcollection01_template.csv'), 'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader):
                if i==1:
                    header = row
    elif basename.startswith('image03'):
        ndaheader = '"image","03"'
        with open(os.path.join(HERE, 'templates', 'image03_template.csv'), 'r') as f:
            reader = csv.reader(f)
            for i,row in enumerate(reader):
                if i==1:
                    header = row

    # grabbing yaml
    content_yamls = [content for content in glob( os.path.join(dest_dir, '*.yaml') ) 
                     if os.path.basename(content) == basename + '.yaml' ]

    content_yaml = content_yamls[0]

    # sanity-check entries in correct content YAML file
    with open(content_yaml, 'r') as f:
        content = yaml.load(f, Loader=yaml.CLoader)

    # load lookup CSV file
    with open(lookup_csv,'r') as f:
        lookup = [row for row in csv.DictReader(f)]

    ### DO WORK ###
    # 1. GLOB all .../ndastructure_type.class.subset/sub-subject_ses-session.type.class.subset/ folders
    uploads = glob(os.path.join(parent, '*.*.*.*'))

    # 2. loop over the folders
    subprocess.call(('echo `date` Creating NDA records'), shell=True)
    records = []
    folders = []
    for upload_dir in uploads:
        # skip to the next iteration of the for loop if the upload_dir is not a directory
        if not os.path.isdir(upload_dir):
            continue

        # create an NDA record for each folder using the content YAML file
        upload_basename = os.path.basename(upload_dir)
        bids_subject_session, datatype, dataclass, datasubset = upload_basename.split('.')

        record_found = False
        for row in lookup:
            if row['bids_subject_session'] == bids_subject_session:
                lookup_record = row
                record_found = True
                # if '_ses-' in bids_subject_session:
                #     # regular expression magic
                break

        if not record_found:
            continue

        # nda-manifest each folder
        manifest_file = '.'.join([upload_dir, 'manifest', 'json'])

        subprocess.call(' '.join(['python3', manifest_script, '-id', '.', '-of', manifest_file]),
                        shell=True, cwd=upload_dir, stdout=subprocess.DEVNULL)

        # correct the manifest contents to remove the leading "./" from each manifest element
        subprocess.call('sed -i "s|\./||g" ' + manifest_file, shell=True)

        # write the new record for entry into the larger output CSV
        new_record = {}
        for column in header:
            if column in content:
                new_record[column] = content[column]
            else:
                new_record[column] = '' 

        if basename.startswith('fmriresults01') or basename.startswith('image03'):
            new_record['manifest'] = os.path.basename(manifest_file)
            new_record['image_description'] = '.'.join([datatype, dataclass, datasubset])
        elif basename.startswith('imagingcollection01'):
            new_record['image_manifest'] = os.path.basename(manifest_file)
            new_record['image_collection_desc'] = '.'.join([datatype, dataclass, datasubset])

        for column in lookup_record:
            if column != 'bids_subject_session':
                new_record[column] = lookup_record[column]

        records.append(new_record)
        folders.append(upload_dir)

    with open(parent + '.complete_records.csv', 'w') as f:
        f.write(ndaheader + '\n')

        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

    with open(parent + '.complete_folders.txt', 'w') as f:
        for folder in folders:
            f.write(folder + '\n')

    max_batch_size = 500 # @TODO this needs to become an integer input defaulted to 500
    total = len(records)
    count = math.ceil(float(total) / max_batch_size )
    batch_size = math.ceil(float(total) / count )

    low = 0
    subprocess.call(('echo `date` Creating batch files'), shell=True)
    for i in range(1, count+1):
        if i < count or total == batch_size:
            B = batch_size
        else:
            B = total % batch_size

        records_subset = records[ low : (low + B) ]
        folders_subset = folders[ low : (low + B) ]
        low = i * batch_size

        batchname = '_'.join([ str(total), str(max_batch_size), str(i) ])
        records_batch = parent + '.records_' + batchname + '.csv'
        folders_batch = parent + '.folders_' + batchname + '.txt'

        with open(records_batch, 'w') as f:
            f.write(ndaheader + '\n')

            writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for record in records_subset:
                writer.writerow(record)

        with open(folders_batch, 'w') as f:
            for folder in folders_subset:
                f.write(folder + '\n')

    print("FINISHED " + basename + " RECORDS PREPARATION.")

if __name__ == "__main__":
    # command line interface parse
    parser = generate_parser()
    args = parser.parse_args()

    records_sanity_check(args.parent)
    cli(args.parent)
    sys.exit(0)
