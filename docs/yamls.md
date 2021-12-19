# 3. Preparing NDA content YAML files

The content YAMLs are used in the prepare.py script.  They are used to create the appropriate NDA data structures for a valid upload.

## YAML files

The content YAML files are used together with the lookup CSV to construct the `fmriresults01`, `image03`, or `imagingcollection01` CSV files.  There are three categories that these fields fall into: **Required**, **Conditional**, and **Recommended**.  Required fields **MUST** be filled with NDA-valid information.  Conditional fields **MUST** be filled if their condition is met.  Recommended fields do not need to be filled, but should be filled if information is available.

There are three YAML files provided.

* `fmriresults01_required.yaml`
* `fmriresults01_complete.yaml`
* `fmriresults01_full_NDA.yaml`

The pair of **complete** and **required** yaml files are used to provide relavent information to **prepare.py**.  These files **MUST** stay in the `content` directory under `nda-bids-upload-prepare`.

## [fmriresults01](https://nda.nih.gov/data_structure.html?short_name=fmriresults01)

There are values found on the NDA site that are not listed below. That is because `records.py` uses the provided files to generate the values stored in the fields `manifest` and `image_description`.

### Required

* `file_source`
* `pipeline`
* `pipeline_script`
* `pipeline_tools`
* `pipeline_type`
* `pipeline_version`
* `qc_fail_quest_reason`
* `qc_outcome`
* `scan_type`

### Conditional

* `derived_files`

The field `derived_files` is conditional on whether or not the field `manifest` is filled.  Since `records.py` generates and fills the `manifest` field, `derived_files` is unnecessary.

### Recommended

* `origin_dataset_id`
* `experiment_id`
* `inputs`
* `img03_id`
* `job_name`
* `proc_types`
* `metric_files`
* `img03_id2`
* `file_source2`
* `session_det`
* `image_history`
