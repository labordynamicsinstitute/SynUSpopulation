#synACS_panda.py
#William Sexton
#Last Modified: 3/30/2016

#imports
import pandas as pd
import numpy as np
import multiprocessing as mp
import pickle
import sys
import csv
import glob
import os.path
import logging
from gen_output import produce_person_output



def main():
    """Builds synthetic population using Bayesian bootstrapping process by populating
    each replicated housing unit/group quarters unit with person records from the ACS person data files"""     
    
    """Configure log"""
    #Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='SynPopulation.log',format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')
    
    
    """Set file paths"""
    person_raw="../inputs/person_data/" #This should be path to raw ACS person files
    filenames_person=glob.glob(os.path.join(person_raw,"*.csv")) #list of four person files
    logging.debug(filenames_person)
    
                
    counts=pd.read_csv("rep_counts.csv",index_col=0) #Dataframe with housing serialno's as index an count column indicating
    mydict=pickle.load(open("serial_idx_dict.p","rb"))
    logging.info('before pool')
    
    pool=mp.Pool(16) #Modify number of processes here
            
    i=0
    funclist=[]
    for f in filenames_person:
        for chunk in pd.read_csv(f,dtype=str,chunksize=10000):
            ofile='../outputs/person_rep/repPus%s.csv' %i
            i+=1
            logging.info('new job')
            res = pool.apply_async(produce_person_output,[chunk,counts,mydict,ofile])
            funclist.append(res)
    for res in funclist:
        res.wait()
    
    logging.info('Finished')
    return
    

if __name__ == '__main__':
       
    main()
    
    
