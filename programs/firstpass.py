#firstpass.py
#William Sexton
#Daniel Lin
#Last Modified: 10/02/2017
import pandas as pd
import numpy as np

def process_person_chunk(df,count_dict,yearCode,serials_g):
    """df is a pandas dataframe containing a chunk of raw ACS person data.
    cound_dict has counts of observed records by year by housing type. Also has total counts.
    yearCode is dictionary for mapping ADJINC to year.
    serials_g is a list of group quarters serial numbers."""
    df=df[(df["RELP"]==16) | (df["RELP"]==17)] #Filter to only include group quarters records. See data dictionary for RELP description.
    
    if df.empty:
        return count_dict, serials_g
    count_dict["total_g"] += len(df.index) #Increases running tally for total number of processed group quarters records
    count_dict["weight_g"] += df['PWGTP'].sum() #Increases running tally for total sum of processed group quarters weights

    serials_g.extend(df["serialno"].tolist()) #Adds serials from current data chunk onto list

    #converts 'ADJINC' variable to years
    df['ADJINC'] = df['ADJINC'].map(yearCode)
    
    #counting group quarters by year
    
    cnt_g=df.groupby("ADJINC").size() #returns pandas series
    #Increase counts by observed number in current chunk, .get(yr,0) returns 0 if no record was observed in yr.
    count_dict["n2011g"] += cnt_g.get(2011,0)
    count_dict["n2012g"] += cnt_g.get(2012,0)
    count_dict["n2013g"] += cnt_g.get(2013,0)
    count_dict["n2014g"] += cnt_g.get(2014,0)
    count_dict["n2015g"] += cnt_g.get(2015,0)
    
    
    return count_dict, serials_g #returns dataframe with serialno set as index and single column containing PWGTP

def process_housing_chunk(df,count_dict,yearCode,serials_h):
    """Goal is to collect information from all raw ACS housing data files.
    Information is collected by aggregating over chunks of data.
    df is pandas dataframe for a chunk of housing data
    count_dict is a dictionary with values representing observed counts for each key.
    yearCode is dictionary used to map 'ADJINC' variable to year following ACS data dictionary specification
    serials_h is a list for storing all processed serials from household records"""
    #count_dict keys ={total, n2011h, n2012h, n2013h, n2014h, n2015h, n2011g, n2012g, n2013g, n2014g, n2015g,weight}
    
    
    df=df[df["TYPE"]==1] #TYPE 1 is housing unit
    if df.empty:
        return count_dict, serials_g
    count_dict["total"] += len(df.index) #Increases running tally for total number of processed records
    count_dict["weight"] += df['WGTP'].sum() #Increases running tally for total sum of processed weights

    serials_h.extend(df["serialno"].tolist()) #Adds serials from current data chunk onto list

    #converts 'ADJINC' variable to years
    df['ADJINC'] = df['ADJINC'].map(yearCode)
    
    #counting housing by year
    
    cnt_h=df.groupby("ADJINC").size() #returns pandas series
    #Increase counts by observed number in current chunk, .get(yr,0) returns 0 if no record was observed in yr.
    count_dict["n2011h"] += cnt_h.get(2011,0)
    count_dict["n2012h"] += cnt_h.get(2012,0)
    count_dict["n2013h"] += cnt_h.get(2013,0)
    count_dict["n2014h"] += cnt_h.get(2014,0)
    count_dict["n2015h"] += cnt_h.get(2015,0)
          
    return count_dict, serials_h
