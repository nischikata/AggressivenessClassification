from __future__ import division
from sklearn.feature_selection import chi2, f_classif, mutual_info_classif
import numpy as np
import pandas as pd
from scipy import stats
from setupDataset import get_dataset
from feature_vector import get_feature_names


def compute_scores(dataset):
    """
    computes 4 different scores per feature; returns array of scores for given indices
    scores[:, 1] f-test scores
    scores[:, 2] ranksum (wilcoxon test) scores
    scores[:, 3] chi squared
    scores[:, 4] mutual information
    
    scores[:, 0] feature indices corresponding to the scores
    
    NOTE: Mutual information (mi) scores will vary somewhat for each function call!!! 
          this influences the resulting all_combined feature list for getTopFeatures()
    """
    X = dataset["data"]
    y = dataset["target"]
    
    f_test_scores, _ = f_classif(X, y)  # F-test (f)
    mi = mutual_info_classif(X, y)      # mutual information (mi)
    chi_scores, _ = chi2(X, y)          # chi squared (chi)
    
    scores = []
    print len(f_test_scores)
    
    n = 68 # number of available features
    
    for i in range(n):
        
        indices_good = np.where(y == 1)[0]
        indices_bad = np.where(y == 0)[0]
        good = X[:, i][indices_good]
        bad  = X[:, i][indices_bad]
        ranksum, _ = stats.ranksums(good, bad) # wilcoxon test
        
        scores.append([i, abs(f_test_scores[i]), abs(ranksum), abs(chi_scores[i]), abs(mi[i])]) 
    
    """
    scores[x]: test results for feature x
    scores[:, y]: test results for test y
    
    """        
    return np.array(scores)
    
def __save_scores(scores, out):
    
    row_label = get_feature_names()
    col_label = ["index", "f", "ranksum", "chi", "mi"]
    df = pd.DataFrame(scores, index=row_label, columns=col_label)
    df.to_csv(out, sep='\t')
    
    return df
    

def save_scores(dataset, out="scores.csv"):
    """
    :param dataset: data + target
    :param out: filename of target outputfile
    sideffect: saves scores into out file
    :return: dataframe of scores
    """    
    return __save_scores(compute_scores(dataset, out))
    
    
def computeTopFeatures(scores):
    ranks = np.zeros(shape=(len(scores), len(scores[0])+1))
    ranks[:,0] = scores[:,0]

    
    rankrange = np.arange(1, len(scores)+1) # [1,2,3,....67,68]
    sums = np.zeros(len(scores)) # for the summation of ranks per score
    
    for i in range(1,5):
        ranks = ranks[scores[:,i].argsort()[::-1]] #sort descending by column idx i (e.g. fscore)

        temp_ranks = ranks[:,0] # feature indices sorted by best first for current idx i
        sums += rankrange[ranks[:,0].argsort()]
        ranks = ranks[ranks[:,0].argsort()] # bring back into order by sorting by indices
        ranks[:,i] = temp_ranks # remember feature indices sorted by best first for current idx i
        
    ranks[:,-1]  = sums 
    
    ranks = ranks[ranks[:,-1].argsort()] # sort by summations of ranks
    temp_ranks = ranks[:,0]
    ranks = ranks[ranks[:,0].argsort()] # sort again by indices
    ranks[:,-1]  = temp_ranks
    
    # USAGE
    # best30_features_fscore = ranks[:,1][:30]
    # best30_features_ranksum = ranks[:,2][:30]
    # best30_features_chi = ranks[:,3][:30]
    # best30_features_mi = ranks[:,4][:30]
    # best30_features_allscores = ranks[:,-1][:30]
    return ranks 
   

def __save_topFeatures(ranks, out):

    data = ranks[:,1:].astype(int)
    col_label = ["f", "ranksum", "chi", "mi", "all_combined"]

    df = pd.DataFrame(data, columns=col_label)
    df.to_csv(out, sep='\t')
    print df
    return df
    

def getTopFeatures(dataset):
    scores = compute_scores(dataset)
    return computeTopFeatures(scores)