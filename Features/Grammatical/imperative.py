
from nltk import word_tokenize
from nltk import RegexpParser
from nltk.tree import Tree
from Utils.text_mods import replace_dont
from Utils.stanford import POS_TAGGER
import sys
print(sys.version_info[0])

# should expect a minimum of two words (incl. punctuation)
def is_imperative(string_sent):
    print("\n---------------------------------")
    imperative = False
    strength = 0
    polite = string_sent.lower().find("please") >= 0  # refers to the empathic do or use of please
    indirect = False  # refers to presence of question tag
    tokenized_sent = (word_tokenize(replace_dont(string_sent)))
    tagged_sent = POS_TAGGER.tag(tokenized_sent)
    print(tagged_sent)


    if(len(tagged_sent) > 1): # minimum sentence example: "Go!"

        last = tagged_sent[-1][0]

        # check if the sentence ends with a full stop or exclamation mark(s)
        if (last == "." or last == "!"):
            if (last == "!"):
                strength += 1
                # check whether there are multiple exclamation marks at the end of the sentence
                if (tagged_sent[-2][0] == "!"):
                    strength +=1

            # does the sentence begin with a verb in base form? if so, this is an imperative sentence.
            if (tagged_sent[0][1] == "VB"):
                imperative = True
                #print ("this is an IMPERATIVE")

                # check for the empathic do (POLITE or FORMAL imperative):
                # examples: Do sit down. Do take a cookie.
                if (not polite and tagged_sent[0][0] == "Do" and tagged_sent[1][1] == "VB"):
                    polite = True

            # does the sentence begin with a verb in base form but has words like
            # "please", "you", "no," etc up front? if so, this is an imperative.
            # examples: "Please sit down.", "You shut up now!", "No, don't go."
            else:

                chunk = chunk_imperative(tagged_sent)
                # if type(node) is nltk.Tree, check if the first chunk of the sentence is a VB Phrase
                if ((type(chunk[0]) is Tree) and chunk[0].label() == "VB-Phrase"):
                    imperative = True

        # check whether it's an imperative with a Question Tag ->  makes the imperative less direct
        # examples "Don't tell anyone, will you?", "Everybody be quiet, will you?"
        elif (last == "?"):
            chunk = chunk_imperative(tagged_sent)

            # before checking the label, make sure it is a nltk.tree.Tree
            # the sentence has to end with a Question Tag and must start with a Verb in Base form

            if (type(chunk[-1]) is Tree and chunk[-1].label() == "Q-Tag" and (chunk[0][1]== "VB" or (type(chunk[0]) is  Tree and chunk[0].label() == "VB-Phrase"))):


                imperative = True
                indirect = True


    # TODO: return a more finegrained result... like
    # 0 ... imperative using '.'
    # 1 ... strong imperative using '!'
    # 2 ... extreme imperative using '!!*"

    return {'imperative': imperative, 'polite': polite, 'indirect': indirect, 'strength': strength}


def chunk_imperative(tagged_sent):

    chunkGram = r"""VB-Phrase: {<DT><,>*<VB>}
                    VB-Phrase: {<RB><VB>}
                    VB-Phrase: {<UH><,>*<VB>}
                    VB-Phrase: {<PRP><VB>}
                    VB-Phrase: {<NN.?>+<,>*<VB>}
                    Q-Tag: {<,><MD><RB>*<PRP><.>}"""

    chunkParser = RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged_sent)
    print(chunked)
    return(chunked)