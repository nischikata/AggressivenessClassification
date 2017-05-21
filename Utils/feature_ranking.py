from __future__ import division
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE, chi2, f_classif, mutual_info_classif
from sklearn import preprocessing
import numpy as np
import pandas as pd
from scipy import stats
from Utils.setupDataset import get_dataset
from Utils.feature_vector import get_feature_names
import os.path



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
    
    n = len(f_test_scores) # number of available features
    
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
    scores =  np.array(scores)
    scores[np.isnan(scores)] = 0    # replace 'nan' values (e.g. appears for  m-dash feature) with 0 
    return scores
    
def __save_scores(scores, out):
    
    row_label = get_feature_names()
    col_label = ["index", "f", "ranksum", "chi", "mi"]
    df = pd.DataFrame(scores, index=row_label, columns=col_label)
    df.to_csv(out, sep='\t')
    
    return df


    
def save_rankSelections(ranks, out='rank_selections.csv'):
    col_label = ["f", "ranksum", "chi", "mi", "combined"]
    df = pd.DataFrame(ranks, columns=col_label)
    df.to_csv(out, sep='\t')
    return df
    
def load_rankSelections(filename='rank_selections.cvs'):
    df = pd.read_csv(filename, sep='\t')
    ranks = df.values
    return ranks[:,1:].astype(int)


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
    # best30_features_fscore = ranks[:,0][:30]
    # best30_features_ranksum = ranks[:,1][:30]
    # best30_features_chi = ranks[:,2][:30]
    # best30_features_mi = ranks[:,3][:30]
    # best30_features_allscores = ranks[:,-1][:30]
    return ranks[:,1:].astype(int)
   

def __save_topFeatures(ranks, out):
    col_label = ["f", "ranksum", "chi", "mi", "all_combined"]

    df = pd.DataFrame(ranks, columns=col_label)
    df.to_csv(out, sep='\t')
    print df
    return df
    

def getTopFeatures(dataset, filename='rank_selections.cvs'):
    
    if not os.path.exists(filename):  
        scores = compute_scores(dataset)
        
        rankSelections = computeTopFeatures(scores)
        save_rankSelections(rankSelections, filename)
        return rankSelections
    else:
        return load_rankSelections(filename)
        
        
#----- Recursive Feature Elimination (RFE)
def getRFE_ranking(dataset, out='SELECTIONS_RFE.csv', scale=True):
    
    if not os.path.exists(out):
        X = dataset["data"]
        y = dataset["target"]
        
        if scale:
            X = preprocessing.minmax_scale(X) # scale the dataset to speed up process and likely better feature ranking
    
        n = len(get_feature_names())+1
    
        first = getRFE_selection(X, y, 1)
        RFE_ranks = [first[0]]
   
        for i in range(2, n):
            sel = getRFE_selection(X,y,i)
            diff = list(set(RFE_ranks).symmetric_difference(sel))
        
            for d in diff:
                if d not in RFE_ranks:  # apparently the ranking is not always identical, prevents an index from being added twice     
                    RFE_ranks.append(d)
        

        RFE_ranks = np.array(RFE_ranks)
        save_RFE_ranks(RFE_ranks, out)
    
    
    return load_rankSelections(out)


def save_RFE_ranks(ranks, out):
    col_label = ["RFE"]
    df = pd.DataFrame(ranks, columns=col_label)
    df.to_csv(out, sep='\t')
    # Note: use load_rankSelections to load
    # combine np.concatenate((ranks, RFE_ranks), axis=1)
    

def getRFE_selection(X, y, n):
    estimator = LogisticRegression()
    selector = RFE(estimator, n, step=1)
    selector = selector.fit(X, y)
    selection = selector.get_support(indices=True)
    return selection.tolist()