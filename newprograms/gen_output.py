#gen_output.py
#William Sexton
#Last Modified: 3/30/16
""" Functions to write output """
import numpy as np
import acs
def produce_housing_output(df, counts, ofile):
    """df is pandas dataframe containing chunk of raw housing data.
    counts is a dataframe indexed by serialno with column listing number
    of replicants to produce.
    idx_base determines where index should start for each new chunk
    to produce a unique id for each replicated record.
    ofile is the current output file"""
    df = df.set_index(acs.SERIALNO)
    df.index = df.index.astype(int)
    df = df.join(counts)
    assert df["Count"].isnull().any() == False 
    # Adds count column onto dataframe
    df = df.loc[np.repeat(df.index.values, df["Count"])] # Replicants rows
                                                         # according to count
                                                         # number
    df = df.reset_index(level=[acs.SERIALNO]) # changes serialno back into
                                                # dataframe column
    unique_id = df.groupby(acs.SERIALNO).cumcount()
    df['id'] = df[acs.SERIALNO].astype(str) + '.' + unique_id.astype(str)
    df = df.drop('Count', 1)
    df.to_csv(ofile, index=False)
   
def produce_person_output(df, counts, ofile):
    """df is dataframe containing chunk of raw ACS person data
    counts is a dataframe indexed by serialno with column listing number
    of replicants to produce.
    mydict is a dictionary key:value = serialno:list of corresponding ids
    for unique instances of serialno in housing records.
    ofile is the current output file"""
    # logging.info('inside function')
    df = df.set_index(acs.SERIALNO)
    df.index = df.index.astype(int)
    # logging.info('set index')
    df = df.join(counts) #Adds count column onto dataframe
    # logging.info('join')
    assert df["Count"].isnull().any() == False
    df.index.name = acs.SERIALNO
    df = df.reset_index(level=[acs.SERIALNO]) # Converts serialno back to column
    df = df.loc[np.repeat(df.index.values, df["Count"])] # Replicants rows
                                                        # according to count
                                                        # number
    # Each person with serialno gets replicated once for each household
    # in the synthetic housing file with serialno
    # Each such person must be uniquely linked to one of the replicated
    # households so we must adjust ids accordingly
    # ie if a person is in a household that got replicated 10 times we just
    # made 10 copies of that person but we still
    # need to assign one copy to each household.
    # logging.info('duplicate')
    df.index.name = 'id' #Set index name
    df = df.reset_index(level=['id']) #Converts index into column
    unique_id = df.groupby('id').cumcount()
    df['id'] = df[acs.SERIALNO].astype(str) + '.' + unique_id.astype(str)
        # adjusts ids to match one copy of person to each replicated household
    df = df.drop('Count', 1)
    #logging.info('end id, begin file')
    df.to_csv(ofile, index=False)
    #logging.info('end file')
    return
