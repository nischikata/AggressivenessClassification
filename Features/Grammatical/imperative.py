from nltk import RegexpParser
from nltk.tree import Tree


# should expect a minimum of two words (incl. punctuation)
def is_imperative(tagged_sent):

    imperative = False
    # polite refers to the empathic do or use of please / thank
    politecheck = [word[0].lower() for word in tagged_sent if word[0].lower() == "please" or word[0].lower() == "thank"]
    polite = len(politecheck) > 0
    indirect = False
    strengthcheck = [word[0] for word in tagged_sent if word[0] == "!" or word[0] == "?"]

    if len(tagged_sent) > 1: # minimum sentence example: "Go!"

        last = tagged_sent[-1][0]

        # check if the sentence ends with a full stop or exclamation mark(s)
        if last != "?":  # sentences ending with ! . or no punctuation

            # does the sentence begin with a verb in base form? if so, this is an imperative sentence.
            # checking for "do" at the beginning is due to the verb not being tagged correctly as VB (infinitive)
            if tagged_sent[0][1] == "VB" or tagged_sent[0][1] == "MD" or tagged_sent[0][0].lower() == "do":
                imperative = True

                # check for the empathic do (POLITE or FORMAL imperative):
                # examples: Do sit down. Do take a cookie.
                if not polite and tagged_sent[0][0].lower() == "do" and tagged_sent[1][1] == "VB":
                    polite = True

            # does the sentence begin with a verb in base form but has words like
            # "please", "you", "no," etc up front? if so, this is an imperative.
            # examples: "Please sit down.", "You shut up now!", "No, don't go."
            else:

                chunk = chunk_imperative(tagged_sent)
                # if type(node) is nltk.Tree, check if the first chunk of the sentence is a VB Phrase
                if (type(chunk[0]) is Tree) and chunk[0].label() == "VB-Phrase":
                    imperative = True

        # check whether it's an imperative with a Question Tag ->  makes the imperative less direct
        # examples "Don't tell anyone, will you?", "Everybody be quiet, will you?", "Would you help me, please?"
        #          "Stop doing that, please?"
        else:
            chunk = chunk_imperative(tagged_sent)

            # before checking the label, make sure it is a nltk.tree.Tree
            # the sentence has to end with a Question Tag and must start with a Verb in Base form

            if (((tagged_sent[0][1] == "VB" or tagged_sent[0][1] == "MD") and 'please' in politecheck)
                or type(chunk[-1]) is Tree and chunk[-1].label() == "Q-Tag"
                and (chunk[0][1]== "VB" or (type(chunk[0]) is Tree and chunk[0].label() == "VB-Phrase"))):

                imperative = True
                indirect = True

    strength = 0
    if imperative:
        if (len(strengthcheck)) == 0:
            pass
        elif (len(strengthcheck) == 1 and strengthcheck[0] == '!') or (len(strengthcheck) == 2 and '?' in strengthcheck):
            # 1 exclamation mark or at least one question mark and an exclamation mark (or a 2nd question mark)
            # signals moderate strength
            strength = 1
        elif len(strengthcheck) <= 3:
            strength = 3    # 2 or 3 repetitions is considered quite strong
        else:
            strength = 7    # more than 3 repetitions is considered extreme

    return {'imperative': imperative, 'polite': polite, 'indirect': indirect, 'strength': strength}


def chunk_imperative(tagged_sent):

    chunkgram = r"""VB-Phrase: {<DT><,>*<VB>}
                    VB-Phrase: {<DT><,><VBP>}
                    VB-Phrase: {<RB><VB>}
                    VB-Phrase: {<UH><,>*<VB>}
                    VB-Phrase: {<UH><,><VBP>}
                    VB-Phrase: {<PRP><VB>}
                    VB-Phrase: {<NN.?>+<,>*<VB>}
                    Q-Tag: {<,><MD><RB>*<PRP><.>*}"""

    """
    Note:
    The currently used POS tagger (model='stanford-postagger-full-2016-10-31/models/wsj-0-18-left3words-distsim.tagger')
    mis-tags occurences of "Do" as "VBP" instead of "VB" in certain cases (e.g. No, don't go. Please, don't go.)
    Therefore some VB-Phrases use VBP instead of VB. However, this should not lead to false positives since these
    constructs don't appear to make grammatical sense (afaik).
    """
    chunkparser = RegexpParser(chunkgram)
    return chunkparser.parse(tagged_sent)
