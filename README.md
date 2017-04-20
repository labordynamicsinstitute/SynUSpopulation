# Synthetic population housing and person records for the United States
- Author: William Sexton
- Last Modified: 3/23/17

These data are meant to be representative of the 2012 US population.

## Inputs
The synthetic population was generated from the 2010-2014 ACS PUMS housing and person files.


    United States Department of Commerce. Bureau of the Census. (2017-03-06).
    American Community Survey 2010-2014 ACS 5-Year PUMS File [Data set].
    Ann Arbor, MI: Inter-university Consortium of Political and Social
    Research [distributor]. http://doi.org/10.3886/E100486V1

Persistent URL:  http://doi.org/10.3886/E100486V1

## Funding support
This work is supported under  Grant G-2015-13903 from the Alfred P. Sloan Foundation on "[The Economics of Socially-Efficient Privacy and Confidentiality Management for Statistical Agencies](https://www.ilr.cornell.edu/labor-dynamics-institute/research/project-19)" (PI: John M. Abowd)

## Testing
Stress testing to determine whether these data can actually reproduce accurate statistics for 2012 is still underway.

## Outputs
There are 17 housing files
- repHus0.csv, repHus1.csv, ... repHus16.csv
and 32 person files
- rep_recode_ACSpus0.csv, rep_recode_ACSpus1.csv, ... rep_recode_ACSpus31.csv.

Files are split to be roughly equal in size. The files contain data for the entire country. Files are not split along any demographic characteristic. The person files and housing files must be concatenated to form a complete person file and a complete housing file, respectively.

If desired, person and housing records should be merged on 'id'. Variable description is below.

## Data Dictionary
See [2010-2014 ACS PUMS data dictionary](http://doi.org/10.3886/E100486V1). All variables from the ACS PUMS housing files are present in the synthetic housing files and all variables from the ACS PUMS person files are present in the synthetic person files. Variables have not been modified in any way. Theoretically, variables like `person weight` no longer have any use in the synthetic population.

### Additional variables.
- `id`: Both the synthetic housing and person files include this variable. It is meant as an extension/recode of the existing `serialno` variable.  Each housing/group quarters unit in the synthetic population gets a unique `id` and each person in the synthetic population gets linked to exactly one housing/group quarter unit by `id`.
`id` takes values from 0 to 140613778.

- Race recode in person files. Variable names are straightforward but somewhat cumbersome. They are composed of `tokens` as follows:

  - WHT - white
  - BLK - black or African American
  - AIAN - American indian or Alaskan native
  - ASN - Asian
  - NHPI - native Hawaiian or pacific islander
  - SOR - some other race

**** There are 63 race recode variables. Each take on 0/1 values. No further description beyond name is required ****

- isWHT
- isBLK
- isAIAN
- isASN
- isNHPI
- isSOR
- isWHTandBLK
- isWHTandAIAN
- isWHTandASN
- isWHTandNHPI
- isWHTandSOR
- isBLKandAIAN
- isBLKandASN
- isBLKandNHPI
- isBLKandSOR
- isAIANandASN
- isAIANandNHPI
- isAIANandSOR
- isASNandNHPI
- isASNandSOR
- isNHPIandSOR
- isWHTandBLKandAIAN
- isWHTandBLKandASN
- isWHTandBLKandNHPI
- isWHTandBLKandSOR
- isWHTandAIANandASN
- isWHTandAIANandNHPI
- isWHTandAIANandSOR
- isWHTandASNandNHPI
- isWHTandASNandSOR
- isWHTandNHPIandSOR
- isBLKandAIANandASN
- isBLKandAIANandNHPI
- isBLKandAIANandSOR
- isBLKandASNandNHPI
- isBLKandASNandSOR
- isBLKandNHPIandSOR
- isAIANandASNandNHPI
- isAIANandASNandSOR
- isAIANandNHPIandSOR
- isASNandNHPIandSOR
- isWHTandBLKandAIANandASN
- isWHTandBLKandAIANandNHPI
- isWHTandBLKandAIANandSOR
- isWHTandBLKandASNandNHPI
- isWHTandBLKandASNandSOR
- isWHTandBLKandNHPIandSOR
- isWHTandAIANandASNandNHPI
- isWHTandAIANandASNandSOR
- isWHTandAIANandNHPIandSOR
- isWHTandASNandNHPIandSOR
- isBLKandAIANandASNandNHPI
- isBLKandAIANandASNandSOR
- isBLKandAIANandNHPIandSOR
- isBLKandASNandNHPIandSOR
- isAIANandASNandNHPIandSOR
- isWHTandBLKandAIANandASNandNHPI
- isWHTandBLKandAIANandASNandSOR
- isWHTandBLKandAIANandNHPIandSOR
- isWHTandBLKandASNandNHPIandSOR
- isWHTandAIANandASNandNHPIandSOR
- isBLKandAIANandASNandNHPIandSOR
- isWHTandBLKandAIANandASNandNHPIandSOR
