
import pickle
import os.path

FILEPATH = "politeness_dict.pickle"
polite_terms = set()   # set() for superfast access for unique values (much faster than a list)

def save_list(): # TODO: funktion auslagern in Utils fuer subjectivity dict, blacklist und politeness
    """
    SAVE TO FILE FOR FASTER ACCESS next time
    :return: side effect only (dumps list into pickle file)
    """
    pickle_out = open(FILEPATH, "wb")
    pickle.dump(polite_terms, pickle_out)
    pickle_out.close()


# Load or create list: # TODO: als funktion auslagern in Utils
if not os.path.exists(FILEPATH):
    with open("word_lists/polite.txt") as fp:
        for line in fp:
            polite_terms.add(line.rstrip())
    save_list()
else:
    # OPEN FILE and reconstruct  DICTIONARY
    pickle_in = open(FILEPATH, "rb")
    polite_terms = pickle.load(pickle_in)

#print polite_terms

def is_polite(term):
    """
    checks whether the given term is on the polite list
    :param term:
    :return: True or False
    >>> is_polite("idiot")
    False
    >>> is_polite("pardon me")
    True
    """
    return term.lower() in polite_terms

"""
MORE IDEAS: https://www.callcentrehelper.com/the-top-25-positive-words-and-phrases-1847.htm

The -LY Ending

This is a little known persuasion secret by all but the major corps and their marketing agencies.

Surprisingly, if you start a sentance with a word ending in LY then what follows is regarded as truth and is very hard to object to.

For example...

Interestingly this is what other customers have...
Naturally my goal is to make sure...
Amazingly we were able to...


https://www.myenglishteacher.eu/blog/polite-expressions-in-english-words-phrases-and-questions-to-be-kind/

2. Negative Question Forms

Another way we can make our English more diplomatic is by using negative questions when we want to make a suggestion.
A more indirect version looks like this:
Shouldn't we redesign the company logo?

3. Using the Past Continuous Tense

Another way to make a sentence less direct and more diplomatic is to use the past continuous tense:

4. Finally, the passive voice is a great way to make your sentences sound more diplomatic:

"""