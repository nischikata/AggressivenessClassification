from string import punctuation
import nltk.data
import re
from dictionaries import en_Dict, basic_leet_nums
import editdistance
from Features.Lexical.lexical import get_lexical_features
from nltk.stem import PorterStemmer

port = PorterStemmer()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


# Text modification module

def lowercase_n_stem(token):
    return port.stem(token.lower())


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

def strip_surrounding_punctuation(token, leading ='!(\'"`{<>', trailing ='\'"`)]<>?.,;!'):
    stripped = token.lstrip(leading).rstrip(trailing)
    return stripped


def get_sents(raw_comment):
    """
    Divides a raw string comment into sentences per paragraph
    sentences here are defined as ending in .?!\n (paragraph - since some users completely omit punctuation)

    :param raw_comment: string
    :return: a 2 dimensional list, consisting of a list of paraphs, which consist of a list of sentences

    >>> get_sents("Time is an illusion. Lunchtime doubly so.\\n- Douglas Adams" )
    [['Time is an illusion.', 'Lunchtime doubly so.'], ['- Douglas Adams']]
    """
    # TODO: use ellipsis as end of sentene too? But if I do this, I MUST call normalize_ellipsis(raw_comment) RIGHT HERE
    # This poses the next question though: What happens to a sentence like this 'Hello... !" TODO: investigate!!
    modified = handle_spaced_ellipsis(raw_comment)
    modified = normalize_ellipsis(modified)
    sents = []

    paragraphs = [p for p in modified.split('\n') if p]
    # and here, sent_tokenize each one of the paragraphs
    for paragraph in paragraphs:

        p_sents = tokenizer.tokenize(paragraph)

        if len(p_sents) > 1 and len(p_sents[-1]) == 1 and p_sents[-1] in ".?!":
        # if the last element in list is not a real sentence but punctuation, move and append it to the previous sentence element in list
            pop = p_sents.pop()
            p_sents[-1] += pop

        sents.append(p_sents)

    #
    return sents

def normalize_ellipsis(raw_sent):
    """
    Replaces any form of ellipsis (.., ..., ......) with a normalized version with a trailing blank (!)
    >>> normalize_ellipsis('...')
    '... '
    >>>
    >>> normalize_ellipsis("Hello..")
    'Hello... '
    >>> normalize_ellipsis("Hey. What's up..........?")
    "Hey. What's up... ?"
    >>> normalize_ellipsis("Hey......sup..?")
    'Hey... sup... ?'
    """
    return re.sub('[.][.]+', '... ', raw_sent)


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

    if len(token) < 2:
        return token
    if token[0] == "$" and re.search('[a-zA-Z]', token) is None:
        return ("$ " + token[1:])
    else:
        return token.replace("$", 's')


def handle_at(token):
    """
    replaces an '@' with an 'a' if it is not used in an email address. can deal with (trailing punctuation
    :param token:
    :return:

    >>> handle_at("zaphod@universe.com")
    'zaphod@universe.com'
    >>>
    >>> handle_at("b@st@rdo")
    'bastardo'
    >>> handle_at("trillian@universe.com...?")
    'trillian@universe.com...?'
    >>> handle_at("(marvin@dont-ask.com)")
    '(marvin@dont-ask.com)'
    """

    token_stripped = token.lstrip(':=\'"`()<>[]').rstrip(':=\'"()<>[].!?,;`') #remove leading and trailing punctuation
    if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", token_stripped) is None:
        return token.replace("@", "a")
    else:
        return token


