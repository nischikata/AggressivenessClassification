from Utils.stanford import get_tagged_sent
from Features.Grammatical.imperative import is_imperative


def demo(sent):
    tagged_sent = get_tagged_sent(sent)
    result = is_imperative(tagged_sent)
    print "\n----------------------------------------------------------------------------------"
    print "INPUT SENTENCE: \n ", sent, "\n ", tagged_sent, "\n"
    print " Imperative? -> ", result["imperative"], "  polite? -> ", result["polite"], \
          "  indirect? -> ", result["indirect"], "  strength: ", result["strength"]

    print "\n----------------------------------------------------------------------------------"

    return result