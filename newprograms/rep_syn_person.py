# rep_syn_person.py
# William Sexton
# Last Modified: 11/22/2017

# imports
import logging
import glob
import os.path
import pandas as pd
# import numpy as np
import multiprocessing as mp
# import sys
# import csv
from gen_output import produce_person_output

def main(args):
    """ Builds synthetic population using Bayesian bootstrapping process by populating
    each replicated housing unit/group quarters unit with person records from the ACS person data files """

    """1. Configure log """
    # Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='SynPopulation.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')

    """Set file paths"""
    person_raw = args.persondir # This should be path to raw ACS person files
    filenames_person = glob.glob(os.path.join(person_raw, "*.csv")) # list of four person files
    logging.debug(filenames_person)

    counts=pd.read_csv("rep_counts.csv",index_col=0) # Dataframe with housing serialno's as index an count column indicating
    
    pool=mp.Pool(8) #Modify number of processes here
            
    i=0
    funclist=[]
    for f in filenames_person:
        for chunk in pd.read_csv(f,dtype=str,chunksize=10000):
            ofile='{}/repPus{}.csv'.format(args.outputdir, i)
            i+=1
            logging.debug("new job")
            res = pool.apply_async(produce_person_output,[chunk,counts,ofile])
            funclist.append(res)
    for res in funclist:
        res.wait()

    logging.info('Finished')
    return    

if __name__ == '__main__':
    from argparse import ArgumentParser
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--persondir", default="../inputs/person_data")
    arg_parser.add_argument("--repcounts", default="rep_counts.csv")
    arg_parser.add_argument("--outputdir", default="../outputs/person_rep")
    args = arg_parser.parse_args()
    if not os.path.exists(args.outputdir):
        os.mkdir(args.outputdir)
    main(args)
