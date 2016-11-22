sjar = '/Users/nischikata/PycharmProjects/JabRef-2.11.1.jar'

from nltk.corpus import stopwords
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import word_tokenize
from nltk import TreebankWordTokenizer
import nltk.data

# PLAINTEXT CORPUS READER
# http://www.nltk.org/_modules/nltk/corpus/reader/plaintext.html#CategorizedPlaintextCorpusReader
# important: The TreebankWordTokenizer separates words like "don't" into "do", "n't", consequently the main verb is correctly identified.
# For the Naive Bayes it may be better though to use WordPunctTokenizer - it is the default, so just omit the word_tokenizer param
corpus = CategorizedPlaintextCorpusReader('.', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')


# Getting RAW SENTENCES from RAW Comment seee: http://stackoverflow.com/a/4576110/4866678
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# returns a list of raw sentences
def get_raw_sentences(fileid): # works
    data = corpus.raw(fileid)
    return tokenizer.tokenize(data)

def get_raw_paragraph(fileid): #TODO test if this works with yahoo! corpus as well (encoding might differ)
    data = corpus.raw(fileid)
    return data.split(u"\r\n \r\n")


# ACCESS all FILEIDS:
# corpus.fileids([category])  # category is optional
print(corpus.fileids())

# GET ABSOLUTE PATH TO a FILEID
# corpus.abspath('not_aggressive/0__10.txt')

# GET RAW CORPUS
# corpus.raw()  or corpus.raw()[:10]  to get the first 10 chars of the raw text


# GET RAW TEXT COMMENT given fileid
# corpus.raw([fileid])  #  my_corpus.raw(my_corpus.fileids()[2])) # prints raw text of file index 2 of whole corpus#

# GET list of TOKENIZED SENTS for a COMMENT via index or fileid:
# sents = corpus.sents(corpus.fileids()[index])
# sents = corpus.sents([fileid])

"""
GET TOKENIZED PARAGRAPHS
para = corpus.paras([fileid])
comment
"""

"""
GET TOKENIZED COMMENT
para = corpus.paras([fileid])
comment
"""



# ITERATE OVER FILEIDS
for fileid in corpus.fileids()[22:23]:
    print(fileid)
    print(type(fileid))
    print(len(corpus.raw(fileid)))
    print(corpus.raw(fileid))

    #sents = get_raw_sentences(fileid)
    sents = get_raw_paragraph(fileid)
   # print("SENT:  " + "\nSENT:  ".join(sents))
    words = corpus.words(fileid)
    print(words)

