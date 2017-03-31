Author: William Sexton
Last Modified: 3/23/17

Synthetic population housing and person files readme. The synthetic population was generated from the 2010-2014 ACS PUMS housing and person files. These data are meant to be representative of the 2012 US population. Stress testing to determine whether these data can actually reproduce accurate statistics for 2012 is still underway.

Details explaining how the synthetic population was produced along with the programs that did the job can be provided if desired.

There are 17 housing files repHus0.csv, repHus1.csv, ... repHus16.csv and 32 person files rep_recode_ACSpus0.csv, rep_recode_ACSpus1.csv, ... rep_recode_ACSpus31.csv.

Files are split to be roughly equal in size. The files contain data for the entire US. Files are not split along any demographic characteristic. The person files and housing files must be concatenated to form a complete person file and a complete housing file, respectively.

If desired, person and housing records should be merged on 'id'. Variable description is below.

Data Dictionary
See 2010-2014 ACS PUMS data dictionary. All variables from the ACS PUMS housing files are persent in the synthetic housing files and all variables from the ACS PUMS person files are present in the synthetic person files. And these variables have not been modified in any way. Though theoretically variables like person weight no longer have any use in the synthetic population. 

Additional variables.
'id': Both the synthetic housing and person files include this variable. It is meant as an extension/recode of the existing 'serialno' variable.  Each housing/group quarters unit in the synthetic population gets a unique 'id' and each person in the synthetic population gets linked to exactly one housing/group quarter unit by 'id'.  
'id' takes values from 0 to 140613778.

Race recode in person files. Variable names are striaghtforward but somewhat cumbersome.
**** These aren't variables but use these to intrepret variable names ****
WHT - white
BLK - black or African American
AIAN - American indian or Alaskan native
ASN - Asian
NHPI - native Hawaiian or pacific islander
SOR - some other race
**** There are 63 race recode variables. Each take on 0/1 values. No further description beyond name is required ****
isWHT
isBLK
isAIAN
isASN
isNHPI
isSOR
isWHTandBLK
isWHTandAIAN
isWHTandASN
isWHTandNHPI
isWHTandSOR
isBLKandAIAN
isBLKandASN
isBLKandNHPI
isBLKandSOR
isAIANandASN
isAIANandNHPI
isAIANandSOR
isASNandNHPI
isASNandSOR
isNHPIandSOR
isWHTandBLKandAIAN
isWHTandBLKandASN
isWHTandBLKandNHPI
isWHTandBLKandSOR
isWHTandAIANandASN
isWHTandAIANandNHPI
isWHTandAIANandSOR
isWHTandASNandNHPI
isWHTandASNandSOR
isWHTandNHPIandSOR
isBLKandAIANandASN
isBLKandAIANandNHPI
isBLKandAIANandSOR
isBLKandASNandNHPI
isBLKandASNandSOR
isBLKandNHPIandSOR
isAIANandASNandNHPI
isAIANandASNandSOR
isAIANandNHPIandSOR
isASNandNHPIandSOR
isWHTandBLKandAIANandASN
isWHTandBLKandAIANandNHPI
isWHTandBLKandAIANandSOR
isWHTandBLKandASNandNHPI
isWHTandBLKandASNandSOR
isWHTandBLKandNHPIandSOR
isWHTandAIANandASNandNHPI
isWHTandAIANandASNandSOR
isWHTandAIANandNHPIandSOR
isWHTandASNandNHPIandSOR
isBLKandAIANandASNandNHPI
isBLKandAIANandASNandSOR
isBLKandAIANandNHPIandSOR
isBLKandASNandNHPIandSOR
isAIANandASNandNHPIandSOR
isWHTandBLKandAIANandASNandNHPI
isWHTandBLKandAIANandASNandSOR
isWHTandBLKandAIANandNHPIandSOR
isWHTandBLKandASNandNHPIandSOR
isWHTandAIANandASNandNHPIandSOR
isBLKandAIANandASNandNHPIandSOR
isWHTandBLKandAIANandASNandNHPIandSOR

