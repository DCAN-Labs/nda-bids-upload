# 3. Preparing Content YAML and File Mapper JSON files

The content YAMLs and file mapper JSONs are used in the prepare.py
script. The YAMLs are used to create the NDA records for upload, which
contain all possible information that one can query about data. The
JSONs are used to symlink the data into individual subdirectories based
on NDA datatypes for ease of upload.  The content YAML and file mapper
JSON file's naming and content structure are provided below.

There are example content YAML files for each of data structures within the 
[examples folder of the NDA Uploads repository.](https://github.com/DCAN-Labs/nda-bids-upload/tree/main/examples)
Only valid NDA data structure content based on the
links above should be used in these YAML files.

## Content YAML and File Mapper JSON file naming conventions
JSON and YAML files are always paired. If a JSON file is created then a
YAML must be made with the same file prefix and different extension. 
For example, if `fmriresults01_sourcedata.anat.T1w.json` exists, then by
necessity `fmriresults01_sourcedata.anat.T1w.yaml` MUST also exist.

**File naming Format**

**<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>.json**<br>
**<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>.yaml**

When creating JSON and YAML files there is an expected naming
convention. The naming convention has four "sections", **<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>** with
**`.yaml`** or **`.json`** on the end depending on the type of file that is
being created. 

**For all sections**

There are two restrictions on naming conventions.

1.  Periods "**.**" should only be used in the separations between sections **<span style="color:blue">X</span>**, **<span style="color:gold">Y</span>**, and **<span style="color:purple">Z</span>**.

2.  An underscore "**_**" MUST be used in the separation between sections **<span style="color:red">A</span>** and **<span style="color:blue">X</span>**. Underscores are allowed in the naming of section **<span style="color:purple">Z</span>**.

A valid content YAML and file mapper JSON pair would be named as such:

**<span style="color:red">fmriresults01</span>_<span style="color:blue">derivatives</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w_MNI</span>.json**

**<span style="color:red">fmriresults01</span>_<span style="color:blue">derivatives</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w_MNI</span>.yaml**

**Descriptions of the naming conventions are given below:**

### <span style="color:red">Section A</span>

Section A must be one of the following:

-   **<span style="color:red">fmriresults01</span>**

-   **<span style="color:red">image03</span>**

-   **<span style="color:red">imagingcollection01</span>**

The **<span style="color:red">fmriresults01</span>** data structure should be used for any processed
MRI or fMRI data with the NDA. The **<span style="color:red">imagingcollection01</span>** data
structure is being phased out by the NDA for non-HCP and non-ABCD
studies and is therefore deprecated within these
tools. For non-HCP and non-ABCD studies use **<span style="color:red">fmriresults01</span>** for all
non-source data (ex: inputs, sourcedata, and derivatives). For all
sources, use the **<span style="color:red">image03</span>** data structure (ex: DICOMs).

### <span style="color:blue">Section X</span>

Section X can be:

-   **<span style="color:blue">inputs</span>**

-   **<span style="color:blue">derivatives</span>**

-   **<span style="color:blue">sourcedata</span>**

For section X there are currently these options. **<span style="color:blue">inputs</span>** are the
unprocessed imaging data in BIDS format. **<span style="color:blue">derivatives</span>** are the results
of processing the BIDS inputs. **<span style="color:blue">sourcedata</span>** are things like task
timing files (EventRelatedInformation) and other raw/as-acquired data
(eg DICOMs).

### <span style="color:gold">Section Y</span>

Section Y usually uses BIDS standard data naming, but is also allowed to deviate:

-   **<span style="color:gold">anat</span>**

-   **<span style="color:gold">dwi</span>**

-   **<span style="color:gold">fmap</span>**

-   **<span style="color:gold">func</span>**

-   **<span style="color:gold">executivesummary</span>**

-   **<span style="color:gold">(similar entries)</span>**

There are BIDS naming conventions for some of these entities. These are
maintained within the BIDS specification and can be found
[here](https://bids-specification.readthedocs.io/en/stable/99-appendices/04-entity-table.html#magnetic-resonance-imaging).
Other naming conventions can be created as necessary.

### <span style="color:purple">Section Z</span>

Section Z is an open-ended and user-defined data subset type. It is recommended to
use something concise enough to convey the contents of what you've
prepared.

## Content YAMLs

The content YAML files are used together with the lookup CSV to
construct the NDA's required data structure for an upload. The fields
within these data structures are described in the NDA's data
dictionaries linked below.

-   [image03](https://nda.nih.gov/data_structure.html?short_name=image03)

-   [fmriresults01](https://nda.nih.gov/data_structure.html?short_name=fmriresults01)

-   [imagingcollection01](https://nda.nih.gov/data_structure.html?short_name=imagingcollection01)

There are three categories that each field within a data structure fall
into: **Required**, **Conditional**, and **Recommended**. 
**Required** fields MUST be filled with NDA-valid information. 
**Conditional** fields MUST be filled if their condition is met. 
**Recommended** fields do not need to be filled, but should be filled if information is available. The
"VALUE RANGE" column gives allowable values for each field

For example, according to the **`fmriresults01`** data dictionary
"scan_type" is a required element and "experiment_id" is a conditional
element. If "scan_type == fMRI" is specified then "experiment_id" is
required.

For further guidance on the values of each element use the 
[previously created content yamls](https://github.com/DCAN-Labs/nda-bids-upload/tree/main/examples) for the ABCC and ADHD collections as a reference. 

*Content YAML Example*

        inputs: "Updated data for the ABCC (ABCD-3165) August 2023 Release"
        file_source: "NDA Collection 3165: DCAN Labs ABCD-BIDS"
        job_name: "abcd-hcp-pipeline"
        proc_types: "Linux Docker processing on a slurm cluster"
        pipeline: "dcanlabs/abcd-hcp-pipeline:v0.1.3"
        pipeline_script: "https://hub.docker.com/r/dcanlabs/abcd-hcp-pipeline"
        pipeline_tools: "abcd-hcp-pipeline v0.1.3, ANTs v2.2.0, Convert3D v1.0.0, FreeSu
        rfer v5.3.0-HCP, FSL v5.0.10, MSM v2.00, Workbench v1.3.2, DCAN-Labs/DCAN-HCP, D
        CAN-Labs/dcan_bold_processing, DCAN-Labs/CustomClean, and DCAN-Labs/ExecutiveSum
        mary"
        pipeline_type: "Dockerized BIDS App for MRI session rocessing"
        pipeline_version: "v0.1.3"
        qc_fail_quest_reason: "Rated questionable because it has not been explicitly ver
        ified yet"
        qc_outcome: "questionable"
        scan_type: "MR structural"
        image_history: "See https://github.com/ABCD-STUDY/abcd-hcp-pipeline"

**Note:** Regarding the NDA required fields for fmriresults01: 
**`manifest`**, **`image_description`**, **`derived_files`**,
**`qc_fail_quest_reason`**, and **`qc_outcome`**:

1.  **`manifest`**, **`image_description`**, and **`derived_files`** should
    not be provided because ***`prepare.py`*** generates them correctly
    already.

2.  **`qc_fail_quest_reason`** and **`qc_outcome`** should be provided as
    **`questionable`** if QC was not performed.

## File-mapper JSON files

The [file mapper](https://github.com/DCAN-Labs/file-mapper) JSON
files are used together with the lookup CSV and the target directory
passed to the ***`prepare.py`*** script to create NDA formatted
directories.  A collection of file mapper JSON file examples are
available [within the nda-bids-upload GitHub repository](https://github.com/DCAN-Labs/nda-bids-upload/tree/master/examples/json).

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