# DCAN Labs NDA BIDS Uploading Tools

This ReadTheDocs site covers installation, five data preparation steps, and
upload specfically for imaging data, which falls under "non-cumulative"
data. By the end of this upload document, the upload folder will contain
JSON and YAML file pairs, a lookup CSV, and subfolders per JSON and YAML
file pair (containing their own file-mapped subfolders with symbolic
links to the actual files you are uploading).

The major steps include:

1.  Install dependencies

2.  Create a NDA Upload Directory

3.  Run prepare.py to filemap the associated data and create the records
    files by datatype for each subject

4.  Run upload.py to validate and upload the data

5.  Create a help desk ticket (send an email to NDAHelp@mail.nih.gov)
    indicating that you are ready for c3165  DCAN Labs ABCD-BIDS
    Community Collection (ABCC) to be QA\'d stating your submission IDs.

## Table of Contents

1.  Installation/Dependencies 

2.  Creating an NDA Upload Directory

3.  Preparing Lookup CSV

4.  Naming conventions of Content YAML and file-mapper JSON files

5.  Content YAML files

6.  file-mapper JSON files

7.  Using Prepare and Upload Scripts

8.  Appendix/Glossary

# 1. Installation/Dependencies

Set up the environment you will be uploading from with the following:

Note: this could be your computer, a [virtual environment](https://docs.python.org/3.6/tutorial/venv.html),
or a conda environment

-   Python 3.6 

-   Python [YAML dictionary](https://pypi.org/project/PyYAML/) package 

-   Install [NDA tools](https://github.com/NDAR/nda-tools) 

-   Clone the [file-mapper GitHub repository](https://github.com/DCAN-Labs/file-mapper) and ensure that file-mapper-script.py is executable

-   Clone the [NDA manifest-data GitHub repository](https://github.com/NDAR/manifest-data) and ensure that nda_manifest.py is executable 

# 2. Creating NDA Upload Directory

1.  Create a working directory for your submissions

2.  Within that directory include the following:

    a.  a datatypes.txt file including a list of all of the NDA datatypes you plan to upload

    b.  a subject_list.csv file containing a list of the subjects and their sessions you plan to upload with the column headers bids_subject_id and bids_session_id, respectively.

    c.  scripts set up to run prepare.py and uploads.py
    
3.  Assure that your version of the nda-bids-upload repository includes
    a JSON and YAML pair for the datatypes you are uploading within its
    examples directory.

    a.  If these do not exist, see <ins>2.2 Preparing Content YAML and File Mapper JSON files</ins> for instructions on how to create them.

4.  Include the lookup.csv for the data you are uploading inside your working directory. 

    a.  If these do not exist, see <ins>2.1 Preparing a lookup CSV file</ins>

INSERT TREE OF WORKING DIR
