# rep_syn_housing.py
# William Sexton
# 11/22/2017
#
# Synthesize the housing data

# imports
import pandas as pd
import numpy as np
import sys
import csv
import glob
import os.path
import logging
from gen_output import produce_housing_output

def main(args):
    """Builds synthetic housing population using Bayesian bootstrapping process on ACS housing records"""     
    
    """Configure log"""
    # Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='SynHousing.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started housing output')
    
    """Set file paths and create output directory"""
    housing_raw  =  args.housingdir
    filenames_housing = sorted(glob.glob(os.path.join(housing_raw, "*.csv"))) #list of four housing files
    counts = pd.read_csv(args.repcount, index_col=0) #Dataframe with housing serialno's as index an count column indicating
    logging.debug(filenames_housing)    

    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    i = 0
    for f in filenames_housing:
        logging.debug("reading {}".format(f))
        for chunk in pd.read_csv(f, dtype=str, chunksize=500000):
            ofile = os.path.join(args.outdir, 'repHus%04d.csv' %i)
            i += 1
            produce_housing_output(chunk, counts, ofile)
    logging.info('Finished')

if __name__ == '__main__':
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description="Make synthetic houses",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--housingdir", help="path to raw ACS housing files", default="../inputs/housing_data")
    parser.add_argument("--repcount", default="rep_counts.csv")
    parser.add_argument("--outdir", help="output directory for repHusI.csv file", default="../outputs/housing_rep")
    args = parser.parse_args()
    main(args)
    
   
