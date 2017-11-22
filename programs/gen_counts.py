#!/usr/bin/env python3.5
# gen_counts.py
# William Sexton
# Last Modified: 11/22/2017
""" Generate counts over serialno's """

# imports
import os.path
import logging
import glob
import pandas as pd
import numpy as np
import acs

def process_chunk(df, cnt_dict, serials, unitType):
    """ inputs: pandas dataframe--either from ACS person or ACS housing files,
                count dictionary,
                list of serialnos,
                unitType is 'HH' or 'GQ'
        (1) map serialno to year, first 4 digits of serialno are the year
        (2) filter to unitType and increment record weight total
        (3) increment total of unitType
        (4) extend list by serialnos in filtered df
        (5) increment observation counts for each year 
        return: count dictionary and serial list of unitType """
    df["YEAR"] = df[acs.SERIALNO].map(lambda serialno: serialno[:4]) 

    if unitType == "GQ":
        df = df[(df["RELP"] == "16") | (df["RELP"] == "17")] # filter to GQ type
        cnt_dict["weight"] += df["PWGTP"].astype(int).sum()
    else:
        df = df[df["TYPE"] == "1"] # filter to housing unit
        cnt_dict["weight"] += df["WGTP"].astype(int).sum()

    cnt_dict["total"] += len(df.index)
    serials.extend(df[acs.SERIALNO].tolist())

    cnt = df.groupby("YEAR").size() 
    for key in cnt_dict:
        cnt_dict[key] += cnt.get(key, 0)
    return cnt_dict, serials

def set_alpha(df, cnt_dict, alpha, unitType):
    """ inputs: pandas dataframe--either from ACS person or ACS housing files 
                count_dict, 
                list of prior probabilities for Dirichlet distribution over records of unitType,
                unitType is 'HH' or 'GQ'
        (1) map serialno to year, first 4 digits of serialno are the year
        (2) map year to counts of unitType
        (3) filter to unitType and extend list of probabilities
        return: extended list of probabilities over unitType records  """
    df["YEAR"] = df[acs.SERIALNO].map(lambda serialno: serialno[:4]) 
    df["YEARCNT"] = df["YEAR"].map(cnt_dict)
    if unitType == "GQ":
        df = df[(df["RELP"] == "16") | (df["RELP"] == "17")] # filter to GQ
        alpha.extend((df["PWGTP"].astype(int)*df["YEARCNT"]/cnt_dict["weight"]).tolist())
    else:
        df = df[df["TYPE"] == "1"] # filter to housing units
        alpha.extend((df["WGTP"].astype(int)*df["YEARCNT"]/cnt_dict["weight"]).tolist())
    return alpha

