from Utils.univariate_featureSelection import featureSelectionResults, get_selectedFeatures
from Utils.lasso_selections import get_LassoSelectionResults
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# computes
def get_stepwise_results(dev, val, rankfile, rfe_file):
    dfs = []
    for i in range(1, 69):
        results = featureSelectionResults(dev, val, rankfile, rfe_file, i)
        df = results.data_frame()
        dfs.append(df)
    return dfs


def plot_score(dfs, scorename='f1', start=0, end=69, title="my dataset"):
    #noselection, RFE, combined, ftest, ranksum, chi, mi = get_stepwise_scores(dfs, scorename='f1')
    #plot_stepwise_scores(noselection, RFE, combined, ftest, ranksum, chi, mi, start=start, end=end, title=title, scorename=scorename)
    noselection, RFE, combined, ftest, ranksum, mi = get_stepwise_scores(dfs, scorename='f1')
    plot_stepwise_scores(noselection, RFE, combined, ftest, ranksum, mi, start=start, end=end, title=title, scorename=scorename)

def get_LR_featureSelectionResults(trainSet, validationSet, rankfile, rfe_file, lasso_file, out="Datasets/MODEL_LR_results.csv"):
    # 1. scale the sets first thing!
    scaler = preprocessing.MinMaxScaler().fit(trainSet['data'])
    X_train = scaler.transform(trainSet['data'])
    X_test = scaler.transform(validationSet['data'])
    
    y_train = trainSet['target']
    y_test = validationSet['target']
    
    trainSet = {'data': X_train, 'target': y_train}
    validationSet = {'data': X_test, 'target': y_test}
    dfs = get_stepwise_results(trainSet, validationSet, rankfile, rfe_file)
    lasso_df = get_LassoSelectionResults(trainSet, validationSet, lasso_file)
    return combine_logReg_featureSelectionResults(dfs, lasso_df, out)


def get_stepwise_scores(dfs, scorename='f1'):
    """
    this is mainly useful for plotting
    """
    noselection = []
    RFE = []
    combined= []
    mi = []
    ranksum = []
    ftest = []

    for df in dfs:
        noselection.append(df[scorename]['no selection'])
        RFE.append(df[scorename]['RFE'])
        combined.append(df[scorename]['combined'])
        ftest.append(df[scorename]['f-test'])
        ranksum.append(df[scorename]['ranksum'])
        mi.append(df[scorename]['mi'])
    
    return noselection, RFE, combined, ftest, ranksum, mi
 

def combine_logReg_featureSelectionResults(univariate_dfs, lasso_df, out):
    """
    This very important function ranks the different selections by their f1 score. Awesome!
    """
    source_label = ["no selection", "f-test", "ranksum", "mi", "combined", "RFE"]
    df0 = univariate_dfs[0]
    df0['source'] = source_label
    results = [df0]
    
    for df in univariate_dfs[1:]:
        df['source'] = source_label
        results.append(df[1:]) # do not add 'no selection' here (repeatedly)
        
    results.append(lasso_df)

    appended_results = pd.concat(results, axis=0)
    appended_results = appended_results.sort_values('f1', ascending=False)
    appended_results.index = range(len(appended_results))

    # save results in cvs
    appended_results.to_csv(out, sep='\t')
    
    return appended_results
