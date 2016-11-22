from Utils.text_mods import replace_dont
from Utils.stanford import POS_TAGGER
from string import punctuation
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def count_tokens(text):
    pass


def max_wordlength(text):
    pass


def punctuation_count(text):
    """Returns number of occurence of punctions  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    >>> text = "Hello, 'world'! What's the time? It's: 12.20 a.m."
    >>> punctuation_count(text)
    {'!': 1, "'": 4, ',': 1, '.': 3, ':': 1, '?': 1}
    >>>
    >>> text = "Hi (there) +"
    >>> punctuation_count(text)
    {')': 1, '(': 1, '+': 1}
    """
    counts = Counter(text)
    return {k: v for k, v in counts.iteritems() if k in punctuation }


# TODO fix this completely rewrite possibly
def word_count(text):
    """Returns number of occurence of punctions  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    >>> text = "Hello, 'world'! What's the time?"
    >>> word_count(text)
    6
    >>>
    >>> text = "Hi there..."
    >>> word_count(text)
    2
    """
    pcount = punctuation_count(text)
    pcountsum = sum(pcount.values())
    tokens = word_tokenize(text)
    print(tokens)
    print(pcountsum)
    sums = len(tokens) - pcountsum
    return sums


word_count("hell, world!! ju")


def sent_count(comment):
    """ Input is tokenized comment from my_corpus.sents(my_corpus.fileids()[9]) object is instance of StreamBackedCorpusView
    :param comment: [[u'Mr.', u'Obama', u',', u'please', u'do', u"n't", u'give', u'10,000', u'Middle', u'East', u'terrorists', u'the', u'chance', u'to', u'enter', u'USA', u'and', u'kill', u'us', u'.'], [u'Instead', u',', u'conduct', u'a', u'mini', u'lottery', u'and', u'give', u'10,000', u'green', u'cards', u'to', u'undocumented', u'immigrants', u'who', u'are', u'already', u'here']]
    :return: 2
    """
    return comment.__len__()


