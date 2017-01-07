from string import punctuation
from tiny_helpers import *
import nltk.data
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk import word_tokenize
from nltk import TreebankWordTokenizer
# Text modification module

def replace_dont(string_sent):
    """
    >>> sent = "Don't do it."
    >>> replace_dont(sent)
    'Do not do it.'
    >>>
    >>> sent = "Please don't do it."
    >>> replace_dont(sent)
    'Please do not do it.'
    """
    i = string_sent.lower().find("don't")
    return string_sent[:i] + string_sent[i:].replace("on't", "o not", 1)  # only replace the first occurrence


#tinas_punctuation = '!"\'()-./:;?[\\]`'

def strip_punctuation(string_text, punc = punctuation):
    return ''.join(c for c in string_text if c not in punc)


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# returns a list of raw sentences, given a raw comment
# sentences here are defined as ending in .?!\n (paragraph - since some users completely omit punctuation)
def get_sents(raw_comment):
    sents = []
    # in my case, when it had '\n', I called it a new paragraph,
    # like a collection of sentences
    paragraphs = [p for p in raw_comment.split('\n') if p]
    # and here, sent_tokenize each one of the paragraphs
    for paragraph in paragraphs:

        p_sents = tokenizer.tokenize(paragraph)

        if len(p_sents) > 1 and len(p_sents[-1]) == 1 and p_sents[-1] in ".?!":
        # if the last element in list is not a real sentence but punctuation, move and append it to the previous sentence element in list
            pop = p_sents.pop()
            p_sents[-1] += pop

        sents.append(p_sents)

    # flatten sents,
    # otherwise returns a 2dim list, consisting of a list of paraphs,
    # which themselves consist of a list of sentences - could be useful (paragraph count)
    return flatten(sents)

