# 6. file-mapper JSON files

The [file
mapper](https://github.com/DCAN-Labs/file-mapper) JSON
files are used together with the lookup CSV and the target directory
passed to the ***`prepare.py`*** script to create NDA formatted
directories.  A collection of file mapper JSON file examples are
available [within the nda-bids-upload GitHub
repository](https://github.com/DCAN-Labs/nda-bids-upload/tree/master/examples/json).

*File mapper JSON Example 1*

```
{
    "CHANGES": "CHANGES",
    "README": "README",
    "dataset_description.json": "dataset_description.json",
    
    "HCP/derivatives/abcd-hcp-pipeline/sub-{SUBJECT}/ses-{SESSION}/anat/sub-{SUBJECT}_ses-{SESSION}_space-ACPC_dseg.nii.gz": 
    "derivatives/abcd-hcp-pipeline/sub-{SUBJECT}/ses-{SESSION}/anat/sub-{SUBJECT}_ses-{SESSION}_space-ACPC_dseg.nii.gz"
}
```

Critically, each JSON file can have more than one file specified.
Furthermore, files need not be MRI images. Files could even be a zip
file.

These JSON files are organized in a two part *key* and *value* system:

-   **`files_source: files_destination`**

The **`files_source`** is the **\*relative\*** path under the target
directory passed to prepare.py. The **`files_destination`** is the
**\*relative\*** path under the child directory as dictated by the BIDS
format. The relative path is relative to the source path you provide
when running prepare.py. Do not use **\*full\*** paths because the code
will not accept forward slashes as the first character for either the
**`files_source`** or the **`files_destination`**.

As seen in *File mapper JSON Example 1*, the subject and session labels
are filled in by the placeholder variables `{SUBJECT}` and `{SESSION}`. This
is so all of the subjects (and sessions) found in the lookup CSV can
have the same file mapper JSON files applied to them. All subjects and
sessions will be symlinked using your provided JSON files.
