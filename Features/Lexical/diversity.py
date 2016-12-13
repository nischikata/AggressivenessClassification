from __future__ import division     # otherwise / is integer division

def get_ttr(token_list):
    #TODO: this is just a primitive form of lexical diversity - must research more into this

    lowercase_tokens = list(map(lambda x: x.lower(), token_list))#map(str.lower, token_list)
    return len(set(lowercase_tokens)) / len(token_list)


"""
o: the simplest way to assess the amount of diversity would simply be to count the number of different terms in a sample.
This measure has been referred to in the past as Number of Different Words (NDW) and is now conventionally referred to
as Types. The problem here is obvious: you could not reliably compare a 75-word sample to a 100-word sample, let alone
a 750-word sample. To account for this, researchers developed whats called a Type-to-Token  Ratio (TTR). This figure
simply places the number of unique words (Types) in the numerator and the number of total words (Tokens) in the
denominator, to generate a ratio that is 1 or lower. The highest possible TTR, 1, is only possible if you never
repeat a term, such as if you are counting (one, two, three...) without repeating. The lowest possible TTR, 1/tokens, is
only possible if you say the same word over and over again (one,  one, one.).

BUT:
We can therefore say that TTR is not robust to changes in sample size, and repeated empirical investigations have
demonstrated that this sensitivity can apply even when the difference in text lengths are quite small. TTR fails to
adequately control for the confounding variable it was expressly intended to control for.
"""