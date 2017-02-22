from nltk import RegexpParser
from nltk.tree import Tree

# should expect a minimum of two words (incl. punctuation)
def is_imperative(tagged_sent):

    imperative = False
    strength = 0
    sent_dict = dict(tagged_sent)
    #polite refers to the empathic do or use of please / thank
    politecheck = [word[0].lower() for word in tagged_sent if word[0].lower() == "please" or word[0].lower() == "thank"]
    polite = len(politecheck) > 0
    indirect = False
    strengthcheck = [word[0] for word in tagged_sent if word[0] == "!" or word[0] == "?"]

    if(len(tagged_sent) > 1): # minimum sentence example: "Go!"

        last = tagged_sent[-1][0]

        # check if the sentence ends with a full stop or exclamation mark(s)
        if (last != "?"): # sentences ending with ! . or no punctuation
            if (last == "!"):
                strength += 1
                # check whether there are multiple exclamation marks at the end of the sentence
                if (tagged_sent[-2][0] == "!"): #TODO: this may be fast but... what about '!!?!' at this point i can safely assume all '!' are punctuation so just count occurences?
                    strength +=1

            # does the sentence begin with a verb in base form? if so, this is an imperative sentence.
            if (tagged_sent[0][1] == "VB" or tagged_sent[0][1] == "MD" ):    # TODO: does use of MODAL verb make imperative more polite/indirect? e.g. 'Would you shut up now!'
                imperative = True


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
        if (len(strengthcheck) == 1 and strengthcheck[0] == '!') or (len(strengthcheck) == 2 and '?' in strengthcheck):
            # 1 exclamation mark or at least one question mark and an exclamation mark (or a 2nd question mark) signals moderate strength
            strength = 1
        elif len(strengthcheck) <= 3:
            strength = 3    # 2 or 3 repetitions is considered quite strong
        else:
            strength = 7    # more than 3 repetitions is considered extreme
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
    #print(chunked)
    return(chunked)
    

#print(is_imperative("This is so cool!"))