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

**<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>.json**<br>
**<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>.yaml**

When creating JSON and YAML files there is an expected naming
convention. The naming convention has four "sections", **<span style="color:red">A</span>_<span style="color:blue">X</span>.<span style="color:gold">Y</span>.<span style="color:purple">Z</span>** with
**`.yaml`** or **`.json`** on the end depending on the type of file that is
being created. 

*For all sections*

There are two restrictions on naming conventions.

1.  Periods "**.**" should only be used in the separations between sections **<span style="color:blue">X</span>**, **<span style="color:gold">Y</span>**, and **<span style="color:purple">Z</span>**.

2.  An underscore "**_**" MUST be used in the separation between sections **<span style="color:red">A</span>** and **<span style="color:blue">X</span>**. Underscores are allowed in the naming of section **<span style="color:purple">Z</span>**.

A valid content YAML and file mapper JSON pair would be named as such:\
**<span style="color:red">fmriresults01</span>_<span style="color:blue">derivatives</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w_MNI</span>.json**

**<span style="color:red">fmriresults01</span>_<span style="color:blue">derivatives</span>.<span style="color:gold">anat</span>.<span style="color:purple">T1w_MNI</span>.yaml**

*Descriptions of the naming conventions are given below:*

### <span style="color:red">Section A</span>

Section A must be:

-   **<span style="color:red">fmriresults01</span>**

-   **<span style="color:red">image03</span>**

-   **<span style="color:red">imagingcollection01</span>**

The **<span style="color:red">fmriresults01</span>** data structure should be used for any processed
MRI or fMRI data with the NDA. The **<span style="color:red">imagingcollection01</span>** data
structure is being phased out by the NDA for non-HCP and non-ABCD
studies. **<span style="color:red">imagingcollection01</span>** is therefore deprecated within these
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
