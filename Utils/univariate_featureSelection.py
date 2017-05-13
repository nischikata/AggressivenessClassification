from Utils.setupDataset import get_dataset, combine_datasets
from Utils.split_dataset import separateByCategory, get_testSet_validationSet, getTestSets
from Utils.feature_ranking import getTopFeatures, getRFE_ranking
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn import metrics as skmetrics
from Utils.selection_metrics import SelectionMetrics



"""
USAGE: see feature_selection_results.ipynb
"""

def get_selectedFeatures(X, indices = []):
    """
    Returns the feature vector for the given Comment
    :param X: the data part of the dataset (array of feature vectors)
    :param indices: a list of the (feature column) indices to select
    :return: numpy array of selected features
    """
    # select column indices
    return X[:, indices]

def concat_datasetList(setlist):
    
    #import pdb; pdb.set_trace()
    data = setlist[0]["data"]
    target = setlist[0]["target"]
    
    for s in setlist[1:]:
        data = np.concatenate([data, s["data"]])
        target = np.concatenate([target, s["target"]])
    
    return data, target

def get_train_test_set(setlist, index):
    X_train, y_train = concat_datasetList(setlist[:index]+setlist[index+1:])
    X_test = setlist[index]["data"]
    y_test = setlist[index]["target"]
    
    return X_train, y_train, X_test, y_test

def get_metrics(X_train, y_train, X_test, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)   

    confusion = skmetrics.confusion_matrix(y_test, y_pred)
    TP = confusion[1,1]
    TN = confusion[0,0]
    FP = confusion[0,1]
    FN = confusion[1,0]
    accuracy = skmetrics.accuracy_score(y_test, y_pred)
    recall = skmetrics.recall_score(y_test,y_pred)

    precision = skmetrics.precision_score(y_test, y_pred)
    f1 = 2*precision*recall/(precision+recall)
    metrics = np.array([ f1, precision, recall, accuracy, TN, FP, FN, TP])
    return metrics


def metrics_feature_selection(ranks, X_train, y_train, X_test, y_test, n):
    # 1. get feature ranks in an array
    # loop over array of ranks (COLUMNS!)
    metrics_noSelection = get_metrics(X_train, y_train, X_test, y_test)
    metrics = [metrics_noSelection]
    
    
    for rank in ranks.T:  # iterate over transposed array (over the columns)
        
        X_train_selection = get_selectedFeatures(X_train, rank[:n]) #apply feature selection according to current ranking
        
        
        
        X_test_selection = get_selectedFeatures(X_test, rank[:n]) #apply feature selection

    
        metrics_temp = get_metrics(X_train_selection, y_train, X_test_selection, y_test)
        metrics.append(metrics_temp)
  
    # returns a list of metrics for each feature selection list for the given train test chunk
    return metrics


def addRFE(dataset, n, ranks):
    """
    will add RFE selected features to ranks array
    NOTE: the RFE features are not sorted by importance/rank, index is sorted in ascending order
    """
    estimator = LogisticRegression()
    selector = RFE(estimator, n, step=1)
    selector = selector.fit(dataset["data"], dataset["target"])
    selection = selector.get_support(indices=True)
    
    # numpy array shape must match, therefore 'empty' cells will contain value -1
    new_col = np.negative(np.ones(len(ranks))) # array len 68, cells initialized with value -1
    new_col[:n] = selection

    # add the new column to the ranks
    ranks = np.c_[ranks, new_col] #
    
    return ranks.astype(int)

    
    

def featureSelectionResults(dataset, rankfile='rank_selections.cvs', RFE_rankfile='RFE_ranks.csv', n=25, k=5):
    # 1. get the feature rankings
    # 1.1 univariate ranks from file
    ranks = getTopFeatures(dataset, rankfile)
    
    # 1.2 compute RFE ranks
    RFE_ranks = getRFE_ranking(dataset, RFE_rankfile)
    ranks = np.concatenate((ranks, RFE_ranks), axis=1)
    
    # 2. separate into test validation sets    
    good, bad = separateByCategory(dataset)
    # good, bad, validate = get_testSet_validationSet(good, bad) brauch kein validation set momentan, oder?
    sets = getTestSets(good, bad, k) #  returns a list of k datasets (each  { "data": data, "target": target})
    r_len = len(ranks.T) + 1 # +1 for result without feature selection
    metrics = [np.zeros(8) for i in range(r_len)]
    
    for index, set in enumerate(sets):
        #actually each set is once the testing set, and then the others are used for training
        # 1. the index set is the testing set, 
        X_train, y_train, X_test, y_test = get_train_test_set(sets, index)

        
        metrics_temp = metrics_feature_selection(ranks, X_train, y_train, X_test, y_test, n)
        metrics = [metrics[i]+metrics_temp[i] for i in range(r_len)] #sum up the metrics (compute avg later)

    
    # now divide all values of the metrics (except TN, TP, FN, FP) by the number of sets
    set_len = len(sets)
    avg_mask = np.array([set_len, set_len, set_len, set_len, 1, 1, 1, 1])
    metrics = [m/avg_mask for m in metrics] #divide by the number of sets to get the average metrics
    
    return SelectionMetrics(metrics, ranks, n)
