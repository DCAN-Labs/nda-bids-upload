# Run and Validate Prepare and Upload Scripts

## Using `prepare.py`

The prepare.py script runs filemapper on the data to be uploaded as
specified in the lookup.csv contained in the upload folder (eg
destination folder for prepare.py). If any of the parent directories
are completely empty, it will delete those folders. It then runs records.py on all of
the file-mapped folders to create manifest JSONs and records.csv, which
contains a list of full paths to all files to upload. 

When using
[prepare.py](https://github.com/DCAN-Labs/nda-bids-upload/blob/master/prepare.py)
there are four mandatory flags:

```
--source (-s): The directory under which all data desired
for upload is found. This is usually the output of a pipeline like
Dcm2Bids or abcd-hcp-pipeline. It is the directory your file mapper
JSONs will be mapping from.

--destination (-d): The upload directory you began in [step two](workingdirectory.md). 
This directory is going to be where all of the data will be
organized after prepare.py has finished.

--subject-list: A list of subjects and session pairs within a .csv
file with column labels "bids_subject_id" and "bids_session_id,"
respectively.

--datatypes: A list of NDA data types within a .txt file you plan
to upload.
```

`prepare.py` should create the following:

* parent/child directories for each datatype 
* complete_folders.txt: contains one line with path to location of that particular file prepped for upload
* complete_records.csv: contains all data for that subject pulled from lookup.csv 
* folders_1_500_1.txt: prepare.py separates out the subject files in separate batches of 500 files each. Eg if there were 1400 files (or is it subjects?), there would be 3 submissions, batch 1 with 500 files, batch 2 with 500 files, and batch 3 with 400 files 
* Companion csv for each txt - manifest.txt information for the files being uploaded


## Validating `prepare.py`

Once this script has been run you will want to spot check the results.

You can validate that all of the expected subjects are present in each
of the datatype folders by running the `validate-prepare.py` script with 
your `subject_list.csv` and your working directory as the inputs. This script
will loop through each datatype folder and compare the subject list to the 
subject IDs present in the folder. It will output a text file containing the 
subject IDs that are in the subject list but not in the datatype folders.  
If there are many subjects missing, part of the issue could be that the lookup.csv
does not contain all of the subjects that it should, so be sure to double check
that all of the subjects listed in the `subject_list.csv` are also in the `lookup.csv`

This script should also create several types of files. It will create pairs of csv and 
txt files that separate out the subject files in separate batches of 500 files each, with the
naming convention {datatype-folder}.records_{num-of-subjects}_500_{batch-number}. For example 
if there were 1400 subjects, there would be 3 submissions: batch 1 and 2 with 500 subjects each 
and batch 3 with 400 subjects. The txt/csv for the final batch would be named
`fmriresults01_derivatives.anat.space-ACPC_dseg.records_1400_500_3.csv/txt`. The companion csv 
contains the manifest.txt information for the files being uploaded.

You should also validate the directory structure of the datatype folders 
that were created. In the upload directory, you will find a parent/child directory setup.
You should have a parent directory for each of the JSON/YAML file pairs 
where relevant files were found.
They should have the same name as their corresponding JSON/YAML files
without the extensions. Underneath you should find a child directory for
every subject (and session if used) that was found to have the relevant
files listed in the corresponding file mapper JSON. 

You will notice a common naming convention for the "child" directories
as well. At the child directory level the naming convention has four
"sections" which follow the model "**<span style="color:green">S</span>.<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>**". The same conventions as
above are followed, with one important exception. The first component 
"**<span style="color:green">S</span>.**" replaces "**<span style="color:red">A</span>_**". The "**<span style="color:green">S</span>.**" represents the
**bids_subject_session** in the lookup.csv file. Below are three
examples to highlight different variations. 

**Example 1: Prepared Parent and Child Directories**

***<span style="color:red">fmriresults</span>_<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>***

Below a parent directory named **<span style="color:red">fmriresults</span>_<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>** the
scripts will expect any amount of BIDS-formatted standard folders, one
for each individual subject or session record you want to upload. Read
on for how the child directories should be formatted.

**<span style="color:red">fmriresults</span>_<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>**/<br>
└── **<span style="color:green">sub-NDARABC123_ses-baseline</span>.<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>**

You can see the different sections put together here:

1.  **<span style="color:red">A</span> is <span style="color:red">fmriresults</span>**

2.  **<span style="color:blue">X</span> is <span style="color:blue">inputs</span>**

3.  **<span style="color:gold">Y</span> is <span style="color:gold">anat</span>**

4.  **<span style="color:purple">Z</span> is <span style="color:purple">T1w</span>**

5.  **<span style="color:green">S</span> is <span style="color:green">sub-NDARABC123_ses-baseline</span>, (the session is being labeled)**

-   **`<subjectlabel>` is <span style="color:green">NDARABC123</span>**

-   **`<sessionlabel>` is <span style="color:green">baseline</span>**

Within all child directories you will find a directory hierarchy created
by your file mapper JSONs underneath.

For BIDS inputs, use the official BIDS Validator to check for validity.
For BIDS derivatives, remember that there should be
**`derivatives/<pipeline>`** prior to your subject-specific and
session-specific derivative folders.

For example, starting from the prepared child directory:

**<span style="color:green">sub-NDARABC123_ses-baseline</span>.<span style="color:blue">input</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>/sub-NDARABC123/ses-baseline/anat**

The final directory structure from the parent directory down should
follow like the examples below.

**Example 2: BIDS Anatomical Inputs**

**<span style="color:red">fmriresults</span>_<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>**/<br>
└── **<span style="color:green">sub-NDARABC123_ses-baseline</span>.<span style="color:blue">inputs</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w</span>**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `CHANGES`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `dataset_description.json`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `README`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `sub-NDARABC123`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `ses-baseline`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `anat`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `sub-NDARABC123_ses-baseline_T1w.json`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `sub-NDARABC123_ses-baseline_T1w.nii.gz`

**Example 3: BIDS Derivatives**

**<span style="color:red">fmriresults</span>_<span style="color:blue">derivatives</span>.<span style="color:gold">func</span>.<span style="color:purple">runs_task-rest</span>**/<br>
└── **<span style="color:green">sub-NDARABC123_ses-baseline</span>.<span style="color:blue">derivatives</span>.<span style="color:gold">func</span>.<span style="color:purple">runs_task-rest</span>**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `derivatives`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `abcd-hcp-pipeline`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `sub-NDARABC123`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `ses-baseline`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `func`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `sub-NDARABC123_ses-baseline_task-rest_run-1_bold_timeseries.dtseries.nii`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `sub-NDARABC123_ses-baseline_task-rest_run-1_motion.tsv`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `sub-NDARABC123_ses-baseline_task-rest_run-2_bold_timeseries.dtseries.nii`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `sub-NDARABC123_ses-baseline_task-rest_run-2_motion.tsv`

If your directories are not formatted correctly please check your file
mapper JSON files for proper formatting.

## Using `upload.py`

Before you begin the upload process, we recommend sending the NDA a curtesy email letting them know that you are about to start uploading data. If possible, provide an estimate of how much data is going to be uploaded. 

The `upload.py` script uses `records.csv` (generated by `prepare.py` above) to
split the files to be uploaded into batches of 500. For each batch, the
script loops through each of the file paths to generate and run the
necessary upload command using NDA-tools.

When using upload.py there are three mandatory arguments:

**`--collection`** (or **`-c`**): The collection flag needs an **NDA
Collection ID**. You can find collection IDs in the [NDA
repository](https://nda.nih.gov/). For instance, the ABCC
is 3165, ASD-BIDS is 1955, ADHD-BIDS years 1-8 is 2857, and ADHD-BIDS
years 9-12 is 3222.

**`--source`** (or **`-s`**): The source flag expects the complete path to
the **<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>** subfolder within the **destination** directory from
**prepare.py**. This should be the exact same path as the **`--source`**
specified for **prepare.py**. The expected basename of the provided path
MUST have the structure **<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>**. The script will fail if this is not
the case.

**`--ndavtcmd`** (or **`-vt`**): The ndavtcmd flag expects the absolute
path to the vtcmd script. 

> *Example \--ndavtcmd:* `~/.local/bin/vtcmd`
> 
> *\# if it is in your local Python installation binaries folder*\
> 

The first time this script is run, you should be prompted for your NIMH
username and password, which is then stored in
`\~/.NDATools/settings.cfg`. However, if only your username is stored in that file, create a `pass.txt` file in your working directory (that only you can read/write) to store just your NDA password.

Find the upload logs, validation results, and submission package here: `\~/NDA/nda-tools/vtcmd`

## Validate `upload.py`

After running `upload.py`, check that the submission was successful. As the upload is running, you should receive emails from the NDA confirming your submission for each batch. First check the output logs for any errors. Then, follow the steps below to check the submission on the NDA:

1. Log into the NDA

2. Navigate to your dashboard.

3. Click on "Collections (#)"

4. Click on the collection name you uploaded to.

5. Click on the "Submissions" tab and check the "Submission Loading Status"