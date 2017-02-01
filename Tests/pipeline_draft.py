import numpy as np
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import word_tokenize
from nltk import TreebankWordTokenizer
import Features.Other.counters as cnt
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics




    

def get_observation(raw_comment):
    observation = np.zeros(10)
        # Get data in different forms
    #raw_comment = corpus.raw(fileid)
    sents = cnt.get_sents(raw_comment)
    word_count = cnt.get_wordcounts(raw_comment)

    observation[0] = len(sents)     # Number of sentences
    observation[1] = word_count["noise_count"]
    observation[2] = word_count["one_char_token_count"]
    observation[3] = word_count["average_wordlength"]
    observation[4] = word_count["median_wordlength"]
    observation[5] = word_count["max_wordlength"]
    observation[6] = word_count["word_count"]
    observation[7] = word_count["long_words_count"]
    observation[8] = word_count["mixed_case_word_count"]
    observation[9] = word_count["ttr"]

    return observation

def get_label(fileid):
        return 1 if fileid[0] is 'a' else 0 # 1 ... aggressive, 0 ... not aggressive (checking the filename to decide category)



#TODO: start end default params!
sentinel = object()
def get_model(corpus, start=0, end=sentinel):  #TODO: use default params
    if end is sentinel:
        end = len(corpus.fileids())
    
    print("WIE VIELE?")
    print(end)

    observations = []
    target = []

    for fileid in corpus.fileids()[start:end]:
        observation = get_observation(corpus.raw(fileid))
        label = get_label(fileid)

        observations.append(observation)
        target.append(label)
        #TODO: save fileid, perhaps in observations array or in a separate array so I can check fileids that are outliers etc
        #print(fileid)
        #print(observation)
        #print(label)
        #print("\n\n--------------------")

        # turn lists into numpy arrays
    observations = np.array(observations)
    target = np.array(target)
    return {"data": observations, "target": target}

# vom terminal
corpus = CategorizedPlaintextCorpusReader('Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')
#pycharm:
#corpus = CategorizedPlaintextCorpusReader('../Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')
"""
# checken wieviel files es ueberhaupt gibt:
fileids = corpus.fileids(categories="aggressive")
print len(fileids)
print "soviele files gibt es aggr"
fileids = corpus.fileids(categories="not_aggressive")
print len(fileids)
print "soviele files gibt es not aggr"
"""


#modl = get_model(corpus, 30, 120)
modl = get_model(corpus)

# define X and y
feature_cols = ['sentence count', 'noise count abs', 'noise count / sent', 'noise count / word']
# panda = panda.read_csv(url, header=None, names=feature_cols) mit panda.head() wird dann eine tabelle mit den ersten 5 reihen ausgegeben
# TODO: check wie das ohne panda gehen koennte bzw... hmm vielleicht sollte ich mir mein panda selber erstellen, also die berechneten features als panda speichern... in am csv

log = LogisticRegression()
X = modl["data"]
y = modl["target"]

log.fit(X, y)

#######################TODO write nice method for this mit ausgabe Aggressive / nicht aggressive
# HERE TODO: manueller test:
manual_test = get_observation("$hit!")
manual_observation = np.zeros(1)
#manual_observation[0] = manual_test
man_pred = log.predict(manual_test)
print("----------------------- PREDICITION for input:")
print(man_pred)

testmodl = get_model(corpus, 1, 5)

prediction = log.predict(testmodl["data"])

print("This is the prediction")
print(prediction)
print("This is the actual label")
print(testmodl["target"])

##############################################################


# Test Training accuracy (TODO: improve it by using precision, recall, f-score)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

#first step: split the Dataset into 2 pieces (commonly 20-40% of the set is used for testing)
# i guess by controlling the random state you do k-fold cross-validation TODO: check how to best do k-fold cross validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=4)

log.fit(X_train, y_train)
y_pred = log.predict(X_test)

print("This is the accuracy")
print metrics.accuracy_score(y_test, y_pred)

# geht nur wenn y_test ein panda series object ist
#print(y_test.value_counts())

#calculate the percentage of ones
ones = y_test.mean()


#calculate the percentage of zeros
zeros = 1 - ones

#calculate null accuracy for binar classification problems
null_accuracy = max(zeros, ones)
print("\nNull accuracy:")
print(null_accuracy)


# confusion matrix.....get the idea:
print "\n\n"
print "true: ", y_test[0:20]
print "pred: ", y_pred[0:20]

# wichtig, zuerst die tatsaechlichen werte, dann die predicted
confusion = metrics.confusion_matrix(y_test, y_pred)
TP = confusion[1,1]
TN = confusion[0,0]
FP = confusion[0,1]
FN = confusion[1,0]
print "\nConfusion matrix"
print(confusion)


print "\n\nRecall or Sensitivity or True Positive Rate" # want to maximize, best possible value = 1.0
print(TP/ float(TP +FN)) # recall by hand
recall = metrics.recall_score(y_test,y_pred)
print(recall)


# when the actual value is negative, how often is the prediction correct? want to maximize, best possible value = 1.0
print "\n\nSpecifity"
print(TN/float(TN+TP))

print "\n\nFalse Positive Rate"
print(FP/float(TN+TP))


print "\n\nPrecision" #how precise the classifier is when prediciton a positive instance
print(TP/float(TP + FP))
precision = metrics.precision_score(y_test, y_pred)
print(precision)

# others to calculate f1 score or Matthews correlation coefficient


# WHAT metric matters most to me???
# false negatives (in which aggressive comments are marked as ok) are probably
# more acceptable than false positives in which non aggressive comments are marked as aggressive and blocked
print "\n\n"

# Adjusting the classification Threshold


# COOOOOOL stuff!
print(log.predict(X_test)[0:10])
print(log.predict_proba(X_test)[0:10])
# each row represents one observation and each column represents a class, left column is 0, right column is 1
# it shows us the predicted probability that each observation belongs to a certain class
# where do these numbers come from? basically the model learns a coefficient for each input feature and those coefficients are used to calculate the likelihood of each class

Y_pred_probs = log.predict_proba(X_test)[:, 1] # das gibt mir nur die rechte column der tabelle aus, weil ja eh binary und der andere wert laesst sich leicht berechnen

# so per default the threshold is 0.5

""""
import matplotlib.pyplot as plt

plt.hist(Y_pred_probs, bins=8)
plt.xlim(0,1)
plt.xlabel("predicted probabiblities of aggressive comments")
plt.ylabel("frequency")
"""

#plot histogramm to show you the distribution. given the 0.5

#decrease the threshold, when can increase the sensitivity of the classifier
from sklearn.preprocessing import binarize
y_pred_class = binarize(Y_pred_probs, 0.3)[0] # more sensitive metal detector, now will return a one for all probabilites above .3
print Y_pred_probs[0:10]
print y_pred_class[0:10]

# Achtung! Adjusting the threshold should be one of the last steps in the model building process!!!

#check out how precision and recall are affected by various thresholds. thats simple, by plotting the ROC curve
# https://youtu.be/85dtiMz9tSo?t=44m21s
