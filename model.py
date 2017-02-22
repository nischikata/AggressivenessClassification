import numpy as np
import pickle
import os.path
from setupDataset import get_dataset
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from comment import Comment
from feature_vector import get_feature_vector
from Utils.tiny_helpers import get_text_label


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


def get_logReg_model():
    path = "model_logRegr.pickle"

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


def get_SVM_model():
    path = "model_SVM.pickle"
    #TODO
    pass


def test_model():
    dataset = get_dataset()
    model = LogisticRegression()
    X = dataset["data"]

    y = dataset["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=4)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # wichtig, zuerst die tatsaechlichen werte, dann die predicted
    confusion = metrics.confusion_matrix(y_test, y_pred)
    TP = confusion[1,1]
    TN = confusion[0,0]
    FP = confusion[0,1]
    FN = confusion[1,0]
    print "\nConfusion matrix"
    print(confusion)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    recall = metrics.recall_score(y_test,y_pred)
    #how precise the classifier is when prediciton a positive instance
    precision = metrics.precision_score(y_test, y_pred)

    return { "accuracy": accuracy, "precision": precision, "recall": recall}


def get_prediction(comment, aggressive=False): # TODO: model type as param
    """

    :param comment: str
    :param aggressive: True for aggressive
    :return: int
    """
    # TODO !!!!!!!!!!!!!!!!!
    print  "TODO: rebuild DATASET ! (out of date!)"


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
    