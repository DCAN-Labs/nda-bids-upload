#!/bin/bash

#SBATCH -J ABCC_Upload
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=30gb
#SBATCH -t 48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user={INSERT YOUR EMAIL HERE}
#SBATCH -o sbatch_upload%A_%a.out
#SBATCH -e sbatch_upload%A_%a.err
#SBATCH -A feczk001

conda activate /home/rando149/shared/code/external/envs/nda-uploads

# Read the array from the file into the upload_directories variable
readarray -t upload_directories < upload_directories.txt

# Loop through each value in the array and echo it
for directory in "${upload_directories[@]}"; do
    echo "Uploading ${directory}"
    password=`cat pass`
    expect -c "
    set timeout -1
    spawn /home/rando149/shared/projects/ABCD/ABCC_Upload/nda-bids-upload/upload.py -c 3165 -s ${directory} -vt /home/faird/mccol199/.local/bin/vtcmd
    expect \"Enter your NIMH Data Archives password:\" {send \"${password}\r\"; exp_continue}"
done