from string import punctuation
from collections import Counter
from Utils.stanford import get_tagged_sent
from Utils.text_mods import strip_punctuation, get_sents
from numpy import median, average
from Features.Lexical.diversity import get_ttr
from Features.Grammatical.imperative import is_imperative
from Features.Lexical.subjectivity import get_subjectivity
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')



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
    return {k: v for k, v in counts.iteritems() if k in punctuation}



# to count words longer than this number
WORD_LENGHT_THRESHOLD = 7

# expects a raw text string
def get_wordcounts(text):
    # approach one: strip punctuation
    modified = text.replace("'", " ")
    words = strip_punctuation(modified, '!"()-./:;,?[\\]`').split()

    if len(words) == 0: #returns None if no words left after stripping punctuation.
        return

    nums = 0
    long_words_count = 0
    list_word_lengths = []
    count_one_char = 0
    noise_count = 0
    mixed_case_word_count = 0
    all_caps = {"count_all": 0, "one_char_count": 0}

    for word in words:
        if word.isdigit():
            nums += 1
        else:

            wl = len(word)
            list_word_lengths.append(wl)

            if wl == 1:
                count_one_char += 1
                if word.isupper():
                    all_caps["one_char_count"] += 1

            else:   # wl > 1
                if not word.isalpha():
                    noise_count += 1

                if word.isupper():
                    all_caps["count_all"] += 1

                elif not word[1:].islower() and not word[1:].isupper() or word.swapcase().istitle():
                    mixed_case_word_count += 1

            if wl > WORD_LENGHT_THRESHOLD:
                long_words_count += 1

    list_word_lengths = sorted(list_word_lengths)

    max_wordlength = max(list_word_lengths)
    wl_median = median(list_word_lengths)
    wl_average = average(list_word_lengths)

    all_caps["count_all"] += all_caps["one_char_count"]

    return {"one_char_token_count": count_one_char, "max_wordlength": max_wordlength, "num_count": nums,
            "word_count": len(list_word_lengths), "median_wordlength": wl_median, "average_wordlength": wl_average,
            "long_words_count": long_words_count, "noise_count": noise_count, "mixed_case_word_count": mixed_case_word_count,
            "all_caps_count": all_caps, "ttr": get_ttr(words)}


# TODO: check whether there's a simpler, more elegant method
def sent_count(comment):
    """ Input is tokenized comment from my_corpus.sents(my_corpus.fileids()[9]) object is instance of StreamBackedCorpusView
    :param comment: [[u'Mr.', u'Obama', u',', u'please', u'do', u"n't", u'give', u'10,000', u'Middle', u'East', u'terrorists', u'the', u'chance', u'to', u'enter', u'USA', u'and', u'kill', u'us', u'.'], [u'Instead', u',', u'conduct', u'a', u'mini', u'lottery', u'and', u'give', u'10,000', u'green', u'cards', u'to', u'undocumented', u'immigrants', u'who', u'are', u'already', u'here']]
    :return: 2
    """
    return comment.__len__()



 # Returns sentence stats:
 # number of sentences;
 # shortest and longest sent, average and median sent length
 # - length measured in tokens without punctuation.
def get_sent_counts(comment):

    sents = get_sents(comment)
    sent_lengths = []


    for sent in sents:
            modified = sent.replace("'", " ")
            words = strip_punctuation(modified, '!"()-./:;,?[\\]`').split()
            l = len(words)
            sent_lengths.append(l)

            #We still want punctuation for POS Tagging:
            tagged_sent = get_tagged_sent(sent)
            imp = is_imperative(tagged_sent)
            subj = get_subjectivity(tagged_sent)

        # TODO: IMPERATIVE
        # TODO: Subjectivity

    longest = max(sent_lengths)
    shortest = min(sent_lengths)
    med = median(sent_lengths)
    avg = average(sent_lengths)

    return {"sent_count": len(sents), "shortest": shortest, "longest": longest, "avg": avg, "median": med}




