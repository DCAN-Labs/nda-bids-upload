# 4. Preparing file-mapper JSON files

The file-mapper JSONs are used in the prepare.py script.  They are used They are used together with the lookup CSV to map the data into BIDS standard format.

## Example 1: file mapper JSON

```ascii
{
    "CHANGES": "CHANGES",
    "README": "README",
    "dataset_description.json": "dataset_description.json",
    "HCP/derivatives/abcd-hcp-pipeline/sub-{SUBJECT}/[ses-{SESSION}/]anat/sub-{SUBJECT}[_ses-{SESSION}]_space-ACPC_dseg.nii.gz": "derivatives/abcd-hcp-pipeline/sub-{SUBJECT}/[ses-{SESSION}/]anat/sub-{SUBJECT}[_ses-{SESSION}]_space-ACPC_dseg.nii.gz"
}
```

The square brackets around `[_ses-{SESSION}/]` and all other session related section implies these blocks are optional, but it should be used if you have multiple sessions for single subjects within a dataset.

These JSON files are organized in a two part system `files_location: files_destination`. The `files_location` is the path under the target directory passed to prepare.py. The `files_destination` is the path under the child directory as dictated by the BIDS format. The child directory will be explained in section X and a link to the BIDS format can be found in the Appendix.

As seen in Example 1, the subject and session lables are filled in with variables. This so the all of the subject (and sessions) found in the lookup CSV can have these files applied to them.