def main(args):
    """ Builds synthetic population using Bayesian bootstrapping process
        on ACS housing records and then populating each
        housing unit/group quarters unit with person records
        from the ACS person data files."""     
    """1. Configure log"""
    # Change filename with each run (if desired) otherwise info
    # will append to same log.
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(filename='gen_counts.log',
            format='%(asctime)s %(message)s', level=logging_level)
    logging.info('Started')
    # Get the files from the provided directories
    # Notes that glob.glob() filenames are sorted.
    # Strictly there is no reason to do this, but it makes debugging easier.
    filenames_person = sorted(glob.glob(os.path.join(args.persondir,"*.csv")))
    logging.debug("filenames_person: {}".format(filenames_person))
    filenames_housing = sorted(glob.glob(os.path.join(args.housingdir,"*.csv")))
    logging.debug("filenames_housing: {}".format(filenames_housing))
    """2. Set up Bookkeeping"""
    #
    # cnt_[GQ | HH] is where we keep track of the counts,
    # for each year, of group quarters and households.
    #
    # index: {YEAR}  where YEAR is the 4 digit year
    #        total: total number of GQ | HH
    #        weight: summed weight over all GQ | HH
    cnt_GQ = {"total":0, "2010":0, "2011":0, "2012":0,
                  "2013":0, "2014":0, "weight":0} 
    cnt_HH = {"total":0, "2010":0, "2011":0, "2012":0,
                  "2013":0, "2014":0, "weight":0}

    """First pass of housing files to collect aggregate counts
       and store serial   numbers of households"""
    # Files processed in chunks to reduce memory footprint.
    # This approach requires multiple read ins of the data to complete
    # the Bayesian bootstrapping but it works. If there is a better way
    # of doing this, I'd love to see it.

    # serials_HH is the array of serial numbers of households
    serials_HH = []
    for f in filenames_housing[0:args.maxstates]:
        logging.info("computing serials_HH reading housing "+f)
        for chunk in pd.read_csv(f, dtype=str,
                                 usecols=[acs.SERIALNO, "TYPE", "WGTP"],
                                 chunksize=10000):
            cnt_HH, serials_HH = process_chunk(chunk,
                                                          cnt_HH,
                                                          serials_HH,
                                                          "HH")
    """First pass at person files to collect aggregate counts
       and store serial numbers of group quarters records"""
    # serials_GQ is an array of the serial numbers of group quarters
    serials_GQ = []
    for f in filenames_person[0:args.maxstates]:
        logging.info("computing serials_GQ reading persons "+f)
        for chunk in pd.read_csv(f, dtype=str,
                                 usecols=[acs.SERIALNO, "PWGTP", "RELP"],
                                 chunksize=10000):
            cnt_GQ, serials_GQ = process_chunk(chunk,
                                                         cnt_GQ, 
                                                         serials_GQ,
                                                         "GQ")
    """Next pass at housing is to define the prior parameter alpha
       for the dirichlet distribution over households."""
    # alpha_HH is the array of weights of households
    alpha_HH = []
    for f in filenames_housing[0:args.maxstates]:
        logging.info("computing alpha_HH reading housing "+f)
        for chunk in pd.read_csv(f, dtype=str,
                                 usecols=[acs.SERIALNO, "TYPE", "WGTP"],
                                 chunksize=10000):
            alpha_HH = set_alpha(chunk, cnt_HH, alpha_HH, "HH")
    """Next pass at person is to define the prior parameter alpha
       for the dirichlet distribution over group quarters."""
    # alpha_GQ is the array of weights of group quarters
    alpha_GQ = []
    for f in filenames_person[0:args.maxstates]:
        logging.info("computing alpha_GQ reading persons "+f)
        for chunk in pd.read_csv(f, dtype=str,
                                 usecols=[acs.SERIALNO, "RELP", "PWGTP"],
                                 chunksize=10000):
            alpha_GQ = set_alpha(chunk, cnt_GQ, alpha_GQ, "GQ")
    # Verify that the number of weights for households and group quarters
    # matches the number of labels. 
    assert len(serials_GQ) == len(alpha_GQ)
    assert len(serials_GQ) == cnt_GQ["total"]
    assert len(serials_HH) == len(alpha_HH)
    assert len(alpha_HH) == cnt_HH["total"]
    
    """ Bayesian bootstrap simulation of households using
       dirichlet-Multinomial model """
    N_HH = 132598198 # target size is number of housing units for 2012.
    theta_HH  = np.random.dirichlet(alpha_HH) # Draw Multinomial probabilities
                                            # from prior.
    counts_HH = np.random.multinomial(N_HH, theta_HH) # Draw N sample from
                                                   # Multinomial.
    counts_HH = pd.DataFrame({'Count':counts_HH}, index=serials_HH) # Dataframe
                      # with housing serialno's as index of the count column.

    """ Bayesian bootstrap simulation of group quarters using
       dirichlet-Multinomial model """
    N_GQ = 8015581 #target size is group quarters population for 2012.
    theta_GQ = np.random.dirichlet(alpha_GQ) # Draw Multinomial probabilities
                                           # from prior.
    counts_GQ = np.random.multinomial(N_GQ, theta_GQ) # Draw N sample from
                                                   # Multinomial.
    counts_GQ = pd.DataFrame({'Count':counts_GQ}, index=serials_GQ) # Dataframe
               # with group quarters serialno's as index of the count column.
    counts = pd.concat([counts_HH, counts_GQ])
    counts.to_csv(args.output)
    logging.info('Wrote output to {}. Finished'.format(args.output))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--debug",action='store_true')
    parser.add_argument("--output",help="output file",default="rep_counts.csv")
    parser.add_argument("--maxstates",default=4,type=int,help="Maximum number of states to compute")
    parser.add_argument("--persondir",help="directory for person ACS files", default="../inputs/person_data")
    parser.add_argument("--housingdir",help="directory for person ACS files", default="../inputs/housing_data")
    args = parser.parse_args()

    np.random.seed(1138) # To facilitate replication.
    main(args)
