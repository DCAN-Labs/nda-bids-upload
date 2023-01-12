# 3. Preparing Content YAML and File Mapper JSON files

The content YAMLs and file mapper JSONs are used in the prepare.py
script. The YAMLs are used to create the NDA records for upload, which
contain all possible information that one can query about data. The
JSONs are used to symlink the data into individual subdirectories based
on NDA datatypes for ease of upload.  The content YAML and file mapper
JSON file's naming and content structure are provided below.

All content YAML files for each data structure are available within the [NDA Uploads
repository](https://github.com/DCAN-Labs/nda-bids-upload)
under examples.  Only valid NDA data structure content based on the
links above should be used in these YAML files.

## Content YAML and File Mapper JSON file naming conventions
JSON and YAML files are always paired. If a JSON file is created then a
YAML must be made with the same file prefix and different extension. 
For example, if `image03_sourcedata.anat.T1w.json` exists, then by
necessity `image03_sourcedata.anat.T1w.yaml` MUST also exist.

*File naming Format*

<img width="200" alt="Screenshot 2022-11-01 114831" src="https://user-images.githubusercontent.com/102316699/199289968-deb0ef10-5264-4578-bee0-69e41a768069.png">

When creating JSON and YAML files there is an expected naming
convention. The naming convention has four "sections", **`A_X.Y.Z`** with
**`.yaml`** or **`.json`** on the end depending on the type of file that is
being created. 

*For all sections*

There are two restrictions on naming conventions.

1.  Periods \"**.**\" should only be used in the separations between sections **X**, **Y**, and **Z**.

2.  An underscore \"**\_**\" MUST be used in the separation between sections **A** and **X**. Underscores are allowed in the naming of section **Z**.

A valid content YAML and file mapper JSON pair would be named as such:\
**`fmriresults01_derivatives.anat.T1w_MNI.json`**

**`fmriresults01_derivatives.anat.T1w_MNI.yaml`**

*Descriptions of the naming conventions are given below:*

<img width="100" alt="Screenshot 2022-11-01 115133" src="https://user-images.githubusercontent.com/102316699/199290610-e3af1791-5c2d-44b3-a07a-de8a28e97420.png">

Section A must be:

-   **`fmriresults01`**

-   **`image03`**

-   **`imagingcollection01`**

The **`fmriresults01`** data structure should be used for any processed
MRI or fMRI data with the NDA. The **`imagingcollection01`** data
structure is being phased out by the NDA for non-HCP and non-ABCD
studies. **`imagingcollection01`** is therefore deprecated within these
tools. For non-HCP and non-ABCD studies use **`fmriresults01`** for all
non-source data (ex: inputs, sourcedata, and derivatives). For all
sources, use the **`image03`** data structure (ex: DICOMs).

<img width="100" alt="Screenshot 2022-11-01 115328" src="https://user-images.githubusercontent.com/102316699/199291057-d4a5dbfd-5cbe-4a40-bf6c-db1911eaa885.png">

Section X can be:

-   **`inputs`**

-   **`derivatives`**

-   **`sourcedata`**

For section X there are currently these options. **`inputs`** are the
unprocessed imaging data in BIDS format. **`derivatives`** are the results
of processing the BIDS inputs. **`sourcedata`** are things like task
timing files (EventRelatedInformation) and other raw/as-acquired data
(eg DICOMs).

<img width="100" alt="Screenshot 2022-11-01 115450" src="https://user-images.githubusercontent.com/102316699/199291436-69d8bc56-be46-483a-a8a7-a4630ff02ac2.png">

Section Y usually uses BIDS standard data naming, but is also allowed to deviate:

-   **`anat`**

-   **`dwi`**

-   **`fmap`**

-   **`func`**

-   **`executivesummary`**

-   **`(similar entries)`**

There are BIDS naming conventions for some of these entities. These are
maintained within the BIDS specification and can be found
[here](https://bids-specification.readthedocs.io/en/stable/99-appendices/04-entity-table.html#magnetic-resonance-imaging).
Other naming conventions can be created as necessary.

<img width="100" alt="Screenshot 2022-11-01 115721" src="https://user-images.githubusercontent.com/102316699/199291771-164f0cec-dd9a-42fe-8366-27d775a04350.png">

Section Z is an open-ended and user-defined data subset type. It is recommended to
use something concise enough to convey the contents of what you've
prepared.
