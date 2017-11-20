#syn_housing.py
#William Sexton
#3/30/2017

#imports
import pandas as pd
import numpy as np
import pickle
import sys
import csv
import glob
import os.path
import logging
from gen_output import produce_housing_output



def main():
    """Builds synthetic housing population using Bayesian bootstrapping process on ACS housing records"""     
    
    """Configure log"""
    #Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='ACS.log',format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started housing output')
    
    
    """Set file paths"""
    housing_raw=sys.argv[1] #This should be path to raw ACS housing files
    filenames_housing=glob.glob(os.path.join(housing_raw,"*.csv")) #list of four housing files
    logging.debug(filenames_housing)
            
    counts=pd.read_csv("rep_counts.csv",index_col=0) #Dataframe with housing serialno's as index an count column indicating
    
    idx_base=0
    mydict=[]
    i=0
    for f in filenames_housing:
        for chunk in pd.read_csv(f,dtype=str,chunksize=500000):
            ofile='../output/housing_rep/repHus%s.csv' %i
            i+=1
            idx_base, subdict=produce_housing_output(chunk,counts,idx_base,ofile)
            mydict.append(subdict)
            
    mydict={k:v for d in mydict for k,v in d.items()}
    pickle.dump(mydict,open("serial_idx_dict.p","wb"))  
    logging.info('Finished')
    return
    

if __name__ == '__main__':
   main()
    
   
