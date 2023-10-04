#! /bin/bash

#SBATCH -J ABCC_Upload_Prepare
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=30gb
#SBATCH -t 96:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user={INSERT YOUR EMAIL HERE}
#SBATCH -o sbatch_prepare.out
#SBATCH -e sbatch_prepare.err
#SBATCH -A feczk001

module load python3/3.8.3_anaconda2020.07_mamba

python3 /home/rando149/shared/projects/ABCD/ABCC_Upload/nda-bids-upload/prepare.py \
-s /path/to/input_data \
-d /path/to/working_directory \
--subject-list=/path/to/working_directory/subject_list.csv \
--datatypes=/path/to/working_directory/datatypes.txt