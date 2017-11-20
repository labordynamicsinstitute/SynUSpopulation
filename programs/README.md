# Creating a synthetic population for a whole country
- Author: William Sexton
- Last Modified: 3/31/17

This directory contains the most recent version of the code used to create SynPopulation. We modified the bootstrap process to account for flaws in the previous versions. This code maintains the runtime improves of [ACS_multiprocessing](/labordynamicsinstitute/SynUSpopulation/tree/ACS_multiprocess).

## Inputs
Assumes raw ACS person and raw ACS housing data are within the appropriate directories in SynUSpopulation/inputs/

## Outputs

The output will be generated in the provided directories of SynUSpopulation/outputs/

## To run
Assumes file structure of git repo. Code requires the current directory when run to be the programs directory.  
`python gen_counts.py`

`python rep_syn_housing.py`

`python rep_syn_person.py`

`python recode.py`
