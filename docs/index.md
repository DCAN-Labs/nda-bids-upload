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

1.  Installation/Dependencies/Creating an NDA Upload Directory

2.  Preparing Lookup CSV

3.  Naming conventions of Content YAML and file-mapper JSON files

4.  Content YAML files

5.  file-mapper JSON files

6.  Using Prepare and Upload Scripts

7.  Appendix/Glossary
