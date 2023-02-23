#!/usr/bin/env python3

import os
#import json
import requests
#import glob
import re
from NDA_submission_API import get_auth, get_submission_ids, get_associated_files

# To resume a stalled upload we must create a space delimited list of all directories containing the associated files for the submission

ndar_username, ndar_password = get_auth()


# File containing full local file path for every associated file
with open('all_files.txt', 'r') as f:
    all_files = f.read().splitlines()
#with open('all_task_files.txt', 'r') as f:
#    all_task_files = f.read().splitlines()

submission_ids = get_submission_ids(3165, 'Uploading', ndar_username=ndar_username, ndar_password=ndar_password)
print('Found {} stalled submissions'.format(len(submission_ids)))

for submission_id in submission_ids:
    if os.path.exists('./resume_cmds/resume_{}.txt'.format(submission_id)):
        print('Skipping {}. Resume command already exists'.format(submission_id))
        continue
    else:
        print('Checking {}'.format(submission_id))
    associated_files = get_associated_files(submission_id, ndar_username=ndar_username, ndar_password=ndar_password)

    # Check if task contrast
    if 'contrast' in associated_files[0]:
        contrast = '_'.join(associated_files[0].split('_')[2:6])
        print('\t contrast: {}'.format(contrast))
        with open('files/{}_files.txt'.format(contrast), 'r') as f:
            full_files_list = f.read().splitlines()
    else:
            full_files_list = all_files
    # Place holder for additional identifiers
    identifiers = []

    associated_file_dirs = []
    for associated_file in associated_files:
        matches = []
        for full_file_path in full_files_list:
            if re.search(associated_file, full_file_path):
                # Remove the relative portion of the associated file from the full file path to get the required directory
                file_dir = full_file_path.replace(associated_file, '')
                matches.append(file_dir)
                #associated_file_dirs.append(file_dir)
        if len(matches) > 1:
            if len(identifiers) == 0:
                print('Warning: {} matched with the following directories: {}'.format(associated_file, matches))
                identifier = input('Enter additional identifying information: ')
                identifiers.append(identifier)
            refined_matches = []
            for match in matches:
                for id in identifiers:
                    if re.search(id, match):
                        refined_matches.append(match)
            matches = refined_matches
        elif len(matches) == 0:
            if associated_file in ["CHANGES", "README", "dataset_description.json"]:
                matches.append(associated_file_dirs[0])
            elif '.dlabel.nii' in associated_file:
                matches.append('/home/feczk001/shared/data/ABCD/')
        #print(matches)

        assert (len(matches) == 1), 'ERROR: {} matched with {}'.format(associated_file, matches)
        associated_file_dirs.append(matches[0])

            
    if len(associated_file_dirs) != len(associated_files):
        print('ERROR: Missing {} of {} associated file directories'.format(len(associated_files) - len(associated_file_dirs), len(associated_files)))
        continue
    else:
        resume_command_dir = os.path.join(os.getcwd(), 'resume_cmds')
        if not os.path.isdir(resume_command_dir):
            os.makedirs(resume_command_dir)
        with open(os.path.join(resume_command_dir, 'resume_{}.txt'.format(submission_id)), 'w') as r:
            cmd = ['~/.local/bin/vtcmd', '-r', submission_id, '-l', ' '.join(associated_file_dirs)]
            cmd_str = ' '.join(cmd) + '\n'
            r.write(cmd_str)








