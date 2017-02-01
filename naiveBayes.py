from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import TreebankWordTokenizer
from Utils.text_mods import strip_surrounding_punctuation
import random
import nltk
from nltk.corpus import stopwords

corpus = CategorizedPlaintextCorpusReader('Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')

documents = []
words = []

for fileid in corpus.fileids():

    comment = corpus.raw(fileid)
    tokens = comment.split()
    stripped_tokens = [strip_surrounding_punctuation(token).lower() for token in tokens]
    stripped_tokens = filter(None, stripped_tokens)
    words.extend(stripped_tokens)

    label = 1 if fileid[0] == 'a' else 0
    documents.append((stripped_tokens, label))

random.shuffle(documents)

all_words = []

#all_words_filtered = []
for w in words:
    #print w, " type: ", type(w)
    #all_words.append(w.lower())
    if w not in stopwords.words('english'):
        all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = sorted(all_words, key=all_words.get)
reversed = word_features[::-1]
word_features = reversed[:3000]


def find_features(document):
    words = set(document)
    features = {} # empty dicitionary

    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

pivot = len(featuresets)//2     # forced integer division
training_set = featuresets[:pivot]
testing_set = featuresets[pivot:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes Algo accuracay: ", (nltk.classify.accuracy(classifier, testing_set))* 100)

#classifier.show_most_informative_features(20)

def accuracy():
    random.shuffle(featuresets)
    pivot = len(featuresets)//2     # forced integer division
    training_set = featuresets[:pivot]
    testing_set = featuresets[pivot:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    acc = nltk.classify.accuracy(classifier, testing_set)
    print("Naive Bayes Algo accuracay: ", acc * 100)
    return acc

n = 25
acc = 0
for i in range(n):
    acc += accuracy()

print "accuracy", acc/n