from __future__ import print_function
sjar = '/Users/nischikata/PycharmProjects/JabRef-2.11.1.jar'

from nltk.corpus import stopwords
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import word_tokenize
from nltk import TreebankWordTokenizer
from nltk import WordPunctTokenizer
import nltk.data
from Utils.stanford import POS_TAGGER

# PLAINTEXT CORPUS READER
# http://www.nltk.org/_modules/nltk/corpus/reader/plaintext.html#CategorizedPlaintextCorpusReader
# important: The TreebankWordTokenizer separates words like "don't" into "do", "n't", consequently the main verb is correctly identified.
# For the Naive Bayes it may be better though to use WordPunctTokenizer - it is the default, so just omit the word_tokenizer param
corpus = CategorizedPlaintextCorpusReader('.', r'(?!\.).*\.txt', word_tokenizer=TreebankWordTokenizer(), cat_pattern=r'(aggressive|not_aggressive)/.*', encoding='utf8')

# Getting RAW SENTENCES from RAW Comment seee: http://stackoverflow.com/a/4576110/4866678
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# returns a list of raw sentences
def get_raw_sentences(fileid): # works mostly but problem with last sentence ending with ?! !! (multiple punct) TODO: fix or remove
    data = corpus.raw(fileid)
    return tokenizer.tokenize(data)

def get_raw_paragraph(fileid): #TODO test if this works with yahoo! corpus as well (encoding might differ)
    data = corpus.raw(fileid)
    return data.split(u"\r\n \r\n")

def get_sents(comment):
    return tokenizer.tokenize(comment)




sents = get_raw_sentences('not_aggressive/Test.txt')
print("\n\n\n")
print(sents)
print(type(sents))
print("\n\n\n")
print(get_sents("He's here!! Omg!! He's here, right? wow!!! "))
print("\n\n")

# ACCESS all FILEIDS:
# corpus.fileids([category])  # category is optional
# print(corpus.fileids())

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

#print(len(corpus.words(corpus.fileids()[1])))


# ITERATE OVER FILEIDS
for fileid in corpus.fileids()[1:2]:
    print(fileid)
    print(type(fileid))
    print(len(corpus.raw(fileid)))
    print(corpus.raw(fileid))

    #sents = get_raw_sentences(fileid)
    sents = get_raw_paragraph(fileid)
   # print("SENT:  " + "\nSENT:  ".join(sents))
    words = corpus.words(fileid)
    print(words)
    print(*words, sep='\n')


"""
tags = POS_TAGGER.tag(corpus.words(corpus.fileids()[1]))
tags1 = POS_TAGGER.tag(word_tokenize(corpus.raw(corpus.fileids()[1])))
tags2 = POS_TAGGER.tag("This ni99er doesn't know $hit?!".split())
print(*tags, sep='\n')
print ("======\n")
print(*tags1, sep='\n')

print ("=======\n")
print(*tags2, sep='\n')
"""