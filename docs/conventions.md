# 1. File naming conventions

YAML and JSON files are always paired. If a YAML file is created then a JSON must be made with the same file name.

## File naming Format

**`A_X.Y.Z`**

When creating JSON and YAML files there is an expected naming convention.  The naming convention has four "sections", `A_X.Y.Z` with `.yaml` or `.json` on the end depending on the type of file that is being created.

## For all sections

There are two restrictions on naming conventions.

1. Periods `"."` should only be used in the separations between sections `X`, `Y` and `Z`.
2. Underscores `"_"` should only be used in EITHER the separation between sections `A` and `X` OR in the naming of section `Z`.

## Section `A`

Must be:

* `fmriresults01`
* `image03`

The `fmriresults01` data structure should be used for any processed MRI or fMRI data with the NDA.  The `imagingcollection01` data structure is being phased out by the NDA for non-HCP and non-ABCD studies.  `imagingcollection01` is therefore deprecated within these tools. For non-HCP and non-ABCD studies use `fmriresults01` for all none source data. For all source use the `image03` data structure.

## Section `X`

Can be:

* `inputs`
* `derivatives`
* `sourcedata`

For section `X` there are currently these options.  `inputs` are the as-acquired data in BIDS format.  `derivatives` are the results of processing inputs.  `sourcedata` are things like task timing files and other raw/as-acquired data.

## Section `Y`

Usually BIDS standard data naming, but is allowed to deviate:

* `anat`
* `dwi`
* `fmap`
* `func`
* `executivesummary`
* (similar entries)

There are BIDS naming conventions for some of these entities.  Other naming conventions can be created as necessary.

## Section `Z`

An open-ended and user-defined data subset type.  It is recommended to use something concise enough to convey the contents of what you've prepared.
