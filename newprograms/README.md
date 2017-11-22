# Creating a synthetic population for a whole country
- Author: William Sexton
- Last Modified: 3/31/17

This directory contains the most recent version of the code used to create SynPopulation. We modified the bootstrap process to account for flaws in the previous versions. This code maintains the runtime improves of [ACS_multiprocessing](/labordynamicsinstitute/SynUSpopulation/tree/ACS_multiprocess).

## Download
You first need to download the files from the Census website. This can be done with the downloader script.

## Inputs
Assumes you have folders containing the raw ACS person and raw ACS housing data within the directory containing python code.

## Outputs

Also you must create the follow empty folder: housing_rep, person_rep, person_recode.

## To run
`python gen_counts.py [folder for raw ACS person data] [folder for raw ACS housing data]`

`python rep_syn_housing.py [folder for raw ACS housing data]`

`python rep_syn_person.py [folder for raw ACS person data]`

`python recode.py [folder containing output from rep_syn_person]`
