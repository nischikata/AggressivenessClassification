from feature_vector import get_feature_vector
from comment import Comment
import numpy as np
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import TreebankWordTokenizer
import pickle
import os.path
import time
import pandas as pd
import re
pd.options.mode.chained_assignment = None

FILEPATH = "dataset.pickle"
FILEPATH_WIKI = "wiki_dataset_good.pickle"
MIN_CHARS_COMMENT = 5

start_index = 0
error_fileid = ""
error = False

def save(dataset, filename = FILEPATH): # TODO: funktion auslagern in Utils
    """
    SAVE TO FILE FOR FASTER ACCESS next time
    :return: side effect only (dumps dataset dict into pickle file)
    """

    pickle_out = open(filename, "wb")
    pickle.dump(dataset, pickle_out)
    pickle_out.close()

def load(filename = FILEPATH):
    # OPEN FILE and reconstruct dataset
    pickle_in = open(filename, "rb")
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
    

def get_dataset(filename = FILEPATH):
    """
    # load or compute and save dataset
    :return:
    """

    # TODO: als funktion auslagern in Utils
    if not os.path.exists(filename):

        corpus = CategorizedPlaintextCorpusReader('Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')
        print "Starting to compute dataset at  ", time.ctime()
        dataset = compute_dataset(corpus)
        print "FINISHED to compute dataset at  ", time.ctime()
        save(dataset, filename)
    else:
        dataset = load(filename)

    return dataset


def test_fileid(fileid):
    corpus = CategorizedPlaintextCorpusReader('Data/', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')
    c = Comment(corpus.raw(fileid), fileid)
    observation = get_feature_vector(c)
    print "--- fileid ", fileid, " -----"
    print corpus.raw(fileid)
    print "------"
    c.print_POStagged_sents()
    c.print_normalized_sents()
    print "raw sents========"
    print c.raw_sents
    print "raw comment===="
    print repr(c.raw)

    return observation
    
  
# ---------------- WIKI DATASET: --------------------------------------------

def preprocess_wiki_comments(comments):
    # replace newline and tab tokens
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("NEWLINE_TOKEN", "\n"))
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("TAB_TOKEN", "   "))
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("``", "\""))
    comments['comment'] = comments['comment'].apply(lambda x: x.replace("`", "'"))
      

def get_wiki_comments():
    comments = pd.read_csv('Data/wiki/aggression_annotated_comments.tsv', sep = '\t', index_col = 0)
    annotations = annotations = pd.read_csv('Data/wiki/aggression_annotations.tsv', sep='\t')
    
    mean = annotations.groupby('rev_id')['aggression'].mean()# > 0.25 
    # join labels and comments
    comments['aggression_value'] = mean
    
    # only keep comments that fall below or above the 25% threshold, drop the rest     
    comments_good = comments.query('aggression_value < 0.25')
    comments_bad  = comments.query('aggression_value > 0.75')
    
    # label the comments
    comments_good['category'] = 'ok'
    comments_bad['category'] = 'aggressive'

    preprocess_wiki_comments(comments_good)
    preprocess_wiki_comments(comments_bad)
    
    return comments_good, comments_bad


def get_wiki_comment(row):
    text = row['comment']
    text = text.decode("utf-8")
    
    alpha_chars = re.findall(r'[A-z]', text)
    
    if len(alpha_chars) < MIN_CHARS_COMMENT: # making sure the comment has at least
        return None
    
    else:
        return Comment(text, row["category"])

   
def compute_wiki_dataset(good, bad):
    
    observations = []
    target = []
    
    comments = good.append(bad)
    
    for index, row in comments.iterrows():
        
        try:
            c = get_wiki_comment(row)
        except:
            print "Hey Tina, ERROR! Exception caught: ", index, " Row: ", str(row)
            pass
        
        if c is not None:
            observation = get_feature_vector(c)
            observations.append(observation)

            label = c.get_label()
            target.append(label)

    # turn lists into numpy arrays
    observations = np.array(observations)
    target = np.array(target)
    dataset = {"data": observations, "target": target}

    return dataset
    

def get_wiki_dataset(filename = FILEPATH):
    """
    # load or compute and save dataset
    :return:
    """

    # TODO: als funktion auslagern in Utils
    if not os.path.exists(filename):
        n = 5
                
        good, bad = get_wiki_comments()
        print "Starting to compute WIKI dataset at  ", time.ctime()
        for i in range(2):
            fn = "wiki_" + str(i) + ".pickle"
            dataset = compute_wiki_dataset(good[i*n:i*n+n], bad[i*n:i*n+n])
            save(dataset, fn)
        print "FINISHED to compute WIKI dataset at  ", time.ctime()
        
    else:
        dataset = load(filename)

    return dataset