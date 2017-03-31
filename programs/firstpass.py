#firstpass.py
#William Sexton
import pandas as pd
import numpy as np

def process_person_chunk(df):
    """df is a pandas dataframe containing a chunk of raw ACS person data"""
    df=df[(df["RELP"]==16) | (df["RELP"]==17)] #Filter to only include group quarters records. See data dictionary for RELP description.
    df=df.drop("RELP",1) #No longer necessary.
    df=df.set_index('serialno')
    return df #returns dataframe with serialno set as index and single column containing PWGTP

def process_housing_chunk(df,count_dict,yearCode,serials):
    """Goal is to collect information from all raw ACS housing data files.
    Information is collected by aggregating over chunks of data.
    df is pandas dataframe for a chunk of housing data
    count_dict is a dictionary with values representing observed counts for each key.
    yearCode is dictionary used to map 'ADJINC' variable to year following ACS data dictionary specification
    serials is a list for storing all processed serials from housing records"""
    #count_dict keys ={total, n2010h, n2011h, n2012h, n2013h, n2014h, n2010g, n2011g, n2012g, n2013g, n2014g,weight}
    
    count_dict["total"] += len(df.index) #Increases running tally for total number of processed records
    count_dict["weight"] += df['WGTP'].sum() #Increases running tally for total sum of processed weights

    serials.extend(df["serialno"].tolist()) #Adds serials from current data chunk onto list

    #converts 'ADJINC' variable to years
    df['ADJINC'] = df['ADJINC'].map(yearCode)
    
    #counting housing by year
    df_h=df[df["TYPE"]==1] #TYPE 1 is housing unit
    cnt_h=df_h.groupby("ADJINC").size() #returns pandas series
    #Increase counts by observed number in current chunk, .get(yr,0) returns 0 if no record was observed in yr.
    count_dict["n2010h"] += cnt_h.get(2010,0)
    count_dict["n2011h"] += cnt_h.get(2011,0)
    count_dict["n2012h"] += cnt_h.get(2012,0)
    count_dict["n2013h"] += cnt_h.get(2013,0)
    count_dict["n2014h"] += cnt_h.get(2014,0)
    
    
    #counting group quarters by year
    df_g=df[df["TYPE"]!=1] #Type 2 and 3 are group quarters
    cnt_g=df_g.groupby("ADJINC").size()
    
    count_dict["n2010g"] += cnt_g.get(2010,0)
    count_dict["n2011g"] += cnt_g.get(2011,0)
    count_dict["n2012g"] += cnt_g.get(2012,0)
    count_dict["n2013g"] += cnt_g.get(2013,0)
    count_dict["n2014g"] += cnt_g.get(2014,0)  
       
    return count_dict, serials