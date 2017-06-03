from Utils.dictionaries import auto_correct
from nltk import word_tokenize
from Utils.text_mods import normalize_comment


def autocorrect(text):
    tokens = word_tokenize(text)
    modified = ""

    for token in tokens:
        if any(c.isalnum() for c in token):
            token = auto_correct(token)

        modified += token + " "

    #print_mod(text, modified)
    return modified


def normalize(text):
    return normalize_comment(text)["normalized_comment"]


def corrections_demo(original):

    print "\n\n\n\n         A U T O - C O R R E C T I O N   D E M O"
    print "\n\n\n---------ORIGINAL TEXT---------------------------------------------------------------------------------\n"
    print " ", original
    print "\n---------AUTO-CORRECTED TEXT---------------------------------------------------------------------------\n"
    print " ", autocorrect(original)
    print "\n---------NORMALIZED TEXT-------------------------------------------------------------------------------\n"
    print " ", normalize(original)
    print "\n-------------------------------------------------------------------------------------------------------\n\n\n\n"

