import pickle
import os.path
from nltk.stem import PorterStemmer


FILEPATH = "subjectivity_dict.pickle"
# strengths of subjectivity
STRONGSUBJ = 1.0
WEAKSUBJ = 0.5
NOSUBJ = 0.0
#polarity of word
#positive, negative, both, neutral
POSITIVE = 0
NEGATIVE = 0
BOTH = 0
NEUTRAL = 0
polarities = ["positive", "negative", "neutral", "both"]


def convert_POS(pos_word):
    pos_tags = {"anypos": "anypos", "verb": "VB", "adj": "JJ", "noun": "NN", "adverb": "RB"}
    return pos_tags[pos_word]

subjectivity_dict = {}

port = PorterStemmer()

if not os.path.exists(FILEPATH):

    with open('subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff') as fp:
        for line in fp:
            entry = line.split(" ")


            stemmed = True if entry[4][9] is 'y' else False
            # TODO: add stemmed version of unstemmed words to dictionary,
            # TODO: additionaly if time check if it already exists and if so check polarity, there might be some conflict!

            #  if the word is marked as stemmed, stem it with THE STEMMER THAT I USE, so the stems will actually match. else use the word as is:
            word = port.stem(entry[2][6:]) if stemmed else entry[2][6:]
            strength = STRONGSUBJ if entry[0][5] is 's' else WEAKSUBJ

            # POS TAG:
            pos = convert_POS(entry[3][5:])



            polarity = entry[5][14:].strip("\n")




            if word in subjectivity_dict:
                """
                pol = subjectivity_dict[word]["polarity"]

                if pol != polarity:
                    pass

                   # print "POLARITY CONFLICT: ", word, "  ", pol, "  ", polarity

                if subjectivity_dict[word]["strength"] != strength:
                    pass
                    #print "TYPE CONFLICT: ", word, "  ", strength, "  ", subjectivity_dict[word]["strength"]
                """
                subjectivity_dict[word][pos] = {"strength": strength, "stemmed": stemmed, "polarity": polarity}

            else:
                subjectivity_dict[word] = {pos: {"strength": strength, "stemmed": stemmed, "polarity": polarity}}


            #subjectivity_dict[word] = {"strength": strength, "pos": pos, "stemmed": stemmed, "polarity": polarity}



    #pickle_out = open("subjectivity_dict.pickle", "wb")
    #pickle.dump(subjectivity_dict, pickle_out)
    #pickle_out.close()

else:
    pickle_in = open(FILEPATH, "rb")
    subjectivity_dict = pickle.load(pickle_in)



## TODO: call this function from counters.py get word_counts() (OR if needed per sentence get sents_count() in the loop)
# tokens: list of tokens without punctuation
# ideally the tokens have been spell-checked and corrected ALREADY
def get_subjectivity(tokens):
    polarity = { "positive": 0.0, "negative": 0.0, "both": 0.0, "neutral": 0.0}
    none = 0.0
    subj = 0.0


    for token in tokens:
        print token
        token = token if token in subjectivity_dict else port.stem(token)
        print token

        if token in subjectivity_dict:
            #token is in subjectivity dict
            subj += 1
            # TODO check the pos tag of the token and see if it matches a pos tag from the entry, then take polarity and strength from there


        else:
            # token is not in subjectivity dictionary
            none += 1


    return polarity


# ------ testing stuff and reminders ----- remove when done

print "zest", subjectivity_dict["zest"]
print "stupid", subjectivity_dict["stupid"]
print "precious", subjectivity_dict["precious"]


# testing the corpus
text = "Swore sworn".split(" ")
#get_subjectivity(text)




# TODO: check this out: http://stackoverflow.com/a/2116011/4866678
# TODO: is_emotive()


"""
REMINDER:
When changing anything in the subjectivity_dictionary build DELETE THE PICKLE and rebuild! ;-)

 P R O B L E M S   and   C H A L L E N G E S :

SOLVED:
some words are being marked as stemmed (e.g. "survive", "surprise"), but the stemmed version of survive is "surviv"
which means they appear both as stemmed but they do not match!
... might need to do some preprocessing when building my subjectivity_lexicon.. -> letting the
stemmer stem at least those, that are marked as stemmed...

SOLVED:
out of place character in the dataset removed

SOLVED:
converted POS Tags into corresponding PENN TREEBANK II CONSTITUENT TAGS

SOLVED:
since there may be multiple versions of the identical word (see entries for "suspicious") but with different
POS Tags some entries will be simply OVERWRITTEN... this does matters if the POS Tags are used as source
of information and especially if the polarity of the word is tied to the POS Tag, as well as the subjectivity type
(Strong vs weak) !! --> TESTED programmatically -> this IS AN ACTUAL PROBLEM
examples:
TYPE CONFLICT:  need    1.0    0.5
TYPE CONFLICT:  okay    1.0    0.5
TYPE CONFLICT:  pain    0.5    1.0
TYPE CONFLICT:  passive    1.0    0.5
POLARITY CONFLICT:  pleas    negative    positive
POLARITY CONFLICT:  precious    positive    neutral
POLARITY CONFLICT:  precious    neutral    positive
POLARITY CONFLICT:  presum    neutral    negative

---> This means: POS TAGS must be considered as well, including their corresponding strength and polarity


NEXT PROBLEM:
type=weaksubj len=1 word1=tangled pos1=adj stemmed1=n priorpolarity=negative
Tangled here is an adjective, but it can also be VBZ or VBN, depending on the situation.

"""

# intersting stuff swore VS sworn (polarity):
# type=strongsubj len=1 word1=swore pos1=verb stemmed1=n priorpolarity=negative
# type=strongsubj len=1 word1=sworn pos1=adj stemmed1=n priorpolarity=positive