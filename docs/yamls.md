# 4. Content YAML files

The content YAML files are used together with the lookup CSV to
construct the NDA's required data structure for an upload. The fields
within these data structures are described in the NDA's data
dictionaries linked below.

-   [image03](https://nda.nih.gov/data_structure.html?short_name=image03)

-   [fmriresults01](https://nda.nih.gov/data_structure.html?short_name=fmriresults01)

-   [imagingcollection01](https://nda.nih.gov/data_structure.html?short_name=imagingcollection01)

There are three categories that each field within a data structure fall
into: **Required**, **Conditional**, and **Recommended**. **Required**
fields MUST be filled with NDA-valid information. **Conditional** fields
MUST be filled if their condition is met. **Recommended** fields do not
need to be filled, but should be filled if information is available. The
"VALUE RANGE" column gives allowable values for each field

For example, according to the **`fmriresults01`** data dictionary
"scan_type" is a required element and "experiment_id" is a conditional
element. If "scan_type == fMRI" is specified then "experiment_id" is
required.

For further guidance on the values of each element use the previously
created content yamls for the ABCC and ADHD collections as a reference.

Note: Regarding the NDA required fields for fmriresults01: 
**`manifest`**, **`image_description`**, **`derived_files`**,
**`qc_fail_quest_reason`**, and **`qc_outcome`**:

1.  **`manifest`**, **`image_description`**, and **`derived_files`** should
    not be provided because ***`prepare.py`*** generates them correctly
    already.

2.  **`qc_fail_quest_reason`** and **`qc_outcome`** should be provided as
    **`questionable`** if QC was not performed.
