from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV
import numpy as np
from Utils.setupDataset import get_dataset, save, load
from univariate_featureSelection import get_metrics, get_selectedFeatures
import pandas as pd


def get_LassoSelections(dataset, out='SELECTIONS_lasso.pickle', step=0.005, maxThresh=0.25, minThresh=0.000005):
    X = dataset["data"]
    y = dataset["target"]
    
    thr_range =  np.arange(0.000005, 0.25, 0.005)
    no_selection = np.arange(0,68)
    
    selections = [no_selection]
    
    for thresh in thr_range:
        
        clf = LassoCV(selection='random', random_state=1, cv=5)
        sfm = SelectFromModel(clf, threshold=thresh)
        sfm.fit(X,y)
        sel = sfm.get_support(indices=True)
        n_features = sfm.transform(X).shape[1]
        
        if len(sel) > 0 and len(sel) != len(selections[-1]):
            selections.append(sel)
    
    selections.reverse()
    save(selections, out)
    return selections


def get_LassoSelectionResults(trainSet, validationSet, file='Datasets/SELECTIONS_lasso.pickle'):
    # 1. load the selections
    selections = load(file) # returns a list of numpy-integer arrays -> should be ok
    # TODO check if file exists, if not, create file
    
    
    X_train = trainSet['data']
    y_train = trainSet['target']
    X_test = validationSet['data']
    y_test = validationSet['target']
       
    metrics = metrics_lasso_selection(selections, X_train, y_train, X_test, y_test)
    
    
    
    return metrics #SelectionMetrics(metrics, ranks, n) 


def metrics_lasso_selection(selections, X_train, y_train, X_test, y_test):
    # 1. get feature ranks in an array
    # loop over array of ranks (COLUMNS!)
    metrics_noSelection = get_metrics(X_train, y_train, X_test, y_test, penalty='l2')
    metrics = [metrics_noSelection]
    source_labels = ['no selection (L2)']
    selections_col = [selections[-1]]
    ns = [len(selections[-1])]
    
    
    for sel in selections[:-1]:  # exclude the noSelections
        
        X_train_selection = get_selectedFeatures(X_train, sel) #apply feature selection according to current ranking
        X_test_selection = get_selectedFeatures(X_test, sel) #apply feature selection

        metrics_temp = get_metrics(X_train_selection, y_train, X_test_selection, y_test, penalty='l2')
        metrics.append(metrics_temp)
        
        source_labels.append("Lasso") # 
        selections_col.append(sel) # add the number of selected features, and the selection list
        ns.append(len(sel))
  
    # returns a list of metrics for each feature selection list for the given train test chunk
    
    # now put the metrics into a DF
    col_label = ["f1", "precision", "recall", "accuracy", "TN", "FP", "FN", "TP"]
    row_label = selections_col
    df = pd.DataFrame(metrics, columns=col_label)

    df['TN'] = df['TN'].astype(int)
    df['FP'] = df['FP'].astype(int)
    df['FN'] = df['FN'].astype(int)
    df['TP'] = df['TP'].astype(int)

    

    df_ranks = pd.DataFrame({'n': ns, 'selection': selections_col, 'source': source_labels})

    df = df.join(df_ranks, how='right')
    return df

"""
    # USAGE
from Utils.setupDataset import get_dataset, save, load

m_devSet = get_dataset("Datasets/M_DEV_dataset.pickle")
w_devSet = get_dataset("Datasets/W_DEV_dataset.pickle")

get_LassoSelections(m_devSet, out='Datasets/M_SELECTIONS_lasso.pickle')
get_LassoSelections(w_devSet, out='Datasets/W_SELECTIONS_lasso.pickle')

m_lasso_selections = load('Datasets/M_SELECTIONS_lasso.pickle')
w_lasso_selections = load('Datasets/W_SELECTIONS_lasso.pickle')

print m_lasso_selections, "\n\n"
print w_lasso_selections
"""