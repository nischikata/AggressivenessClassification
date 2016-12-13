import numpy as np
#import Data.corpus as C
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import word_tokenize
from nltk import TreebankWordTokenizer
import Features.Other.counters as cnt
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics





def get_observation(fileid):
    observation = np.zeros(10)
        # Get data in different forms
    raw_comment = corpus.raw(fileid)
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




def get_model(corpus, start, end):  #TODO: use default params

    observations = []
    target = []

    for fileid in corpus.fileids()[start:end]:
        observation = get_observation(fileid)
        label = get_label(fileid)

        observations.append(observation)
        target.append(label)
        print(fileid)
        print(observation)
        print(label)
        print("\n\n--------------------")

        # turn lists into numpy arrays
    observations = np.array(observations)
    target = np.array(target)
    return {"data": observations, "target": target}


corpus = CategorizedPlaintextCorpusReader('../Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')



modl = get_model(corpus, 30, 80)

log = LogisticRegression()
X = modl["data"]
y = modl["target"]

log.fit(X, y)

testmodl = get_model(corpus, 1, 5)

prediction = log.predict(testmodl["data"])

print("This is the prediction")
print(prediction)
print("This is the actual label")
print(testmodl["target"])


# Test Training accuracy (TODO: improve it by using precision, recall, f-score)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

#first step: split the Dataset into 2 pieces (commonly 20-40% of the set is used for testing)
# i guess by controlling the random state you do k-fold cross-validation TODO: check how to best do k-fold cross validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=2)

trained = log.fit(X_train, y_train)
y_pred = log.predict(X_test)

print metrics.accuracy_score(y_test, y_pred)