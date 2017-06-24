from Utils.univariate_featureSelection import get_selectedFeatures
from Utils.feature_ranking import getTopFeatures, getRFE_ranking
from Utils.lasso_selections import get_LassoSelectionResults
from Utils.setupDataset import get_dataset, load
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn import metrics as skmetrics
from sklearn.svm import SVC, LinearSVC
from sklearn import preprocessing
from ast import literal_eval
import pandas as pd
import numpy as np
import warnings
import os.path
import time


warnings.filterwarnings('ignore')

# ____________ FEATURE SELECTION

def featureSelectionResults_SVM(trainSet, validationSet, univariate, RFE, lasso, combination, rfb_kernel=True):

    # 1. scale the sets first thing!
    scaler = preprocessing.MinMaxScaler().fit(trainSet['data'])
    X_train = scaler.transform(trainSet['data'])
    y_train = trainSet['target']
    X_test = scaler.transform(validationSet['data'])
    y_test = validationSet['target']
    
    trainSet = {'data': X_train, 'target': y_train}
    validationSet = {'data': X_test, 'target': y_test}
    
    
    # 1. get the feature rankings
    # 1.1 univariate ranks from file
    if not os.path.exists(combination):
        # pass a copy 
        selections_df = combine_selections(trainSet, univariate, RFE, lasso, rfb_kernel)
        # save results in cvs
        selections_df.to_csv(combination, sep='\t')
    
    selections_df = pd.read_csv(combination, sep='\t', index_col=0)

       
    selections_df = apply_feature_selection_SVM(selections_df, X_train, y_train, X_test, y_test, rfb_kernel)
    selections_df = selections_df.sort_values('n', ascending=True)
    selections_df = selections_df.sort_values('f1', ascending=False)
    
    selections_df = selections_df.reset_index(drop=True)
    selections_df.to_csv(combination, sep='\t')
    return selections_df
    
    
def apply_feature_selection_SVM(selections_df, X_train, y_train, X_test, y_test, rfb_kernel):

    for i in range(0, len(selections_df)):
        # convert the selection list from string to int list
        sel = literal_eval(selections_df['selection'][i])
    
        X_train_selection = get_selectedFeatures(X_train, sel) #apply feature selection according to current ranking
        X_test_selection = get_selectedFeatures(X_test, sel) #apply feature selection
    
        if rfb_kernel:
            metrics = get_metrics_SVM(X_train_selection, y_train, X_test_selection, 
                                      y_test, selections_df['gamma'][i], selections_df['C'][i])
        else:
            metrics = get_metrics_linearSVM(X_train_selection, y_train, X_test_selection, 
                                      y_test, selections_df['C'][i])
    
        selections_df.iloc[i, :len(metrics)] = metrics
   
    return selections_df
    
    
def get_metrics_SVM(X_train, y_train, X_test, y_test, gamma, C):

    g = gamma
    c = C

    # 
    model = SVC(kernel='rbf', C=c, gamma=g, tol=1e-10, random_state=0)
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
    
    
def combine_selections(trainSet, univariate, RFE, lasso, rfb_kernel):

    col_labels = ["f1", "precision", "recall", "accuracy", "TN", "FP", "FN", "TP", "n", "selection", "source", "gamma", "C"]

    uni_selections = getTopFeatures(trainSet, univariate)
    RFE_selections = getRFE_ranking(trainSet, RFE)
   
    selections = np.concatenate((uni_selections, RFE_selections), axis=1)

    print "starting with 'no selection' at ", time.ctime()

    if rfb_kernel:
        gamma, C = compute_SVM_params(trainSet, range(0,68))
        combination = [[0.0, 0.0, 0.0, 0.0, 0,0,0,0, 68, range(0,68), 'no selection', gamma, C]]
    else:
        C = compute_linearSVM_params(trainSet, range(0,68))
        combination = [[0.0, 0.0, 0.0, 0.0, 0,0,0,0, 68, range(0,68), 'no selection', 0.0, C]]


    source = ["f-test", "ranksum", "mi", "combined", "RFE"]

    
    for i, sel in enumerate(selections.T):
        print "starting selection '", source[i], "' at ", time.ctime()        
        for n in range(1, 68):
            if rfb_kernel:
                gamma, C = compute_SVM_params(trainSet, sel[:n])
                combination.append([0.0, 0.0, 0.0, 0.0, 0,0,0,0, n, sel[:n], source[i], gamma, C])
            else:
                C = compute_linearSVM_params(trainSet, sel[:n])
                combination.append([0.0, 0.0, 0.0, 0.0, 0,0,0,0, n, sel[:n], source[i], 0.0, C])
            
    lasso_selections = load(lasso)

    print "almost there... starting with the Lasso now... ", time.ctime()
    for sel in lasso_selections[:-1]:  # exclude the noSelections
        if rfb_kernel:
            gamma, C = compute_SVM_params(trainSet, sel)
            combination.append([0.0, 0.0, 0.0, 0.0, 0,0,0,0, len(sel), sel, 'Lasso', gamma, C])
        else: 
            C = compute_linearSVM_params(trainSet, sel)
            combination.append([0.0, 0.0, 0.0, 0.0, 0,0,0,0, len(sel), sel, 'Lasso', 0.0, C])
    print "done. saving to file... ", time.ctime()
    df = pd.DataFrame(combination, columns = col_labels)
    
    # make sure all the selections are lists (instead of numpy arrays!!)
    df['selection'] = df['selection'].apply(lambda x: x.tolist() if type(x).__module__ == np.__name__ else x)
    return df


def compute_SVM_params(trainSet, selection): 
    gamma_range = np.logspace(-2,3,6)
    C_range = np.logspace(-2,3,6)


    X_train = get_selectedFeatures(trainSet["data"], selection)
    y = trainSet["target"]

    tuning_params = [{'kernel': ['rbf'], 'gamma': gamma_range, 'C':  C_range}]
    f1 = make_scorer(f1_score)

    clf = GridSearchCV(SVC(C=1), tuning_params, cv=5, scoring=f1, n_jobs=4)
    clf.fit(X_train, y)

    # parameters for best training result
    C = clf.best_params_['C']
    gamma =  clf.best_params_['gamma']
    return gamma, C
    
    
#__________ LINEAR SVC specific ____________

def compute_linearSVM_params(trainSet, selection): 
    tuning_linear = [ {'loss': ['hinge'], 'C': [1.0, 20, 100, 200, 1000, 2000]},]

    X_train = get_selectedFeatures(trainSet["data"], selection)
    y = trainSet["target"]

    f1 = make_scorer(f1_score)

    clf = GridSearchCV(LinearSVC(), tuning_linear, cv=5, scoring=f1)
    clf.fit(X_train, y)

    # parameters for best training result
    C = clf.best_params_['C']
    return C
    
    
def get_metrics_linearSVM(X_train, y_train, X_test, y_test, C):
    # Scale X:
    c_param = C
    # 
    
    """ Random State & Tolerance https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/svm/classes.py#L89 :
    The underlying C implementation uses a random number generator to
        select features when fitting the model. It is thus not uncommon
        to have slightly different results for the same input data. If
        that happens, try with a smaller ``tol`` parameter.
    """
    model = LinearSVC(C=c_param, loss='hinge', tol=1e-10, random_state=0)
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