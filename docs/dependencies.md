# 1. Installation/Dependencies

Set up the environment you will be uploading from with the following:

Note: this could be your computer, a [virtual environment](https://docs.python.org/3.6/tutorial/venv.html),
or a conda environment

-   Python 3.6 

-   Python [YAML dictionary](https://pypi.org/project/PyYAML/) package 

-   Install [NDA tools](https://github.com/NDAR/nda-tools) 

-   Clone the [file-mapper GitHub repository](https://github.com/DCAN-Labs/file-mapper) and ensure that file-mapper-script.py is executable

-   Clone the [NDA manifest-data GitHub repository](https://github.com/NDAR/manifest-data) and ensure that nda_manifest.py is executable 

## Creating NDA Upload Directory

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

