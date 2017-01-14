from Utils.text_mods import get_sents, strip_punctuation, handle_noise
from Utils.stanford import get_tagged_sent
from Utils.tiny_helpers import flatten
"""
# create a comment object with all the different representations of the comment text
# (raw, punctuation stripped, raw sentences, punctuation stripped sentences, spellcorrected, POS tagged...)

also should include fileid

I guess i will move EVERYTHING from the counters.py into this class... makes sense, right?



def get_sent_counts(comment):

    sents = get_sents(comment)
    sent_lengths = []


    for sent in sents:
            modified = sent.replace("'", " ")
            words = strip_punctuation(modified, '!"()-./:;,?[\\]`').split()
            l = len(words)
            sent_lengths.append(l)

            #We still want punctuation for POS Tagging:
            tagged_sent = get_tagged_sent(sent)
            imp = is_imperative(tagged_sent)
            subj = get_subjectivity(tagged_sent)
"""

class Comment:
    def __init__(self, raw_text, fileid="", category=0):
        self.raw = raw_text
        self.fileid = fileid
        self.cat = category
        self.init()

    def init(self):
        paras = get_sents(self.raw)
        self.cnt_paras = len(paras)
        self.raw_sents = flatten(paras)
        self.sents_processed = self.get_sents_variations()


    # HELPERS

    def get_sents_variations(self):
        stripped = []
        noise_handled = []
        pos_tagged = []
        for sent in self.raw_sents:
            stripped.append(strip_punctuation(sent, True))

            no_noise = handle_noise(sent)
            noise_handled.append(no_noise)

            pos_tagged.append(get_tagged_sent(no_noise))

        return {"punc_stripped": stripped, "noise_handled": noise_handled, "pos_tagged": pos_tagged}



    # COMMENT TEXT REPRESENTATIONS (raw sents, tagged sents, preprocessed sents,....)



    def raw_sentences(self):
        return self.raw_sents

    def comment_wo_punctuation(self):
        return ' '.join(s for s in self.sents_processed["punc_stripped"])

    #TODO noise corrected sentences
    #TODO

    # NUMERIC REPRESENTATIONS of comment (amount of paragraphs, sentences, words,....)
    def count_paras(self):
        return self.cnt_paras

    def count_sents(self):
        return len(self.raw_sents)



co = Comment("Shut up! I'm so sick of it all.\nGimme a break. NIce!", "123")
print co.raw_sentences()
print co.count_paras()
