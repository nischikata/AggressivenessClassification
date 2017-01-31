from __future__ import division
from string import punctuation
from collections import Counter
from Utils.text_mods import strip_punctuation, get_sents
from Utils.tiny_helpers import flatten
from numpy import median, average
from Features.Lexical.diversity import get_ttr
import nltk.data


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# to count words longer than this number
WORD_LENGHT_THRESHOLD = 7

def get_char_count(raw_comment, whitespaces=True):
    """
    counts the length of the given string, optionally without the whitespaces
    :param raw_comment: string
    :param whitespaces: set False to exclude whitespaces from count
    :return: integer
    """
    if whitespaces:
        return len(raw_comment)
    else:
        return len("".join(raw_comment.split()))   # strip all whitespaces and count remaining chars


def get_whitespace_ratio(raw_comment):
    all_chars = get_char_count(raw_comment)
    wo_whitespace = get_char_count(raw_comment, False)
    return wo_whitespace/all_chars


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


def get_punctuation_stats(raw_comment):
    """

    :param raw_comment:
    :return:
    """
    punctuation_dict = punctuation_count(raw_comment)

    period_count = 0 if '.' not in punctuation_dict else punctuation_dict['.']
    exclamation_count = 0 if '!' not in punctuation_dict else punctuation_dict['!']
    questionmark_count = 0 if '?' not in punctuation_dict else punctuation_dict['?']

    comma_count = 0 if ',' not in punctuation_dict else punctuation_dict[',']
    semicolon_count = 0 if ';' not in punctuation_dict else punctuation_dict[';']
    colon_count = 0 if ':' not in punctuation_dict else punctuation_dict[':']
    dash_count = 0 if '-' not in punctuation_dict else punctuation_dict['-']

    quotation_count = 0 if '"' not in punctuation_dict else punctuation_dict['"']
    asterisk_count = 0 if '*' not in punctuation_dict else punctuation_dict['*']
    l_paranth = 0 if '(' not in punctuation_dict else punctuation_dict['(']
    r_paranth = 0 if ')' not in punctuation_dict else punctuation_dict[')']

    sent_endings = period_count + questionmark_count + exclamation_count    # note: doesn't take ellipsis into account

    connectors = comma_count + semicolon_count + colon_count + dash_count

    highlighters = quotation_count + l_paranth + r_paranth + asterisk_count # quotation marks etc. visually seperate content from rest of text, they 'highlight'

    period_ratio = 0 if sent_endings == 0 else period_count/sent_endings
    exclamation_ratio = 0 if sent_endings == 0 else exclamation_count/sent_endings
    questionmark_ratio = 0 if sent_endings == 0 else questionmark_count/sent_endings

    return {"period_ratio": period_ratio, "exclamation_ratio": exclamation_ratio,
            "questionmark_ratio": questionmark_ratio, "sent_endings_count": sent_endings,
            "connectors_count": connectors, "highlighters_count": highlighters}



# expects a raw text string
def get_wordcounts(tokens): #TODO rewrite pytest input in count_test.py
    """

    :param words: expects a list of tokens, (surrounding) punctuation stripped
    :return: a dict of features
    >>> get_wordcounts(['hello', 'world'])

    """
    # approach one: strip punctuation
    #words = strip_punctuation(text, True, '!"()-./:;,?[\\]`').split()

    if len(tokens) == 0:     #if no words left after stripping punctuation.
        return None

    nums = 0
    long_words_count = 0
    list_word_lengths = []
    count_one_char = 0
    noise_count = 0
    mixed_case_word_count = 0
    all_caps = {"count_all": 0, "one_char_count": 0}

    for token in tokens:
        if token.isdigit():
            nums += 1
        else:

            wl = len(token)
            list_word_lengths.append(wl)

            if wl == 1:
                count_one_char += 1
                if token.isupper():
                    all_caps["one_char_count"] += 1

            else:   # wl > 1
                if not token.isalpha():
                    noise_count += 1

                if token.isupper():
                    all_caps["count_all"] += 1

                elif not token[1:].islower() and not token[1:].isupper() or token.swapcase().istitle():
                    mixed_case_word_count += 1

            if wl > WORD_LENGHT_THRESHOLD:
                long_words_count += 1

    list_word_lengths = sorted(list_word_lengths)

    max_wordlength = max(list_word_lengths)
    wl_median = median(list_word_lengths)
    wl_average = average(list_word_lengths)

    all_caps["count_all"] += all_caps["one_char_count"]     # count of all tokens in all caps style

    return {"one_char_token_count": count_one_char, "max_wordlength": max_wordlength, "num_count": nums,
            "word_count": len(list_word_lengths), "median_wordlength": wl_median, "average_wordlength": wl_average,
            "long_words_count": long_words_count, "noise_count": noise_count, "all_caps_count": all_caps,
            "mixed_case_word_count": mixed_case_word_count, "ttr": get_ttr(tokens)}



 # Returns sentence stats:
 # number of sentences;
 # shortest and longest sent, average and median sent length
 # - length measured in tokens without punctuation.
def get_sent_counts2(comment): #TODO rewrite input, get it form Comment object

    sents = get_sents(comment)
    sents = flatten(sents)
    sent_lengths_w = [] # length in words
    sent_lengths_ch = [] # lenght in characters



    for sent in sents:
            words = strip_punctuation(sent, True, '!"()-./:;,?[\\]`').split()
            l = len(words)
            sent_lengths_w.append(l)
            ch = len(sent)
            w_ch_ratio = l/ch
            sent_lengths_ch.append(ch)


    longest = max(sent_lengths_w)
    shortest = min(sent_lengths_w)
    med = median(sent_lengths_w)
    avg = average(sent_lengths_w)

    #TODO words to characters ratio

    return {"sent_count": len(sents), "shortest": shortest, "longest": longest, "avg": avg, "median": med}


def get_sent_counts(tokenized_sents):
    """
    shortest and longest sent, average and median sent length
    length measured in tokens without punctuation.

    :param tokenized_sents: a list of tokenized sentences
    :return: a dict
    """

    sent_lengths_w = []     # length in words

    for tokens in tokenized_sents:
        l = len(tokens)
        sent_lengths_w.append(l)

    longest = max(sent_lengths_w)
    shortest = min(sent_lengths_w)
    med = median(sent_lengths_w)
    avg = average(sent_lengths_w)

    return {"sent_count": len(tokenized_sents), "shortest_sent_len": shortest, "longest_sent_len": longest, "avg_sent_len": avg, "median_sent_len": med}

