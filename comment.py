from Utils.text_mods import get_sents, strip_surrounding_punctuation, normalize_comment
from Utils.stanford import get_tagged_sent
from Utils.tiny_helpers import flatten
from Features.Lexical.subjectivity import get_subjectivity
from Features.Grammatical.imperative import is_imperative
from Features.Other.counters import get_wordcounts, get_punctuation_stats, get_sent_counts, get_whitespace_ratio

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

        paras = get_sents(self.raw)
        self.cnt_paras = len(paras)
        self.raw_sents = flatten(paras)

        self.features = {"paras_count": self.cnt_paras}

        self.sents_processed = self.__compute_sents_variations()
        self.features.update(get_sent_counts(self.get_sent_tokens_wo_punctuation()))
        self.features["subjectivity"] = self.get_subjectivity_features()
        self.features.update(self.get_imperative_features())
        self.features["modal_count"] = self.count_modal_verbs()
        self.features["whitespace_ratio"] = get_whitespace_ratio(self.raw)
        self.features.update(get_wordcounts(flatten(self.sents_processed["tokens_stripped"])))
        self.features.update(get_punctuation_stats(self.raw))


    # HELPERS

    def __compute_sents_variations(self):
        stripped = []
        pos_tagged = []
        for sent in self.raw_sents:
            tokens = sent.split()

            stripped_tokens = [strip_surrounding_punctuation(token) for token in tokens if token != '']
            stripped_tokens = filter(None, stripped_tokens)     # remove any empty strings from list

            if len(stripped_tokens) > 0:
                stripped.append(stripped_tokens)

        preprocessed_comment = normalize_comment(self.raw)
        self.features.update(preprocessed_comment["features"])
        self.raw_preprocessed_comment = preprocessed_comment["normalized_comment"]
        preprocessed_sents = get_sents(self.raw_preprocessed_comment)
        preprocessed_sents = flatten(preprocessed_sents)

        for sent in preprocessed_sents:
            pos_tagged.append(get_tagged_sent(sent))


        return {"tokens_stripped": stripped, "normalized": preprocessed_sents, "pos_tagged": pos_tagged}



    # COMMENT TEXT REPRESENTATIONS (raw sents, tagged sents, preprocessed sents,....)



    def get_raw_sentences(self):
        return self.raw_sents

    def get_raw_preprocessed_comment(self):
        return self.raw_preprocessed_comment

    def get_sent_tokens_wo_punctuation(self):
        return self.sents_processed["tokens_stripped"]

    def get_POStagged_sents(self):
        return self.sents_processed["pos_tagged"]


    # NUMERIC REPRESENTATIONS of comment (amount of paragraphs, sentences, words,....)
    def count_paras(self):
        return self.cnt_paras

    def count_sents(self):
        return len(self.raw_sents)

    def get_features_dict(self):
        return self.features

    def get_subjectivity_features(self):
        sents = self.get_POStagged_sents()

        polarity = {"positive": 0.0, "negative": 0.0, "none": 0.0, "subj": 0.0}

        for sent in sents:
            subj_sent = get_subjectivity(sent)

            #polarity = {x: polarity.get(x, 0) + subj_sent.get(x, 0) for x in set(polarity).union(subj_sent)}
            for k in polarity:
                polarity[k] += subj_sent[k]
            #polarity = polarity + Counter(subj_sent)  # add dictionaries together

        return polarity

    def get_imperative_features(self):
        sents = self.get_POStagged_sents()
        imp = {"imperative_count": 0.0, "imperative_polite": 0.0, "imperative_indirect": 0.0, "imperative_strength": 0.0}

        for sent in sents:
            i = is_imperative(sent)  # {'imperative': Bool, 'polite': Bool, 'indirect': Bool, 'strength': Int}
            if i["imperative"]:
                imp["imperative_count"] += 1
                imp["imperative_polite"] += 1 if i['polite'] else 0
                imp["imperative_indirect"] += 1 if i['indirect'] else 0
                imp["imperative_strength"] += 1 if i['strength'] else 0

        if imp['imperative_count'] > 0:
            # ratio: number of imperative subtype / total number of imperative
            imp["imperative_polite"] /= imp["imperative_count"]
            imp["imperative_indirect"] /= imp["imperative_count"]
            imp["imperative_strength"] /= imp["imperative_count"]

        return imp

    def count_modal_verbs(self):
        sents = self.get_POStagged_sents()
        md_count = 0
        for sent in sents:
            mds = [1 for tup in sent if tup[1] == "MD"]
            md_count += len(mds)

        return md_count

    def count_ellipsis(self):   # Note: this could be done (more efficiently?) in normalize_ellipsis()
        sents = self.get_POStagged_sents()
        ellipsis_count = 0
        for sent in sents:
            ells = [1 for tup in sent if tup[0] == "..."]
            ellipsis_count += len(ells)

        return ellipsis_count




co = Comment("Would you stop that bullsh*t. .! \n$h1t can happen all the 71m3. N!99a!", "123")

print "\n---- FEATURES ----"
print co.features
print "\---------\n"
print co.get_POStagged_sents()

print co.get_subjectivity_features()

print co.get_sent_tokens_wo_punctuation()


def extract_features(text):
    comment = Comment(text)
