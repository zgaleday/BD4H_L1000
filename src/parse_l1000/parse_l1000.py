### Must be run with an enviroment created following: http://cmappy.readthedocs.io/en/latest/build.html
### Instructions for parsing gtx file can be found at:
### https://github.com/cmap/cmapPy/blob/master/tutorials/cmapPy_pandasGEXpress_tutorial.ipynb

import pandas as pd
import numpy as np
from os.path import join
## cmap package to pull in their filetype
from cmapPy.pandasGEXpress import parse
from cmapPy.pandasGEXpress import write_gctx as write_gctx

### Filepath for data
FILE_PATH = "/home/zachary/git_repo/BD4H_L1000/data/"

def reduce_and_save():
    """
    Reads in the level 5 data and outputs a file with only the landmark gene z-scores(rows and the small molecule
     perterbagens (cols)
    """
    ### Get the signature information
    sig_info = pd.read_csv(join(FILE_PATH, "GSE92742_Broad_LINCS_sig_info.txt"), sep="\t")
    ### Columns are:
    ###  Index([u'sig_id', u'pert_id', u'pert_iname', u'pert_type', u'cell_id',
    ###       u'pert_dose', u'pert_dose_unit', u'pert_idose', u'pert_time',
    ###       u'pert_time_unit', u'pert_itime', u'distil_id'],
    ###      dtype='object')

    ### Filter for signature ids for small molecule pertubagens
    small_mol_sigs = sig_info['sig_id'][sig_info['pert_type'] == "trt_cp"]
    ### Results in 205034 signatures

    ### Read in the gene info
    gene_info = pd.read_csv(join(FILE_PATH, "GSE92742_Broad_LINCS_gene_info.txt"), sep='\t')
    ### Index([u'pr_gene_id', u'pr_gene_symbol', u'pr_gene_title', u'pr_is_lm',
    ###      u'pr_is_bing'],
    ###      dtype='object')

    landmark_gene_ids = gene_info['pr_gene_id'][gene_info['pr_is_lm'] == 1] #Filters for directly measured transcripts
    ### Results in the 978 landmark pr_gene_ids

    ### LOAD in the main file filtering the columns so that only the small molecules signatures are loaded and the
    ### rows such that only the landmark genes are loaded into their custom gctoo container type
    relevent_sigs_gctoo = parse(join(FILE_PATH, "GSE92742_Broad_LINCS_Level5_COMPZ.MODZ_n473647x12328.gctx"),
                                cid=small_mol_sigs, rid=landmark_gene_ids)
    # print small_mol_sigs.data_df.shape
    ### Should write an intermediate file with dimensions (978, 205034)
    write_gctx.write(relevent_sigs_gctoo, join(FILE_PATH, "lm_sm_aggz"))

def read_reduced():
    """
    Reads in the reduced file outputs a data_frame with the maximal magnitude signature for each pert_id
    :return reduce l1000 feature dataframe (as pandas dataframe)
    """
    ### read in the reduced data
    reduced_data = parse(join(FILE_PATH, "lm_sm_aggz.gctx"))

    ### read in the signature info and set the index to the signature id for easy indexing in the next step
    sig_info = pd.read_csv(join(FILE_PATH, "GSE92742_Broad_LINCS_sig_info.txt"), sep="\t")
    sig_info.index = sig_info['sig_id']

    ### map the columns to the pert_id that generated the signature to allow for comparison in spark
    reduced_data.data_df.columns = sig_info.loc[pd.Index(reduced_data.data_df.columns)]['pert_id']
    ### return data_frame with pert_ids in row_major form ready for scala
    return reduced_data.data_df.transpose()

def max_mag_sig(df, thresh=3.0):
    """
    Read in the the data frame as output from read reduces, thresholds based on the z-score and computes the magnitude
    of the signature as a linear combination of the L1000 transcripts.
    :param df: input data frame with l1000, sigs
    :param thresh: the absolute value of the z-score to serve as a threshold value
    :return: filtered df
    """
    ### Filter features below the threshold (set to zero)
    df[abs(df) < thresh] = 0
    ### magnitude of the absolute values of the feature vectors
    df['magnitude'] = df.abs().sum(axis=1)
    df['max_group'] = df.groupby(df.index, sort=False)['magnitude'].transform(max)
    ### select only signatures with maximal magnitude
    df = df[df['magnitude'] == df['max_group']]
    ### clean up after myself
    df.drop(df.columns[-2:], axis=1, inplace=True)
    df.columns = np.arange(1, df.shape[1]+1)
    return df

def pert_stats(df, verbose=False):
    """
    Takes the features dataframe as argument and counts the number of nonzero-features
    :param df: features data frame
    :param verbose: toggle to pretty print stats
    :return: avg, median, min, max number of non-zero features
    """
    df[df != 0] = 1
    df['num_features'] = df.sum(axis=1)
    df_mean, df_med, df_min, df_max =\
        df['num_features'].mean(), df['num_features'].median(), df['num_features'].min(), df['num_features'].max()
    if verbose:
        print "##########Pert Statistics#############"
        print "Mean:   ", df_mean
        print "Median: ", df_med
        print "Min:    ", df_min
        print "Max:    ", df_max
        print "######################################"
    return df_mean, df_med, df_min, df_max

def feature_stats(df, verbose=False):
    """
    Takes the features dataframe as argument and counts the number of non-zero perts per feature
    :param df: features data frame
    :param verbose: toggle to pretty print stats
    :return: avg, median, min, max number of perts with feature != 0
    """
    df[df != 0] = 1
    feat_df = df.sum(axis=0)
    df_mean, df_med, df_min, df_max = \
        feat_df.mean(), feat_df.median(), feat_df.min(), feat_df.max()
    if verbose:
        print "##########Feature Statistics##########"
        print "Mean:   ", df_mean
        print "Median: ", df_med
        print "Min:    ", df_min
        print "Max:    ", df_max
        print "######################################"
    return df_mean, df_med, df_min, df_max


rd = read_reduced()
rd = max_mag_sig(rd)
feature_stats(rd, True)
# rd.to_csv(join(FILE_PATH, "l1000_scala_features.txt"), delimeter='\t')