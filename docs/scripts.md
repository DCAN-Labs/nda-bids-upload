# 5. Using prepare and upload scripts

## `Setting up your system`

When using `prepare.py`,`records.py` and `upload.py` there is a list of things that must exist before the use of the scripts.

1. Python 3.6 needs to be wherever the scripts are being run.  If it is not Python 3.6 you will get an error form the NDA's scripts.  You can either use a system Python 3.6 or a virtual environment with Python 3.6.  ([setting up a virual environment documentation](https://docs.python.org/3.6/tutorial/venv.html)).

2. The Python YAML dictionary must be installed into which ever environment you are runing these scrripts on. ([installing YAML dictionary](https://pypi.org/project/PyYAML/))

3. Install NDA tools into your Python 3.6 environment ([link to the GitHub for nda-tools](https://github.com/NDAR/nda-tools)).  To install `nda-tools`, use the command:

    ```shell
    python3.6 -m pip install nda-tools --user
    ```

4. Create an upload directory and move all appropriate JSON files and lookup CSV into it.

5. Create a pair of directories under the upload directory. They need to be named `manifest` and `file_mapper`

6. Download the DCAN Labs's `file_mapper_script.py` script.  Clone it into the `file_mapper` directory.  Once it is cloned permissions to the script need to be changed to `755 (-rwxr-xr-x)`.  A link to the DCAN Lab's Gitlab for the file_mapper_script and how to clone it can be found in the Appendix

7. Download the NDA's `nda_manifest.py` script.  Clone it into the `manifest` directory.  Once it is cloned permissions to the script need to be changed to `755 (-rwxr-xr-x)`.  A link to the NDA's Github for the nda_manifest script and how to clone it can be found in the Appendix

## Using `prepare.py`

When using `prepare.py` there are two mandatory flags:

`--destination` (or `-d`): The upload directory mentioned above in set four. This directory is going to be where all of the data will be organized under after data_perpare.py has finished.

`--target` (or `-t`): The directory under which all data the is wanted for upload can be found. This is often a self made directory or the output of a pipeline.

Once this script has been run you will want to check the results. In the upload directory you will find a parent/child directory setup. You should have a parent directory for each of the JSON files. They should have the same name as their corosponding file. Underneither you should find a README, CHANGES, dataset_description.json and child direcotry for ever subject [and session] that was found to have the relevent files listed in the corispoding JSON. If there are no child files under the parent directory then the script couldn't find any of the relavent files listed in the JSON.

The child directory should be labeled thusly.

**`S.X.Y.Z`**

There is also an expected naming convention for the "child" directories.  At the child directory level the naming convention has four "sections", `S.X.Y.Z`.  Three of those are the exact same as above, `"X.Y.Z"`.  The first is `"S."` instead of `"A_"` (the `"."` instead of `"_"` is intentional).

### Section `S`

Defined like this:

**`sub-<subjectlabel>[_ses-<sessionlabel>]`**

Where:

* `<subjectlabel>` needs to be replaced by your actual BIDS-standard subject label
* `<sessionlabel>` needs to be replaced by your actual BIDS-standard session label
* The square brackets around `[_ses-<sessionlabel>]` implies this block is optional, but it should be used if you have multiple sessions for single subjects within a dataset.

Remember: BIDS labels (`<subjectlabel>` and `<sessionlabel>`) are **ONLY** alphanumeric.  Spaces, underscores, hyphens, and any other seperators are **NOT ALLOWED**.

## Example 1: Prepared Parent and Child Directories

### `fmriresults01_inputs.anat.T1w`

Below a parent directory named `fmriresults01_inputs.anat.T1w` the scripts will expect any amount of BIDS-formatted standard folders, one for each individual subject or session record you want to upload.  Read on for how the child directories should be formatted.

```ascii
fmriresults01_inputs.anat.T1w/
└── sub-NDARABC123_ses-baseline.inputs.anat.T1w
```

You can see the different sections put together here:

1. `A` is `fmriresults01`
1. `X` is `inputs`
1. `Y` is `anat`
1. `Z` is `T1w`
1. `S` is `sub-NDARABC123_ses-baseline`, (the session is being labeled)
    * `<subjectlabel>` is `NDARABC123`
    * `<sessionlabel>` is `baseline`

### `sub-NDARABC123_ses-baseline.input.anat.T1w`

Within all child directories there **MUST** be a valid BIDS standard directory hierarchy underneath that follows a standard BIDS folder layout **from the top folder**.

For inputs, use the Official BIDS Validator to check for validity.  For derivatives, remember that there should be `derivatives/<pipeline>` prior to your subject-specific and session-specific derivative folders.

For example, starting with the prepared child directory:

### `sub-NDARABC123_ses-baseline.input.anat.T1w/sub-NDARABC123/ses-baseline/anat/...`

The final directory structure from the parent directory down should follow like the examples below.

## Example 2: BIDS Anatomical Inputs

```ascii
fmriresults01_inputs.anat.T1w/
└── sub-NDARABC123_ses-baseline.inputs.anat.T1w
    ├── CHANGES
    ├── dataset_description.json
    ├── README
    └── sub-NDARABC123
        └── ses-baseline
            └── anat
                ├── sub-NDARABC123_ses-baseline_T1w.json
                └── sub-NDARABC123_ses-baseline_T1w.nii.gz
```

## Example 3: BIDS Derivatives

```ascii
fmriresults01_derivatives.func.runs_task-rest/
└── sub-NDARABC123_ses-baseline.derivatives.func.runs_task-rest
    └── derivatives
        └── abcd-hcp-pipeline
            └── sub-NDARABC123
                └── ses-baseline
                    └── func
                        ├── sub-NDARABC123_ses-baseline_task-rest_run-1_bold_timeseries.dtseries.nii
                        ├── sub-NDARABC123_ses-baseline_task-rest_run-1_motion.tsv
                        ├── sub-NDARABC123_ses-baseline_task-rest_run-2_bold_timeseries.dtseries.nii
                        └── sub-NDARABC123_ses-baseline_task-rest_run-2_motion.tsv
```

If you directoried do not look to be formatted correctly please check your JSON files for proper formatting.

## Using `records.py`

When using `records.py` there are three mandatory flags:

`--source` (or `-s`): The upload directory mentioned above in set four.

`--lookup` (or `-l`): The lookup flag expects the complete path to the lookup.csv that was covered in part 2 of this README.

`--manifest` (or `-m`): The manifest flag expects the complete path to the `nda_manifest.py` script mentioned at the head of this section of the README.

## Using `upload.py`

When using `upload.py` there are three mandatory flags:

`--collection` (or `-c`): The collection flag needs an **NDA Collection ID**.

`--source` (or `-s`): The source flag expects the complete path to the parent directory from part 1 of this README.  The expected basename of the provided path should have the structure `A_X.Y.Z`.  The script will fail if this is not the case.

`--ndavtcmd` (or `-vt`): The ndavtcmd flag expects the direct path to the `vtcmd` script.

Examples:

```bash
# Maybe it is in your local Python installation binaries folder
~/.local/bin/vtcmd

# Or maybe a Python virtualenv you made in the "..." folder
.../virtualenv/bin/vtcmd
```
