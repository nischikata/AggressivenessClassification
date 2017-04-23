
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from Utils.text_mods import replace_dont
from nltk.parse.stanford import StanfordDependencyParser

# ---- 1. POS TAGGER ----
sjar = 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
model = 'stanford-postagger-full-2016-10-31/models/wsj-0-18-left3words-distsim.tagger'

POS_TAGGER = StanfordPOSTagger(model, sjar, encoding='utf8')


def get_tagged_sent(string_sent):
    tokenized_sent = (word_tokenize(replace_dont(string_sent)))
    return POS_TAGGER.tag(tokenized_sent)


# ---- 2. DEPENDENCY PARSER ----

stanford_parser_dir = 'stanford-parser-full-2016-10-31/'
eng_model_path = stanford_parser_dir + "edu/stanford/nlp/models/lexparser/englishRNN.ser.gz"
my_path_to_models_jar = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
my_path_to_jar = stanford_parser_dir + "stanford-parser.jar"

#parser=StanfordParser(model_path=eng_model_path, path_to_models_jar=my_path_to_models_jar, path_to_jar=my_path_to_jar)
PARSER = StanfordDependencyParser(path_to_jar=my_path_to_jar, path_to_models_jar=my_path_to_models_jar)


def get_dependencies(sent):

    #mylist = [list(parse.triples()) for parse in PARSER.tagged_parse(get_tagged_sent(sent))]
    triples = PARSER.tagged_parse(get_tagged_sent(sent)).next().triples()
    #triples = list(triples)
    #for triple in triples:
    #    print triple, "\n"
    #print "------------"

    return list(triples)


def print_dep_triples(triples):
    for triple in triples:
        print triple, "\n"
    print "------------"