#recode.py
#William Sexton
#3/15/17

#imports
import pandas as pd
import numpy as np
#import multiprocessing as mp
import glob
import os.path
import sys
import csv
import logging

def load_files(filelist):
    return pd.concat((pd.read_csv(f,dtype=str) for f in filelist),ignore_index=True)

def add_recode(df):
    #1 race
    df['isWHT']=((df["RACWHT"]=='1') & (df["RACNUM"]=='1')).astype(int)
    df['isBLK']=((df["RACBLK"]=='1') & (df["RACNUM"]=='1')).astype(int)
    df['isAIAN']=((df["RACAIAN"]=='1') & (df["RACNUM"]=='1')).astype(int)
    df['isASN']=((df["RACASN"]=='1') & (df["RACNUM"]=='1')).astype(int)
    df['isNHPI']=((df["RACNHPI"]=='1') & (df["RACNUM"]=='1')).astype(int)
    df['isSOR']=((df["RACSOR"]=='1') & (df["RACNUM"]=='1')).astype(int)
    logging.info('1 race done')
    #2 races
    ############## WHT + one
    df['isWHTandBLK']=((df["RACWHT"]=='1') & (df["RACBLK"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isWHTandAIAN']=((df["RACWHT"]=='1') & (df["RACAIAN"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isWHTandASN']=((df["RACWHT"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isWHTandNHPI']=((df["RACWHT"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isWHTandSOR']=((df["RACWHT"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='2')).astype(int)
    ############## BLK + one 
    df['isBLKandAIAN']=((df["RACBLK"]=='1') & (df["RACAIAN"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isBLKandASN']=((df["RACBLK"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isBLKandNHPI']=((df["RACBLK"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isBLKandSOR']=((df["RACBLK"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='2')).astype(int)
    ############## AIAN + one
    df['isAIANandASN']=((df["RACAIAN"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isAIANandNHPI']=((df["RACAIAN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isAIANandSOR']=((df["RACAIAN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='2')).astype(int)
    ############## ASN + one
    df['isASNandNHPI']=((df["RACASN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='2')).astype(int)
    df['isASNandSOR']=((df["RACASN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='2')).astype(int)
    ############## NHPI + one
    df['isNHPIandSOR']=((df["RACNHPI"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='2')).astype(int)
    logging.info('2 race done')
    #3 races
    ############## WHT + BLK + one
    df['isWHTandBLKandAIAN']=((df["RACWHT"]=='1') & (df["RACBLK"]=='1') & (df["RACAIAN"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandBLKandASN']=((df["RACWHT"]=='1') & (df["RACBLK"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandBLKandNHPI']=((df["RACWHT"]=='1') & (df["RACBLK"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandBLKandSOR']=((df["RACWHT"]=='1') & (df["RACBLK"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ############# WHT + AIAN + one    
    df['isWHTandAIANandASN']=((df["RACWHT"]=='1') & (df["RACAIAN"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandAIANandNHPI']=((df["RACWHT"]=='1') & (df["RACAIAN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandAIANandSOR']=((df["RACWHT"]=='1') & (df["RACAIAN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ############ WHT + ASN + one
    df['isWHTandASNandNHPI']=((df["RACWHT"]=='1') & (df["RACASN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isWHTandASNandSOR']=((df["RACWHT"]=='1') & (df["RACASN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ############ WHT + NHPI + one   
    df['isWHTandNHPIandSOR']=((df["RACWHT"]=='1') & (df["RACNHPI"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)

    ########### BLK + AIAN + one
    df['isBLKandAIANandASN']=((df["RACBLK"]=='1') & (df["RACAIAN"]=='1') & (df["RACASN"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isBLKandAIANandNHPI']=((df["RACBLK"]=='1') & (df["RACAIAN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isBLKandAIANandSOR']=((df["RACBLK"]=='1') & (df["RACAIAN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ########### BLK + ASN + one    
    df['isBLKandASNandNHPI']=((df["RACBLK"]=='1') & (df["RACASN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isBLKandASNandSOR']=((df["RACBLK"]=='1') & (df["RACASN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ########### BLK + NHPI + one
    df['isBLKandNHPIandSOR']=((df["RACBLK"]=='1') & (df["RACNHPI"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    
    ########### AIAN + ASN + one
    df['isAIANandASNandNHPI']=((df["RACAIAN"]=='1') & (df["RACASN"]=='1') & (df["RACNHPI"]=='1') & (df["RACNUM"]=='3')).astype(int)
    df['isAIANandASNandSOR']=((df["RACAIAN"]=='1') & (df["RACASN"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    ########### AIAN + NHPI + one
    df['isAIANandNHPIandSOR']=((df["RACAIAN"]=='1') & (df["RACNHPI"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    
    ########### ASN + NHPI + one
    df['isASNandNHPIandSOR']=((df["RACASN"]=='1') & (df["RACNHPI"]=='1') & (df["RACSOR"]=='1') & (df["RACNUM"]=='3')).astype(int)
    logging.info('3 race done')    
    #4 races
    ########### WHT + BLK + two
    df['isWHTandBLKandAIANandASN']=((df["RACNHPI"]=='0') & (df["RACSOR"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df['isWHTandBLKandAIANandNHPI']=((df["RACASN"]=='0') & (df["RACSOR"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df['isWHTandBLKandAIANandSOR']=((df["RACASN"]=='0') & (df["RACNHPI"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df['isWHTandBLKandASNandNHPI']=((df["RACAIAN"]=='0') & (df["RACSOR"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isWHTandBLKandASNandSOR"]=((df["RACAIAN"]=='0') & (df["RACNHPI"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isWHTandBLKandNHPIandSOR"]=((df["RACAIAN"]=='0') & (df["RACASN"]=='0') & (df["RACNUM"]=="4")).astype(int)
    ########### WHT + AIAN + two
    df["isWHTandAIANandASNandNHPI"]=((df["RACBLK"]=='0') & (df["RACSOR"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isWHTandAIANandASNandSOR"]=((df["RACBLK"]=='0') & (df["RACNHPI"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isWHTandAIANandNHPIandSOR"]=((df["RACBLK"]=='0') & (df["RACASN"]=='0') & (df["RACNUM"]=="4")).astype(int)
    ########### WHT + ASN + two
    df["isWHTandASNandNHPIandSOR"]=((df["RACBLK"]=='0') & (df["RACAIAN"]=='0') & (df["RACNUM"]=="4")).astype(int)
    ########### BLK + AIAN + two
    df["isBLKandAIANandASNandNHPI"]=((df["RACWHT"]=='0') & (df["RACSOR"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isBLKandAIANandASNandSOR"]=((df["RACWHT"]=='0') & (df["RACNHPI"]=='0') & (df["RACNUM"]=="4")).astype(int)
    df["isBLKandAIANandNHPIandSOR"]=((df["RACWHT"]=='0') & (df["RACASN"]=='0') & (df["RACNUM"]=="4")).astype(int)
    ########### BLK + ASN + two
    df["isBLKandASNandNHPIandSOR"]=((df["RACWHT"]=='0') & (df["RACAIAN"]=='0') & (df["RACNUM"]=="4")).astype(int)
    ########### AIAN + ASN + two
    df["isAIANandASNandNHPIandSOR"]=((df["RACWHT"]=='0') & (df["RACBLK"]=='0') & (df["RACNUM"]=="4")).astype(int)
    logging.info('4 race done')
    #5 races
    df['isWHTandBLKandAIANandASNandNHPI']=((df["RACSOR"]=='0') & (df["RACNUM"]=='5')).astype(int)
    df['isWHTandBLKandAIANandASNandSOR']=((df["RACNHPI"]=='0') & (df["RACNUM"]=='5')).astype(int)
    df['isWHTandBLKandAIANandNHPIandSOR']=((df["RACASN"]=='0') & (df["RACNUM"]=='5')).astype(int)
    df["isWHTandBLKandASNandNHPIandSOR"]=((df["RACAIAN"]=='0') & (df["RACNUM"]=='5')).astype(int)
    df["isWHTandAIANandASNandNHPIandSOR"]=((df["RACBLK"]=='0') & (df["RACNUM"]=='5')).astype(int)
    df["isBLKandAIANandASNandNHPIandSOR"]=((df["RACWHT"]=='0') & (df["RACNUM"]=='5')).astype(int)
    logging.info('5 race done')
    #6 races
    df["isWHTandBLKandAIANandASNandNHPIandSOR"]=(df["RACNUM"]=='6').astype(int)
    logging.info('6 race done')
    return df

def main():
    """Configure log"""
    #Change filename with each run (if desired) otherwise info will append to same log.
    logging.basicConfig(filename='recode.log',format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')
    
    """Set file paths"""
    person_rep=sys.argv[1] #This should be path to replicated ACS person files
    filenames_person=glob.glob(os.path.join(person_rep,"*.csv")) #list of all 1556 person_rep files
    
    segmented_filelist=[filenames_person[i:i+50] for i in range(0, len(filenames_person), 50)] #splits into list of lists of 50 files.
    
    
    
    i=0
    gq_pop=0
    housing_pop=0
    for filelist in segmented_filelist:
        logging.info('processing next filelist')
        df=load_files(filelist)
        logging.info('filelist loaded')
        ofile='person_recode/rep_recode_ACSpus%s.csv' %i
        i+=1
        cnt=df.groupby('RELP').size()
        gq_pop += cnt.get('16',0)+cnt.get('17',0)
        housing_pop += cnt.sum()-(cnt.get('16',0)+cnt.get('17',0))
        logging.info('begin recode')
        df=add_recode(df)
        df.to_csv(ofile,index=False)
        
    print gq_pop
    print housing_pop    
    
    return

if __name__ == '__main__':
    main()