#gen_output.py
#William Sexton
#Last Modified: 3/11/16
import pandas as pd
import numpy as np
import csv
import logging

def produce_housing_output(df,counts,idx_base,ofile):
    """df is pandas dataframe containing chunk of raw housing data
    counts is a dataframe indexed by serialno with column listing number of replicants to produce
    idx_base determines where index should start for each new chunk to produce a unique id for each replicated record
    ofile is the current output file"""
    df=df.set_index('serialno')
    df.index=df.index.astype(int)
    df=df.join(counts)
    #Adds count column onto dataframe
    df=df.loc[np.repeat(df.index.values,df["Count"])] #Replicants rows according to count number
    df=df.reset_index(level=['serialno']) #changes serialno back into dataframe column
    df.index=range(idx_base,len(df)+idx_base) #sets unique ids for current chunk of data
    idx_base += len(df) #increments base id index
    df=df.drop('Count',1)
    df.to_csv(ofile,index_label='id')
    #Returns base id index and dictionary key:value = serialno: list of corresponding ids for unique instances of serialno.
    return idx_base, df.groupby('serialno').groups

def produce_person_output(df,counts,mydict,ofile):
    """df is dataframe containing chunk of raw ACS person data
    counts is a dataframe indexed by serialno with column listing number of replicants to produce
    mydict is a dictionary key:value = serialno:list of corresponding ids for unique instances of serialno in housing records
    ofile is the current output file"""
    #logging.info('inside function')   
    df=df.set_index('serialno')
    df.index=df.index.astype(int)
    #logging.info('set index')
    df=df.join(counts) #Adds count column onto dataframe
    #logging.info('join')
    df.index.name='serialno'
    df=df.reset_index(level=['serialno']) #Converts serialno back to column
    df=df.loc[np.repeat(df.index.values,df["Count"])] #Replicants rows according to count number
    #Each person with serialno gets replicated once for each household in the synthetic housing file with serialno
    #Each such person must be uniquely linked to one of the replicated households so we must adjust ids accordingly
    #ie if a person is in a household that got replicated 10 times we just made 10 copies of that person but we still
    #need to assign one copy to each household.
    #logging.info('duplicate')
    df.index.name='id' #Set index name
    df=df.reset_index(level=['id']) #Converts index into column
    myset=df.groupby('id').groups
    #logging.info('begin id')
    for key in myset:
        df.loc[myset[key],'id']=mydict[df.loc[myset[key][0],'serialno']] #adjusts ids to match one copy of person to each replicated household
    df=df.drop('Count',1)
    #logging.info('end id, begin file')
    df.to_csv(ofile,index=False)
    #logging.info('end file')
    return