from nltk.internals import find_jars_within_path
from nltk.tag import StanfordPOSTagger

# ---- 1. SETUP ENVIRONMENT VARIABLES ----

sjar = '/Users/nischikata/PycharmProjects/stanford-postagger-full-2015-12-09/stanford-postagger.jar'
model = '/Users/nischikata/PycharmProjects/stanford-postagger-full-2015-12-09/models/english-left3words-distsim.tagger'


# ---- 2. CREATE POS TAGGER ----
POS_TAGGER = StanfordPOSTagger(model, sjar)

#  ---- 3. ADD OTHER JARS FROM STANFORD DIRECTORY ----
# yep, that should happen anyway if the CLASSPATH is set, but for some reason it doesn't - these 3 lines will do the job:
stanford_dir = POS_TAGGER._stanford_jar.rpartition('/')[0]
stanford_jars = find_jars_within_path(stanford_dir)
POS_TAGGER._stanford_jar = ':'.join(stanford_jars)
