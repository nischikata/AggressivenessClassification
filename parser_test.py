# Parsing:
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from Utils.stanford import get_tagged_sent
import time

stanford_parser_dir = 'stanford-parser-full-2016-10-31/'
eng_model_path = stanford_parser_dir + "edu/stanford/nlp/models/lexparser/englishRNN.ser.gz"
my_path_to_models_jar = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
my_path_to_jar = stanford_parser_dir + "stanford-parser.jar"

#parser=StanfordParser(model_path=eng_model_path, path_to_models_jar=my_path_to_models_jar, path_to_jar=my_path_to_jar)
parser = StanfordDependencyParser(path_to_jar=my_path_to_jar, path_to_models_jar=my_path_to_models_jar)

#r = parser.parse_sents([["I", "like", "apples", "and", "bananas", "."]])


# http://www.nltk.org/api/nltk.parse.html#nltk.parse.stanford.StanfordDependencyParser

#mylist = [parse.tree() for parse in r]

#mylist = [parse.tree() for parse in parser.raw_parse("The quick brown fox jumps over the lazy dog.")]
print "Starting to parse:  ", time.ctime()


mylist = [list(parse.triples()) for parse in parser.raw_parse("The quick brown fox jumps over the lazy dog.")]

print "FINISHED parsing with raw parse ", time.ctime()

for i in mylist:
    print mylist


print "UND JETZT MIT TAGGED SENT"
print "Starting to parse:  ", time.ctime()

# TODP: als input POS-tagged sentences rein schieben (performance!) und schaun wie ich zu diesen triples komme
# tagged_parse([("I", "PRP"), ("am", "VBP"])...
# returns iter(Tree)

mylist = [list(parse.triples()) for parse in parser.tagged_parse(get_tagged_sent("The quick brown fox jumps over the lazy dog."))]
print "FINISHED parsing with tagged parse ", time.ctime()

for i in mylist:
    print mylist

"""
for i in r:
    for j in i:
        #print j
        next(i)
    next(r)
"""

#[list(parse.triples()) for parse in