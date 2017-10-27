### Reads in the L1000 pert_info file and uses the pubchempy package to find the cids for each using the smiles string

from pubchempy import *
import pandas as pd
import numpy as np

def cid_from_canonical_smiles(smiles):
    """
    Takes the canonical
    :param smiles: the canonical smiles string
    :return: returns the CID associates with the smiles string in the pubchem database (format 'CIDxxxx')
    """
    cid = 'CID' + str(get_compounds(smiles, 'smiles')[0].cid)
    print cid
    return cid


def read_cmpnds():
    """
    reads in the pert id data as a pandas df object with only compound perts
    :return: df
    """
    file_path = "../../data/GSE92742_Broad_LINCS_pert_info.txt"
    cmpd_df = pd.read_csv(file_path, sep='\t')
    cmpd_df = cmpd_df[cmpd_df['pert_type'] == "trt_cp"]
    cmpd_df = cmpd_df[['pert_id', 'canonical_smiles']]
    cmpd_df = cmpd_df[(cmpd_df['canonical_smiles'] != '-666') & (cmpd_df['canonical_smiles'] != 'restricted')]
    vector_lookup = np.vectorize(cid_from_canonical_smiles)
    cmpd_df['CID'] = vector_lookup(cmpd_df['canonical_smiles'])
    print cmpd_df
    return cmpd_df


df = read_cmpnds()
df.to_csv("../../data/perts_with_cid.txt", delimeter='\t')