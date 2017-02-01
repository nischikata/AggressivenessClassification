from feature_vector import get_feature_vector
from comment import Comment
import numpy as np
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import TreebankWordTokenizer
import pickle
import os.path

FILEPATH = "dataset.pickle"

start_index = 0
error_fileid = ""
error = False

def save(dataset): # TODO: funktion auslagern in Utils
    """
    SAVE TO FILE FOR FASTER ACCESS next time
    :return: side effect only (dumps dataset dict into pickle file)
    """

    pickle_out = open(FILEPATH, "wb")
    pickle.dump(dataset, pickle_out)
    pickle_out.close()

def load():
    # OPEN FILE and reconstruct dataset
    pickle_in = open(FILEPATH, "rb")
    return pickle.load(pickle_in)



sentinel = object()
def compute_dataset(corpus, start=0, end=sentinel):
    if end is sentinel:
        end = len(corpus.fileids())

    observations = []
    target = []

    for fileid in corpus.fileids()[start:end]:
        c = Comment(corpus.raw(fileid), fileid)

        observation = get_feature_vector(c)
        observations.append(observation)

        label = c.get_label()


        target.append(label)
        # TODO: save fileid (where? separate array?) to enable to identify outliers
        # fileids that are outliers etc

    # turn lists into numpy arrays
    observations = np.array(observations)
    target = np.array(target)
    return {"data": observations, "target": target}


def get_dataset():
    """
    # load or compute and save dataset
    :return:
    """

    # TODO: als funktion auslagern in Utils
    if not os.path.exists(FILEPATH):

        corpus = CategorizedPlaintextCorpusReader('Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')

        dataset = compute_dataset(corpus)
        save(dataset)
    else:
        dataset = load()

    return dataset


