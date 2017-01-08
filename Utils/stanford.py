from nltk.internals import find_jars_within_path
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from Utils.text_mods import replace_dont

# ---- 1. SETUP ENVIRONMENT VARIABLES ----

sjar = 'stanford-postagger-full-2015-12-09/stanford-postagger.jar'
model = 'stanford-postagger-full-2015-12-09/models/english-left3words-distsim.tagger'


# ---- 2. CREATE POS TAGGER ----
POS_TAGGER = StanfordPOSTagger(model, sjar)

#  ---- 3. ADD OTHER JARS FROM STANFORD DIRECTORY ----
# yep, that should happen anyway if the CLASSPATH is set, but for some reason it doesn't - these 3 lines will do the job:
stanford_dir = POS_TAGGER._stanford_jar[0].rpartition('/')[0]
# if error occurs here see https://gist.github.com/alvations/e1df0ba227e542955a8a
stanford_jars = find_jars_within_path(stanford_dir)
POS_TAGGER._stanford_jar = ':'.join(stanford_jars)

def get_tagged_sent(string_sent):
    tokenized_sent = (word_tokenize(replace_dont(string_sent)))
    return POS_TAGGER.tag(tokenized_sent)

#print get_tagged_sent("Hello world.")