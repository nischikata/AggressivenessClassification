from __future__ import division
import numpy as np
import pandas as pd
import pickle
import os.path
from Utils.setupDataset import get_dataset
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from Utils.comment import Comment
from Utils.feature_vector import get_feature_vector
from Utils.tiny_helpers import get_text_label
from Utils.univariate_featureSelection import get_selectedFeatures, single_selection
from sklearn import preprocessing


def save(model, filepath): # TODO: funktion auslagern in Utils
    """
    SAVE TO FILE FOR FASTER ACCESS next time
    :return: side effect only (dumps model into pickle file)
    """

    pickle_out = open(filepath, "wb")
    pickle.dump(model, pickle_out)
    pickle_out.close()


def load(filepath):
    # OPEN FILE and reconstruct dataset
    pickle_in = open(filepath, "rb")
    return pickle.load(pickle_in)


def setUp_model():
    pass


def get_logReg_model(path = "model_logRegr.pickle"):

    if not os.path.exists(path):
        dataset = get_dataset()
        model = LogisticRegression()
        X = dataset["data"]
        y = dataset["target"]

        model.fit(X, y)
        save(model, path)
    else:
        model = load(path)

    return model




def get_prediction(comment, aggressive=False): # TODO: model type as param
    """

    :param comment: str
    :param aggressive: True for aggressive
    :return: int
    """
    label = 'a' if aggressive else 'na'
    # X.reshape(1, -1)
    # 1. compute feature vector for comment
    c = Comment(comment, label)
    observation = get_feature_vector(c)
    model = get_logReg_model()
    pred = model.predict(observation.reshape(1,-1))

    print "\n"
    c.print_original_sents()

    print " EXPECTED:  ", get_text_label(c.get_label()), "    PREDICTED:   ", get_text_label(pred)
    print "------------------------------------------------------------------------------------------\n\n"



def get_bestPrediction(comment, aggressive=False, FS=True, dataset='wiki', selection = []):
    """
    
    """

    if selection == []:
        selection = range(0,68)
        if FS:
            if dataset == 'wiki':
                selection = [60, 56, 40, 24, 51, 61, 7, 1, 62, 13, 36, 12, 32, 33, 4, 46, 20, 18, 6, 23, 19, 26, 43, 11, 0, 35, 59, 64, 10, 57, 37, 58, 31, 41, 14, 2, 54, 48, 22, 44, 50, 49, 53, 30, 34, 8, 27, 39, 29, 55, 67, 66, 28, 9, 5, 52, 15, 47, 65, 17, 3, 42, 16, 63, 25]
                
                # or with best 24 features (f-test):
                # selection = [60, 4, 61, 24, 0, 62, 33, 7, 6, 32, 53, 23, 44, 49, 64, 54, 31, 35, 67, 59, 1, 26, 29, 66]
                
                # or with best 6 features (Lasso)
                #selection = [7, 24, 60, 61, 62, 64] 	
                
            else:
                selection = [1, 43, 10, 11, 40, 26, 59, 35, 56, 24, 60, 62, 0, 61, 18, 2, 12, 54, 63, 19, 42, 34, 46, 20, 23, 53, 58, 4, 49, 47, 52, 8, 3, 38, 45, 55, 9, 16, 32, 7, 66, 36, 33, 13, 17, 48, 50, 44]
                # or with best 21 features
                #selection = [1, 43, 10, 11, 40, 26, 59, 35, 56, 24, 60, 62, 0, 61, 18, 2, 12, 54, 63, 19, 42]
                
                # best 'manual selection by Tina' (83 % f1 score!!):
                # selection = [1, 5, 7, 17, 24, 34, 40, 46, 59]
        
    label = 'a' if aggressive else 'na'
  
    
    c = Comment(comment, label)
    observation = (get_feature_vector(c)) #[selection] # remove!
    
    # get both datasets
    w_dataset = get_dataset("Datasets/W_DEV_dataset.pickle")
    m_dataset = get_dataset("Datasets/M_DEV_dataset.pickle")
        
    # get predictions for both
    w_pred = _pred(w_dataset, observation, selection)
    m_pred = _pred(m_dataset, observation, selection)

    print "\n"
    c.print_original_sents()

    print "     You EXPECTED:  ", get_text_label(c.get_label())
    print "   Wiki PREDICTED:  ", get_text_label(w_pred), "\n Martin PREDICTED:  ", get_text_label(m_pred)
    print "------------------------------------------------------------------------------------------\n\n"    
    


def _pred(dataset, observation, selection):
    
    X_train = get_selectedFeatures(dataset["data"], selection)
    y = dataset["target"]
    
    observation = observation[selection]
    #DATA SCALING!
    scaler = preprocessing.MinMaxScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    observation = scaler.transform([np.array(observation)])
    
    model = LogisticRegression(penalty='l1', random_state=5)
    model.fit(X_train, y)

    pred = model.predict(observation)
    return pred
    
    
def DIY_selection(selection=[0,1,2,3]):
    
    selection = [sel for sel in selection if sel >= 0 and sel < 68]
    
    w_dev = get_dataset("Datasets/W_DEV_dataset.pickle")
    w_val = get_dataset("Datasets/W_VAL_dataset.pickle")

    m_dev = get_dataset("Datasets/M_DEV_dataset.pickle")
    m_val = get_dataset("Datasets/M_VAL_dataset.pickle")
    
    w_r = single_selection(w_dev, w_val, selection)
    m_r = single_selection(m_dev, m_val, selection)
    col_label = ["f1", "precision", "recall", "accuracy", "TN", "FP", "FN", "TP"]
    
    df = pd.DataFrame([w_r, m_r], columns=col_label, index=['wiki', 'martin'])
    df['TN'] = df['TN'].astype(int)
    df['FP'] = df['FP'].astype(int)
    df['FN'] = df['FN'].astype(int)
    df['TP'] = df['TP'].astype(int)
    return df
