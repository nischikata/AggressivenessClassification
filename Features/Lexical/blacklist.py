import pickle
import os.path

FILEPATH = "word_lists/blacklist_dict.pickle"
blacklist = set()   # set() for superfast access for unique values (much faster than a list)

def save_blacklist():
    """
    SAVE TO FILE FOR FASTER ACCESS next time
    :return: side effect only (dumps blacklist into pickle file)
    """
    pickle_out = open(FILEPATH, "wb")
    pickle.dump(blacklist, pickle_out)
    pickle_out.close()


# Load or create blacklist:
if not os.path.exists(FILEPATH):
    with open("word_lists/full-list-of-bad-words-banned-by-google-txt-file_2013_11_26_04_53_31_867.txt") as fp:
        for line in fp:
            blacklist.add(line.rstrip())
    save_blacklist()
else:
    # OPEN FILE and reconstruct BLACKLIST DICTIONARY
    pickle_in = open(FILEPATH, "rb")
    blacklist = pickle.load(pickle_in)


def is_blacklisted(term):
    """
    checks whether the given term is on the blacklist
    :param term:
    :return: True or False
    >>> is_blacklisted("avocado")
    False
    >>> is_blacklisted("dickhead")
    True
    """
    return term.lower() in blacklist or term in blacklist


def add_to_blacklist(terms):
    """
    adds the term(s) in lowercase into blacklist

    :param terms: single term or list of terms
    :return: None, but has sideffect: blacklist pickle is overwritten with updated version
    """
    if isinstance(terms, basestring):
        term = terms
        terms = [term]

    for term in terms:
        term = term.rstrip().lower()
        blacklist.add(term)
        save_blacklist()




# ----- TESTS -------

#print blacklist
#add_to_blacklist("libtard")
#add_to_blacklist("republicunt")
#add_to_blacklist("hitlery")
#add_to_blacklist("OBUmmer")
#add_to_blacklist("killary")
#add_to_blacklist(["Fraudbama", "Gaybama", "Obammy", "Obumma", "Ovomit"])
