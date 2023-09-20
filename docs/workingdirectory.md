# Create Your Uploads Working Directory

1.  Create a working directory for your submissions.

2.  Within that working directory include the following:

    a.  A datatypes.txt file including a list of all of the NDA datatypes you plan to upload

    b.  A subject_list.csv file containing a list of the subjects and their sessions you plan to upload with the column headers bids_subject_id and bids_session_id, respectively.

    c.  Scripts set up to run prepare.py and uploads.py on your system. Examples of what our team uses on MSI exist under the `utilities` directory inside [this repository](https://github.com/DCAN-Labs/nda-bids-upload).

3.  Copy or create your YAML and JSON pair files within your working directory under `prepared_yamls` and `prepared_jsons` directories, respectively.

    a.  If these do not exist, see [Create YAML and JSON Files](metadatafiles.md) for instructions on how to create them.

4.  Include the lookup.csv for the data you are uploading inside your working directory. 

    a.  If this does not exist, see [Prepare the Lookup CSV](lookup.md) for instructions on how to create it.

```

├── working directory
│   ├── prepared_yamls
│   ├── prepared_jsons
|   ├── datatypes.txt
|   ├── subject_list.csv
|   ├── lookup.csv
|   ├── run_prepare.sh
|   ├── run_upload.sh


```
<br />
