# ACS PUMS Person data
This directory should contain the following files:

- ss14pusa.csv  
- ss14pusb.csv  
- ss14pusc.csv  
- ss14pusd.csv

where `14` denotes the particular vintage of ACS, adjust as necessary.

## Original location at Census Bureau

- http://www2.census.gov/programs-surveys/acs/data/pums/2013/5-Year/csv_pus.zip
- http://www2.census.gov/programs-surveys/acs/data/pums/2014/5-Year/csv_pus.zip
- http://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_pus.zip

## DataLumos copies of sources:

- http://doi.org/10.3886/E100517V2 (2009-2013)
- http://doi.org/10.3886/E100486V2 (2010-2014)
- http://doi.org/10.3886/E100521V2 (2011-2015)

## Simple script

```
pref_year=2014
for file in $(grep census.gov README.md | grep $pref_year )
do
  wget $file
done
```


