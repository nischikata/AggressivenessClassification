from string import punctuation
import nltk.data
import re
import enchant

en_Dict = enchant.Dict("en_US")

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


def strip_punctuation(string_text, seperate_contractions=False, punc = punctuation):
    """
    :param string_text:
    :param seperate_contractions: pass True if contractions like "don't", "isn't" should become "don t", "isn t"
    :param punc: the characters that are going to be stripped (eg. '!"\'()-./:;?[\\]`' )
    :return: a string stripped off the punctuation

    >>> sent = "Don't do it."
    >>> strip_punctuation(sent, True)
    'Don t do it'
    """

    if seperate_contractions:
            string_text = string_text.replace("'", " ")
            string_text = string_text.replace("`", " ")
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

    # returns a 2dim list, consisting of a list of paraphs, which consist of a list of sentences
    return sents

def normalize_ellipsis(raw_sent):
    """
    >>> sent = "Hello.."
    >>> normalize_ellipsis(sent)
    'Hello...'
    >>>
    >>> sent = "Hey. What's up..........?"
    >>> normalize_ellipsis(sent)
    "Hey. What's up...?"
    >>> normalize_ellipsis("Hey...... sup..?")
    'Hey... sup...?'
    """
    return re.sub('[.][.]+', '...', raw_sent)


def handle_dollar(token):
    """
    replaces the '$' char with an 's' if it's not at the beginning of a numeric value.
    :param token:
    :return:

    >>> t = "$3.5"
    >>> handle_dollar(t)
    '$ 3.5'
    >>>
    >>> t = "$!X"
    >>> handle_dollar(t)
    's!X'
    >>> handle_dollar("dumba$$")
    'dumbass'
    """
    if token[0] == "$" and re.search('[a-zA-Z]', token) is None:
        return ("$ " + token[1:])
    else:
        return token.replace("$", 's')

def handle_at(token):
    """
    replaces an '@' with an 'a' if it is not used in an email address
    :param token:
    :return:

    >>> handle_at("zaphod@universe.com")
    'zaphod@universe.com'
    >>>
    >>> handle_at("b@st@rdo")
    'bastardo'
    """
    if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", token) is None:
        return token.replace("@", "a")
    else:
        return token


def handle_exclamationMark(token):
    """
    replaces the '!' char with an 'i' if its within a word
    :param token:
    :return:

    >>> t = "Stop!!?!"
    >>> handle_exclamationMark(t)
    'Stop!!?!'
    >>>
    >>> t = "$!X"
    >>> handle_exclamationMark(t)
    '$iX'
    >>> handle_exclamationMark("Sh!t!!!")
    'Shit!!!'
    >>> handle_exclamationMark("tr!99er")
    'tri99er'
    """
    if '!' in token:
        punc = True
        index = len(token) - 1
        new_token = ""
        while index >= 0:
            char = token[index]
            index -= 1

            if punc and char not in punctuation:
                punc = False

            if char == '!' and not punc:
                char = 'i'

            new_token = char + new_token

        return new_token

    else:
        return token


def handle_lengthening(token):
    """
    To normalize lenghtend words like: 'niiiice' -> 'nice', 'coooooool' -> 'cool', 'realllllly' -> 'really'
    :param token:
    :return:
    >>> handle_lengthening("cooooool")
    'cool'
    >>> handle_lengthening("really")
    'really'
    >>> handle_lengthening("hellllloooooooo")
    'helloo'
    """

    # http://stackoverflow.com/a/1660758/4866678

    f = re.search(r'(.)\1{3,}', token)
    while f:
        token = token[:f.start()] + f.group()[:2] + token[f.end():]
        f = re.search(r'(.)\1{3,}', token)

    return token



def handle_noise(raw_sentence):
    """
    :param raw_sentence:
    :return:
    >>> sent = "Hey a$$hole, give me $300!"
    >>> handle_noise(sent)
    'Hey asshole, give me $ 300!'
    >>> sent = "Th@ts $tup!d!"
    >>> handle_noise(sent)
    'Thats stupid!'
    """
    #TODO:
    # find sequences of . and if they are not of length 1 or 3, then change them to length 3
    # 1. split into tokens by " "
    tokens = raw_sentence.split(" ")
    new_sent = ""
    # 2. find tokens that contain non alphanumeric chars but keep punctuation ( . , ? ! % () "" ' ) and similar intact
    # look for chars like @#%*$ or numbers within a word


    for token in tokens:
        new_sent += fix_word(token) + " "


    # 3. TODO: is there a sequence of single char tokens, possibly even all caps? uuh! that's a sign

    return new_sent[:-1]


def get_spellchecked(word):
    """
    :param word: single string word
    :return: same word (if it exists in en_US dictionary) or the highest ranked spelling suggestion
    >>> get_spellchecked("happy")
    'happy'
    >>> get_spellchecked("unhapy")
    'unhappy'

    """
    if en_Dict.check(word):
        return word
    else:
        suggestions = en_Dict.suggest(word)
        if len(suggestions) > 0:
            return suggestions[0]
        else:
            return word



# PLAYING WITH DECORATORS  --- How cooooool is that???? :-))))))
# http://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators-in-python?rq=1
def fix_at(fn):
    def wrapped(word):
        word = handle_at(word)
        return fn(word)
    return wrapped

def fix_exclamation(fn):
    def wrapped(word):
        word = handle_exclamationMark(word)
        return fn(word)
    return wrapped

def fix_dollar(fn):
    def wrapped(word):
        word = handle_dollar(word)
        return fn(word)
    return wrapped


@fix_at
@fix_exclamation
@fix_dollar
def fix_word(w):
    return w
