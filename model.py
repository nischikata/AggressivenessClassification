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


def test_model(test_size, random_state):
    dataset = get_dataset()
    model = LogisticRegression()
    X = dataset["data"]

    y = dataset["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    #TODO finish


    # wichtig, zuerst die tatsaechlichen werte, dann die predicted
    confusion = metrics.confusion_matrix(y_test, y_pred)
    TP = confusion[1,1]
    TN = confusion[0,0]
    FP = confusion[0,1]
    FN = confusion[1,0]
    print "\nConfusion matrix"
    print(confusion)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    print "\n\nAccuracy: ", accuracy

    recall = metrics.recall_score(y_test,y_pred)
    print "\n\nRecall or Sensitivity or True Positive Rate: ", recall # want to maximize, best possible value = 1.0

    # when the actual value is negative, how often is the prediction correct? want to maximize, best possible value = 1.0
    print "\n\nSpecifity: ", (TN/float(TN+TP))

    print "\n\nFalse Positive Rate: ", (FP/float(TN+TP))

    #how precise the classifier is when prediciton a positive instance
    print "\n\nPrecision: ", (TP/float(TP + FP))
    precision = metrics.precision_score(y_test, y_pred)
    print(precision)
    return [accuracy, precision, recall]


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



# TODO remove again
results = [0,0,0]
n = 25

for i in range(n):
    r = test_model(0.5, n)
    results[0] += r[0]
    results[1] += r[1]
    results[2] += r[2]

print "avg accuracy: ", results[0]/n, " avg precision: ", results[1]/n, " avg recall: ", results[2]/n