#synACS_panda.py
#William Sexton
#3/8/2016

#imports
import pandas as pd
import numpy as np
import sys
import csv
import glob
import os.path
import logging
from gen_output import produce_housing_output
from gen_output import produce_person_output
from firstpass import process_housing_chunk
from firstpass import process_person_chunk


def set_alpha(df,gq_serials, count_dict, yearCode, alpha):
    """alpha is the prior parameter for the dirichlet distribution
    df is a pandas dataframe containing a chunk of data from the raw ACS housing data
    gq_serials is a pandas dataframe indexed by group quarter serial numbers with a single person weight column PWGTP
    count_dict, yearCode,defined elsewhere in code for bookkeeping purposes
    alpha stores prior probabilities for Dirichlet distribution over records of housing data"""
    
    df["ADJINC"]=df["ADJINC"].map(yearCode) #convert ADJINC to year
    
    #convert year to count_dict key for housing units/group quarters
    df.loc[(df["TYPE"]==1),"ADJINC"]=df.loc[(df["TYPE"]==1),"ADJINC"].map({2010:"n2010h",2011:"n2011h",2012:"n2012h",2013:"n2013h",2014:"n2014h"})
    df.loc[(df["TYPE"]!=1),"ADJINC"]=df.loc[(df["TYPE"]!=1),"ADJINC"].map({2010:"n2010g",2011:"n2011g",2012:"n2012g",2013:"n2013g",2014:"n2014g"})
    
    df["ADJINC"]=df["ADJINC"].map(count_dict) #convert year to count
    
    df.set_index("serialno")
    df=df.join(gq_serials) #Add person weight column to dataframe where person weight is NaN for households
    
    df=df.fillna(0) #Sets Household person weight to 0.
    #A household person weight PWGTP is 0 and group quarter weight WGTP is 0 so summing PWGTP and WGTP gives desired weight column.
    #ADJINC has been converted to include year by housing type count factors
    #count_dict includes total weight.
    alpha.extend(((df["WGTP"]+df["PWGTP"])*df["ADJINC"]/count_dict["weight"]).tolist())
    return alpha






def main():
    """Builds synthetic population using Bayesian bootstrapping process on ACS housing records and then populating
    each housing unit/group quarters unit with person records from the ACS person data files"""     
    
    """Configure log"""
    #Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='ACS.log',format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')
    
    
    """Set file paths"""
    person_raw=sys.argv[1] #This should be path to raw ACS person files
    filenames_person=glob.glob(os.path.join(person_raw,"*.csv")) #list of four person files
    logging.debug(filenames_person)
    
    housing_raw=sys.argv[2] #This should be path to raw ACS housing files
    filenames_housing=glob.glob(os.path.join(housing_raw,"*.csv")) #list of four housing files
    logging.debug(filenames_housing)
    
    
    
    """Bookkeeping"""
    yearCode={1094136:2010,1071861:2011,1041654:2012,1024037:2013,1008425:2014} #See data dictionary for ADJINC
    
    count_dict={"total":0, "n2010h":0, "n2011h":0, "n2012h":0, "n2013h":0, "n2014h":0, #n%yr%h is number of observed housing records in yr 
                "n2010g":0, "n2011g":0, "n2012g":0, "n2013g":0, "n2014g":0,"weight":0} #n%yr%g is number of observed group quarters in yr
    
        
    """First pass of housing files to collect aggregate counts and store serial numbers"""
    #Files processed in chunks due to memory limitations.
    #This approach requires multiple read ins of the data to complete the Bayesian bootstrapping
    #but it works. If there is a better way of doing this, I'd love to see it.
    serials=[]
    for f in filenames_housing:
        for chunk in pd.read_csv(f,usecols=["serialno","ADJINC","TYPE","WGTP"],chunksize=100000): #Restrict to necessary columns
            count_dict,serials=process_housing_chunk(chunk,count_dict,yearCode,serials)
            
    """First pass at person files to find person weights associated with group quarters records"""
    #Goal is to produce dataframe with all group quarters serialno as the the index and associated weights in a single column.
    df_list=[]
    for f in filenames_person:
        for chunk in pd.read_csv(f,usecols=["serialno","PWGTP","RELP"],chunksize=100000): #Restrict to necessary columns
            df_list.append(process_person_chunk(chunk))
    gq_serials=pd.concat(df_list)
    count_dict["weight"] += gq_serials['PWGTP'].sum() #Update total weight to include group quarters weights.
    
    """Next pass at housing is to define the prior parameter alpha for the dirichlet distribution."""
    alpha=[]
    for f in filenames_housing:
        for chunk in pd.read_csv(f,usecols=["serialno","ADJINC","TYPE","WGTP"],chunksize=100000):
            alpha=set_alpha(chunk,gq_serials,count_dict,yearCode,alpha)
    
    logging.info(len(alpha)==count_dict['total']) #sanity check
    
    
    
    """Bayesian bootstrap using dirichlet-Multinomial model"""
    N=132598198+8015581 #target size is number of housing units + group quarters population estimates for 2012.
    theta=np.random.dirichlet(alpha) #Draw Multinomial probabilities from prior.
    counts=np.random.multinomial(N,theta) #Draw N sample from Multinomial.
    logging.info(len(counts)==len(serials))
    counts=pd.DataFrame({'Count':counts},index=serials) #Dataframe with housing serialno's as index an count column indicating
    
      
    idx_base=0
    mydict=[]
    i=0
    for f in filenames_housing:
        for chunk in pd.read_csv(f,dtype=str,chunksize=100000):
            ofile='housing_rep/repHus%s.csv' %i
            i+=1
            idx_base, subdict=produce_housing_output(chunk,counts,idx_base,ofile)
            mydict.append(subdict)
    mydict={k:v for d in mydict for k,v in d.items()} #not a syntax error in python 2.7
    
    i=0
    for f in filenames_person:
        for chunk in pd.read_csv(f,dtype=str,chunksize=100000):
            ofile='person_rep/repPus%s.csv' %i
            i+=1
            produce_person_output(chunk,counts,mydict,ofile)
    
    
    logging.info('Finished')
    return
    

if __name__ == '__main__':
    np.random.seed(1138) #To facilitate replication.
    main()