def handle_exclamationMark(token):
    """
    replaces the '!' char with an 'i' if its within a word
    :param token: string
    :return: string

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


def handle_numeric_1337_speak(token):
    """

    turns 'sh1t' into 'shit'
    note: token should be preprocessed with handle_dollar

    :param token: string
    :return: string

    >>> handle_numeric_1337_speak("h473")
    'hate'
    >>> handle_numeric_1337_speak('5h1T!')
    'shiT!'
    >>> handle_numeric_1337_speak("666")
    '666'
    >>> handle_numeric_1337_speak("400!")
    '400!'
    >>> handle_numeric_1337_speak("$ 400")
    '$ 400'

    """
    stripped = strip_punctuation(token).replace(" ", "")
    if stripped.isdigit() or stripped.isalpha() or stripped == "":
        return token

    word = ""
    for i, c in enumerate(token):
        if c.isdigit():
            word += basic_leet_nums[c]
        else:
            word += c

    return word


def handle_lengthening(token):
    """
    To normalize lenghtend words like: 'niiiice' -> 'nice', 'coooooool' -> 'cool', 'realllllly' -> 'really'
    Note: only works for 3 repetitions or more (efficiency!) -> 'niice' stays the same 'niice'
    also punctuation and numbers will not be shortened
    :param token: string
    :return: string
    >>> handle_lengthening("cooooool")
    'cool'
    >>> handle_lengthening("niiiiiiiiiiiiiiice")
    'nice'
    >>> handle_lengthening("reallly")
    'really'
    >>> handle_lengthening("hellllloooooooo")
    'hello'
    >>> handle_lengthening("helloo!!!")
    'helloo!!!'
    >>> handle_lengthening("30000")
    '30000'
    >>> handle_lengthening("heeellllllooooo")   # 'fail' / room for improvement
    'heelloo'
    """

    # http://stackoverflow.com/a/1660758/4866678

    pattern = re.compile(r'([a-zA-Z])\1{2,}')
    f = pattern.search(token)
    len1 = ""
    while f:
        len1 = token[:f.start()] + f.group()[:1] + token[f.end():]
        token = token[:f.start()] + f.group()[:2] + token[f.end():]
        f = pattern.search(token)

    if len1 != "" and not en_Dict.check(strip_punctuation(token)):
        # if the token is not in the dictionary (e.g. niice), check if the len1 version is (e.g. nice)
        if en_Dict.check(strip_punctuation(len1)):
            token = len1

    return token


def handle_other_noise(token):
    """
    transforms other 'misused' characters in words into most likely alphabetical char
    :param token:
    :return:
    >>> handle_other_noise("S#%t")
    'Shit'
    >>> handle_other_noise("#42")
    '#42'
    >>> handle_other_noise("10%!")
    '10%!'
    """
    if any(str.isalpha(c) for c in token):  # and not any(str.isdigit(c) for c in token):
        token = token.replace("#", 'h')
        token = token.replace("%", 'i')
        # token = token.replace("+", 't') # this is problematic where '+' is a replacement for 'and'
    return token


# input raw comment exactly as it is
def handle_spacing(raw_comment):
    """
    collapses spaced words. e.g. 's h i t' -> 'shit'; 's.t.u.p.i.d' -> 'stupid'
    connects a sequence of single alpha characters (num alpha chars >= 3) to form a word

    :param raw_comment:
    :return:
    >>> handle_spacing("S t u p i d !")
    {'spaced_words_count': 1, 'modified_string': 'Stupid !'}
    >>> handle_spacing("T h i s is   s t u p i d!")
    {'spaced_words_count': 2, 'modified_string': 'This is   stupid!'}
    >>> handle_spacing("B.a.s.t.a.r.d!")
    {'spaced_words_count': 1, 'modified_string': 'Bastard!'}
    >>> handle_spacing("you i*d*i*o*t!")
    {'spaced_words_count': 1, 'modified_string': 'you idiot!'}
    """
    count = 0
    modified = ""
    search_string = raw_comment
    pattern = re.compile('(^|\s)(([a-zA-Z])( |$|[.!?*])){3,}')
    f = pattern.search(search_string)
    while f:
        word = f.group()[0] + strip_punctuation(f.group()[1:-1], False, " .!*") + f.group()[-1]
        if len(word) < f.group():
            count += 1

        modified += search_string[0:f.start()] + word
        search_string = search_string[f.end():] # search the rest of the string and add it to the modified head of string afterwards
        f = pattern.search(search_string)

    modified += search_string

    return {"modified_string": modified, "spaced_words_count": count}


def handle_spaced_ellipsis(raw_comment):    # TODO: TEST this!
    """
    collapses spaced ellipsis e.g. '. . .' -> '...'
    :param raw_comment:
    :return:
    >>> handle_spaced_ellipsis("This sucks. . . .!")
    'This sucks....!'
    """
    modified = ""
    search_string = raw_comment
    #pattern = re.compile('(([\.])( |$)){3,}')
    pattern = re.compile('(([\.])( )){2,}[\.]')
    f = pattern.search(search_string)
    while f:
        word = strip_punctuation(f.group(), False, " ")

        modified += search_string[0:f.start()] + word
        search_string = search_string[f.end():]
        f = pattern.search(search_string)

    modified += search_string
    return modified



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

def fix_lenghtening(fn):
    def wrapped(word):
        word = handle_lengthening(word)
        return fn(word)
    return wrapped

def fix_leet(fn):
    def wrapped(word):
        word = handle_numeric_1337_speak(word)
        return fn(word)
    return wrapped

def fix_other_noise(fn):
    def wrapped(word):
        word = handle_other_noise(word)
        return fn(word)
    return wrapped



@fix_at
@fix_exclamation
@fix_dollar
@fix_leet
@fix_lenghtening
@fix_other_noise
def fix_word(w):
    """
    applies preprocessing steps on input token and returns a 'fixed' version of the word
    :param w: string token
    :return: string token

    >>> fix_word("alright")
    'alright'
    >>>
    >>> fix_word("suuuuuucks")
    'sucks'

    """
    return w


def normalize_comment(raw_comment):
    """
    returns a noise corrected and normalized version of the comment, including a set of features
    :param raw_sentence: string
    :return: string
    >>> sent = "Hey a$$hole, give me $100!"
    >>> normalize_comment(sent)
    {'normalized_comment': 'Hey asshole, give me $ 100!', 'features': {'lengthening_counts': 0, 'spaced_words_count': 0, 'edit_distance': 3L}}
    >>> sent = "Th@ts $tuuuuuup!d! 5hu7 y0u2 724p."
    >>> normalize_comment(sent)
    {'normalized_comment': 'Thats stupid! shut your trap.', 'features': {'lengthening_counts': 1, 'spaced_words_count': 0, 'edit_distance': 15L}}
    >>> normalize_comment("If there's anything more important than my ego around, I want it caught and shot now.\\nSend an e-mail to: donald@madeinchina.com!!?.... ")
    {'normalized_comment': "If there's anything more important than my ego around, I want it caught and shot now.\\nSend an e-mail to: donald@madeinchina.com!!?...  ", 'features': {'lengthening_counts': 0, 'spaced_words_count': 0, 'edit_distance': 0L}}
    """

    processed = handle_spaced_ellipsis(raw_comment)     # CAUTION handle_spaced_ellipsis has not been tested thoroughly
    processed = normalize_ellipsis(processed)
    ellipsis_count = processed.count("...")     # ellipsis feature

    fixed_spacing = handle_spacing(processed)
    processed = fixed_spacing["modified_string"]

    # 1. split into tokens by " "
    tokens = processed.split(" ")
    processed_comment = ""
    # 2. find tokens that contain non alphanumeric chars but keep punctuation ( . , ? ! % () "" ' ) and similar intact
    # look for chars like @#%*$ or numbers within a word
    lengthening = 0
    edit_distance = 0
    count_modified_tokens = 0

    # starting with spellchecker and word-list features...
    features = {"no_dict": 0, "in_dict": 0, "urbdict_only": 0, "blacklist": 0, "polite": 0}

    for token in tokens:
        modified_token = fix_word(token)

        # edit distance shows how much a token has been altered
        ed = editdistance.eval(token, modified_token)
        edit_distance += ed

        if ed > 0:  #counting the number of tokens that were 'fixed'
            count_modified_tokens += 1

        features = get_lexical_features(strip_surrounding_punctuation(token), features)

        if len(modified_token) < len(token):
            lengthening += 1
        processed_comment += modified_token + " "

    features.update({"modified_tokens_count": count_modified_tokens, "lengthening_counts": lengthening,
                     "edit_distance": edit_distance, "spaced_words_count": fixed_spacing["spaced_words_count"],
                     "ellipsis_count": ellipsis_count})

    return {"normalized_comment": processed_comment[:-1],
            "features": features}


#print normalize_comment("Hey yo! what's up dude? shit.")
#print normalize_comment("If there's anything more important than my ego around, I want it caught and shot now.\\nSend an e-mail to: donald@madeinchina.com!!?.... ")
#print normalize_comment("You are a stuuuuupid l y i n g  b@$t@rd......!")
