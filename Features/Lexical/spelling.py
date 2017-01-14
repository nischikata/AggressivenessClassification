import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter




# Apply spellchecker after auto correction of noise-words
# Apply it to whole comment which includes punctuation.

#TODO first find all NAMED ENTITIES, possibly remove them from string, so the you only get the errors
# this way i'll get at least the number of spelling mistakes; fixing is a different chapter. not sure if i'll do it since
# doesn't work too well for simple errors :(
# Might have to create a comment object with all the different representations of the comment text
# (raw, punctuation stripped, raw sentences, punctuation stripped sentences, spellcorrected, POS tagged...)

ench = enchant.Dict("en_US")
#check if a word is in the dictionary:
ench.check("hello")     # returns True
ench.check("helo")      # returns False
print ench.check("Paris")
print ench.check("Afghanistan")
print ench.check("refugees")

ench.suggest("Helo")    # returns an ordered list of suggestions (most likely to least likely) ['He lo', 'He-lo', 'Hello', 'Helot',...]

text = "I have great spelling. Don't you think?"
chkr = SpellChecker("en_US", filters=[EmailFilter,URLFilter])
chkr.set_text(text)
for err in chkr:
    print "ERROR: ", err.word, " suggestion: ", ench.suggest(err.word)
    err.replace(ench.suggest(err.word))

print "-------------------"
text2 = "They`re my friends' addresses: blabla@gmail.com and blub@gmailc.om. His name is Obama. That's Hillary. It s a nce day, isnt it? Cant go wrong with that. Thats Donald the old duck."
chkr.set_text(text2)
for err in chkr:
    print "ERROR: ", err.word, " suggestion: ", ench.suggest(err.word)
    err.replace(ench.suggest(err.word)[0])


print chkr.get_text()