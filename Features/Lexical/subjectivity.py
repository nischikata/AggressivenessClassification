import pickle
import os.path
from nltk.stem import PorterStemmer


FILEPATH = "subjectivity_dict.pickle"
WEAKSUBJ = 1
STRONGSUBJ = 2

subjectivity_dict = {}

port = PorterStemmer()

if not os.path.exists(FILEPATH):
    print "does not exist"

    with open('subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff') as fp:
        for line in fp:
            entry = line.split(" ")

            word = entry[2][6:]
            subj = STRONGSUBJ if entry[0][5] is 's' else WEAKSUBJ
            pos = entry[3][5:] #pos ... part of speech tag #TODO convert to PENN TREEBANK II CONSTITUENT TAGS...hmmmm... IF I ever even need it...
            stemmed = True if entry[4][9] is 'y' else False
            polarity = entry[5][14:].strip("\n")
            subjectivity_dict[word] = {"strongsubj": subj, "pos": pos, "stemmed": stemmed, "polarity": polarity}

    pickle_out = open("subjectivity_dict.pickle", "wb")
    pickle.dump(subjectivity_dict, pickle_out)
    pickle_out.close()

else:
    pickle_in = open(FILEPATH, "rb")
    subjectivity_dict = pickle.load(pickle_in)



## TODO: call this function from counters.py get word_counts() (OR if needed per sentence get sents_count() in the loop)
# tokens: list of tokens without punctuation
# ideally the tokens have been spell-checked and corrected ALREADY
def get_subjectivity(tokens):
    weak = strong = 0

    for token in tokens:
        stemmed = port.stem(token)
        if token in subjectivity_dict:
            print "first try success. ", token
        elif stemmed in subjectivity_dict:
            print "stemmed version here ", token, " :  ", "stemmed"
        else:
            print "not in subj dict. ", token

    return {"weaksubj": weak, "strongsubj": strong}


# ------ testing stuff and reminders ----- remove when done

print subjectivity_dict["zest"]
print subjectivity_dict["stupid"]

# checking whether a word is in the subjectivity dictionary:
if "you" in subjectivity_dict:
    print "you is there"
else:
    print "you is not there"

# testing the corpus
text = "I am so happy".split(" ")
get_subjectivity(text)




# TODO: check this out: http://stackoverflow.com/a/2116011/4866678
# TODO: is_emotive()