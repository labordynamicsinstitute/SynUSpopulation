# Synthetic population housing and person records for the United States
- Author: William Sexton
- Last Modified: 11/29/17

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
There is a set of housing files
- repHus0.csv, repHus1.csv, ...
and a set of person files
- repPus0.csv, repPpus1.csv, ...

Files are split to be roughly equal in size. The files contain data for the entire country. Files are not split along any demographic characteristic. The person files and housing files must be concatenated to form a complete person file and a complete housing file, respectively.

If desired, person and housing records should be merged on 'id'. Variable description is below.

## Data Dictionary
See [2010-2014 ACS PUMS data dictionary](http://doi.org/10.3886/E100486V1). All variables from the ACS PUMS housing files are present in the synthetic housing files and all variables from the ACS PUMS person files are present in the synthetic person files. Variables have not been modified in any way. Theoretically, variables like `person weight` no longer have any use in the synthetic population.

### Additional variables.
- `id`: Both the synthetic housing and person files include this variable. It is meant as an extension/recode of the existing `serialno` variable.  `id` has the form _serialno_._replicationno where _serialno_ is the `serialno` and _replicationno_ is a nonnegative integer ranging from 0 up to _n-1_ where _n_ is the number of times the household/GQ with `serialno` = _serialno_ was replicated in the synthetic population. 
