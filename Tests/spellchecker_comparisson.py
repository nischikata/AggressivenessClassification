from textblob import TextBlob, Word
import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter


"""
Enchant seems to perform better than TextBlob when used on a text with no spelling mistakes. TextBlob corrected a few
words that were actually correct. Both do not fare well with noise words though it must be pointed out, that TextBlob
at least sometimes does have the correct word among its suggestions (though they are usually ranked too low).


Performance regarding time:
enchant: 10 loops, best of 3: 435 msec per loop
TextBlob: 10 loops, best of 3: 2.78 sec per loop


Enchant seems to be overall the better choice.

correct word:  Obama
  enchant suggests:  ['Obadiah', 'Obadias', 'Bamako', 'Alabama']
  textBlob suggest:  [(u'Drama', 1.0)]
"""

# lists of tuples of typos/noise words and the correct word

# note: test output case insensitive
typos = [("teh", "the"),("cab=nt", "can't"), ("yrs", "years"), ("Jihadists", "Jihadists"), ("rediculous", "ridiculous"),
         ("muslims", "muslims"), ("baaaaad", "bad"), ("niiice", "nice"), ("Obama", "Obama"), ("Donald", "Donald"),
         ("Sh!t", "Shit"), ("$hit", "Shit"), ("f**k", "fuck"), ("f***ing", "fucking"), ("b@d", "bad"),
         ("ni99er", "nigger"), ("nigga", "nigger"), ("m0r0n", "moron"), ("@$$hole", "asshole")]

text = "Taking in such a large number of Muslims into America is akin to the citizens of TROY who " \
       "pulled in their own doom when they pulled in the wooden horse filled with Enemy soldiers into the fortress of" \
       " Troy. The Americans are doing the same thing, they are pulling in would be terrorists into their island " \
       "fortress of America. These are the same muslims who rejoiced and danced in the streets when the twin towers " \
       "were bought down by Bin Laden."

"""
TEXTBLOB:
https://textblob.readthedocs.io/en/dev/quickstart.html
does a lot more than just spellchecking such as POS tagging, noun phrase extraction, sentiment analysis, ....
(tried tokenization: does deliver worse results for noise words like $hit, sh!t, etc. than nltk tokenizer)

+ spelling suggestions have a confidence value
. ALWAYS offers at least one suggestion (which might be the input word, but with confidence level 0.0 ... interesting)


- automated correction does not include info which words were corrected
- corrects test sentence "He is a Muslim." into "He is a Slim."

"""
tb = TextBlob(text)
print tb.correct()


"""
PyEnchant
http://pythonhosted.org/pyenchant/tutorial.html

+ possible to store words in personal word list
+ checking of entire text blocks possible
+ has filters to ignore email addresses, urls, etc. - NICE!
+ multiple languages and multiple dictionaries supported

also includes a tokenizer, but same problem as textblob (plus it returns a list of tuples (word, position) - don't
need it)

- noise words or word lengthening are not handled well, suggestions - if there are any, they rarely include the correct
word
- does not know named entities (e.g. Obama)

Questions...
build own filters for use with enchant?

interesting testcase:
ERROR:  muslims  suggestion:  ['Muslims', 'muslins', 'mu slims']
-> !!!!! check when checking for error if it's just a case sensitivity problem !!!!!
"""

ench = enchant.Dict("en_US")
#check if a word is in the dictionary:
ench.check("hello")     # returns True
ench.check("helo")      # returns False

ench.suggest("Helo")    # returns an ordered list of suggestions (most likely to least likely) ['He lo', 'He-lo', 'Hello', 'Helot',...]

chkr = SpellChecker("en_US", filters=[EmailFilter,URLFilter])
chkr.set_text(text)
for err in chkr:
    print "ERROR: ", err.word, " suggestion: ", ench.suggest(err.word)

print "-------------------"
text2 = "Send an asldfjls em@il to: blabla@gmail.com!"
chkr.set_text(text2)
for err in chkr:
    print "ERROR: ", err.word, " suggestion: ", ench.suggest(err.word)


"""
for typo in typos:
    e = ench.suggest(typo[0])
    b = Word(typo[0]).spellcheck()

    print "correct word: ", typo[1]
    print "  enchant suggests: ", e
    print "  textBlob suggest: ", b
"""

def test_enchant():
    e = enchant.Dict("en_US")
    suggestions = []

    for typo in typos:
        suggestions.append(e.suggest(typo[0]))

    return suggestions


def test_textblob():
    suggestions = []

    for typo in typos:
        suggestions.append(Word(typo[0]).spellcheck())

    return suggestions


"""
TIME test from terminal:
python -mtimeit -s'import Tests.spellchecker_comparisson as sp' 'sp.test_enchant()'
python -mtimeit -s'import Tests.spellchecker_comparisson as sp' 'sp.test_textblob()'
"""