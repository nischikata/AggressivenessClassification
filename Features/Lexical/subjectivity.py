import pickle
import os.path
from Utils.text_mods import port
import random


FILEPATH = "word_lists/subjectivity_dict.pickle"
# strengths of subjectivity:
STRONGSUBJ = 1.0
WEAKSUBJ = 0.5

STRENGTHS = { "weaksubj": WEAKSUBJ, "strongsubj": STRONGSUBJ}
POLARITIES = ["positive", "negative", "neutral", "both"]


def convert_POS(pos_word):
    pos_tags = {"anypos": "anypos", "verb": "VB", "adj": "JJ", "noun": "NN", "adverb": "RB"}
    return pos_tags[pos_word]

subjectivity_dict = {}


if not os.path.exists(FILEPATH):

    with open('word_lists/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff') as fp:
        for line in fp:
            entry = line.split(" ")

            stemmed = True if entry[4][9] is 'y' else False
            # TODO: add stemmed version of unstemmed words to dictionary,
            # TODO: additionaly if time check if it already exists and if so check polarity, there might be a conflict!

            #  if the word is marked as stemmed, stem it with THE STEMMER THAT I USE, so the stems will actually
            #  match. else use the word as is:
            word = port.stem(entry[2][6:]) if stemmed else entry[2][6:]
            strength = STRONGSUBJ if entry[0][5] is 's' else WEAKSUBJ

            # POS TAG:
            pos = convert_POS(entry[3][5:])

            polarity = entry[5][14:].strip("\n")

            if word in subjectivity_dict:
                subjectivity_dict[word][pos] = {"strength": strength, "stemmed": stemmed, "polarity": polarity}

            else:
                subjectivity_dict[word] = {pos: {"strength": strength, "stemmed": stemmed, "polarity": polarity}}

    # SAVE TO FILE FOR FASTER ACCESS next time
    pickle_out = open(FILEPATH, "wb")
    pickle.dump(subjectivity_dict, pickle_out)
    pickle_out.close()

else:
    # OPEN FILE and reconstruct SUBJECTIVITY DICTIONARY
    pickle_in = open(FILEPATH, "rb")
    subjectivity_dict = pickle.load(pickle_in)


# tagged_sent: a sentence in the form of POS-Tag tuple tokens
def get_subjectivity(tagged_sent):
    polarity = {"positive": 0.0, "negative": 0.0, "both": 0.0, "neutral": 0.0, "none": 0.0, "subj": 0.0}

    for t in tagged_sent:

        token = t[0].lower()

        if not token.isalpha():
            continue

        # check if the token is in the subj dict, else try the stemmed version of the token
        token = token if token in subjectivity_dict else port.stem(token)

        if token in subjectivity_dict:
            polarity["subj"] += 1
            item = subjectivity_dict[token]
            #item looks like {pos: {"strength": strength, "stemmed": stemmed, "polarity": polarity}}

            tag = t[1][:2]  # only take the first 2 chars - we don't care about subcategories of pos tags

            # check if the tag of this token is available for the lexicon item that was found
            # e.g. token = ("blood", "NN") ... see if there is an NN-tag entry for the "blood" item
            # yes there is:
            # blood {'JJ': {'stemmed': False, 'polarity': 'neutral', 'strength': 0.5},
            #        'NN': {'stemmed': False, 'polarity': 'negative', 'strength': 0.5}}

            if tag not in item:
                if tag == 'RB':     # adverb is close enought to adjectiv
                    tag = 'JJ'
                else:
                    tag = 'anypos'

            if tag in item:
                # print "matching POS tag found for ", token, " tag: ", tag
                data = item[tag]
                # data looks like {"strength": strength, "stemmed": stemmed, "polarity": polarity}
                polarity[data["polarity"]] += data["strength"]

            else:
                # TODO: decide: take a random entry from the item dict or nothing?
                # right now I am choosing a random entry and add its value
                random_tag = random.choice(item.keys())
                data = item[random_tag]
                polarity[data["polarity"]] += data["strength"]

        else:
            # token is not in subjectivity dictionary
            polarity["none"] += 1

    return polarity

# TODO: FINISH THIS! funktionalitaet von obiger methode in diese auslagern
def get_word_subjectivity(word, pos_tag):
    word = word if word in subjectivity_dict else port.stem(word)

    pass



# ------ TESTS, REMINDERS AND PROBLEMS/CHALLENGES----- remove when done

#print "zest", subjectivity_dict["zest"]
#print "blood", subjectivity_dict["blood"]
#print "precious", subjectivity_dict["precious"]

#text = [(u'The', u'DT'), (u'patient', u'NN'), (u'lost', u'VBD'), (u'a', u'DT'), (u'lot', u'NN'), (u'of', u'IN'), (u'blood', u'NN')]

#print get_subjectivity(text)


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


(SORT OF) SOLVED by assigning RANDOM Tag if no matching Tag was found:
type=weaksubj len=1 word1=tangled pos1=adj stemmed1=n priorpolarity=negative
Tangled here is an adjective, but it can also be VBZ or VBN, depending on the situation.

"""

# intersting stuff swore VS sworn (polarity):
# type=strongsubj len=1 word1=swore pos1=verb stemmed1=n priorpolarity=negative
# type=strongsubj len=1 word1=sworn pos1=adj stemmed1=n priorpolarity=positive