import enchant
import urbandictionary as ud

en_Dict = enchant.Dict("en_US")

basic_leet_nums = {'0': 'o', '1': 'i', '2': 'r', '3': 'e', '4': 'a', '5': 's', '6': 'b', '7': 't', '8': 'B', '9': 'g'}


# ----- URBAN DICTIONARY ----

def in_urbanDict(term):
    """
    :param term: string; single token or phrase
    :return: True or False

    >>> in_urbanDict("White House")
    True
    >>> in_urbanDict("White House!??") # urban dictionary is able to deal with punctuation -> cool!
    True
    """
    return ud.define(term) != []


def get_best_UrbanDefinition(term):
    defs = ud.define(term)
    if len(defs) > 0:
        # Access:
        # text definition of term via defs[i].definition
        # number of upvotes: defs[i].upvotes
        # number of downvotes: defs[i].downvotes
        # usage example: defs[i].example
        return defs[0]
    else:
        return None


# ----- REGULAR DICTIONARY (enchant) ----

def in_regularDict(word):
    """
    :param word:
    :return:
    >>> in_regularDict("White House")
    False
    >>> in_regularDict("White")
    True
    >>> in_regularDict("House!") # cannot deal with punctuation!
    False
    """
    return en_Dict.check(word)


def auto_correct(word):
    """
    :param word: single string word
    :return: same word (if it exists in en_US dictionary) or the highest ranked spelling suggestion
    >>> auto_correct("happy")
    'happy'
    >>> auto_correct("unhapy")
    'unhappy'

    """
    if not in_regularDict(word):
        suggestions = en_Dict.suggest(word)
        if len(suggestions) > 0:
            word = suggestions[0]

    return word




