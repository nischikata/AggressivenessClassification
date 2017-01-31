
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from Utils.text_mods import replace_dont


# ---- 1. SETUP ENVIRONMENT VARIABLES ----
sjar = 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'

#TODO: check which model is the best in terms of speed and accuracy (speed might be more important...)
#model = 'stanford-postagger-full-2016-10-31/models/english-left3words-distsim.tagger'
model = 'stanford-postagger-full-2016-10-31/models/wsj-0-18-left3words-distsim.tagger'

# ---- 2. CREATE POS TAGGER ----

POS_TAGGER = StanfordPOSTagger(model, sjar, encoding='utf8')


def get_tagged_sent(string_sent):
    tokenized_sent = (word_tokenize(replace_dont(string_sent)))
    return POS_TAGGER.tag(tokenized_sent)