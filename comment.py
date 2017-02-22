from __future__ import division
from Utils.text_mods import get_sents, strip_surrounding_punctuation, normalize_comment, separate_contractions
from Utils.stanford import get_tagged_sent
from Utils.tiny_helpers import flatten
from Features.Lexical.subjectivity import get_subjectivity
from Features.Grammatical.imperative import is_imperative
from Features.Other.counters import get_wordcounts, get_punctuation_stats, get_sent_counts, get_whitespace_ratio


class Comment:
    def __init__(self, raw_text, fileid):
        self.raw = raw_text     # raw ... 'unprocessed', unmodified
        self.fileid = fileid

        self.label = 1 if fileid[0] == 'a' else 0   # 1 ... aggressive, 0 ... not aggressive (extract from filepath)

        paras = get_sents(self.raw)
        self.paragraph_count = len(paras)
        self.raw_sents = flatten(paras)

        self.features = {"paras_count": self.paragraph_count}

        self.sents_processed = self.__compute_sents_variations()
        self.features.update(get_sent_counts(self.get_sent_tokens_wo_punctuation()))

        self.features.update(self.get_imperative_features())

        self.features["whitespace_ratio"] = get_whitespace_ratio(self.raw)
        self.features.update(get_wordcounts(flatten(self.sents_processed["tokens_stripped"])))

        self.features.update(self.get_posTag_features())

        self.features.update(self.get_subjectivity_features())
        self.features.update(get_punctuation_stats(self.raw))


    # HELPERS

    def __compute_sents_variations(self):
        stripped = []
        pos_tagged = []
        for sent in self.raw_sents:
            # replace m-dash with blank
            sent = sent.replace("--", " ")
            # remove dashes
            sent = sent.replace("-", "")
            # replace commas with blanks
            sent = sent.replace(",", " ")
            # replace slashes with blanks
            sent = sent.replace("/", " ")

            # replace common contractions but otherwise keep single quotes
            sent = separate_contractions(sent)

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
    def count_tokens(self):
        return self.features['word_count']

    def count_paras(self):
        return self.paragraph_count

    def count_sents(self):
        return len(self.get_sent_tokens_wo_punctuation())

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

        all = polarity['none'] + polarity['subj']
        subj_ratio = 0 if all == 0 else polarity['subj']/all
        subj_pos_ratio = 0 if all == 0 else polarity['positive']/all
        subj_neg_ratio = 0 if all == 0 else polarity['negative']/all

        return {'subj_ratio': subj_ratio, 'subj_pos_ratio': subj_pos_ratio, 'subj_neg_ratio': subj_neg_ratio}

    #def get_punctuation_style_features(self):
        # TODO get normalized


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


    def count_pos_tags(self):
        sents = self.get_POStagged_sents()
        tags = {}

        for sent in sents:
            for tup in sent:
                tag = tup[1]
                if tag not in tags:
                    tags[tag] = 1
                else:
                    tags[tag] += 1

        return tags


    def get_posTag_features(self):
        tags = self.count_pos_tags()

        jjr_ratio = jjs_ratio = rbr_ratio = rbs_ratio = md_ratio = present_ratio = past_ratio = 0

        # ADJECTIVES
        jj = 0 if 'JJ' not in tags else tags['JJ']
        jjr = 0 if 'JJR' not in tags else tags['JJR']   # comparative adjective
        jjs = 0 if 'JJS' not in tags else tags['JJS']   # superlative

        adj = jj + jjr + jjs

        if adj > 0:
            jjr_ratio = jjr/adj
            jjs_ratio = jjs/adj


        # ADVERBS
        rb = 0 if 'RB' not in tags else tags['RB']
        rbr = 0 if 'RBR' not in tags else tags['RBR']   # comparative adverb
        rbs = 0 if 'RBS' not in tags else tags['RBS']   # superlative adverb

        adv = rb + rbr + rbs

        if adv > 0:
            rbr_ratio = rbr/adv
            rbs_ratio = rbs/adv

        # VERBS
        vb = 0 if 'VB' not in tags else tags['VB']      # base form verb
        vbd = 0 if 'VBD' not in tags else tags['VBD']   # past tense verb
        vbg = 0 if 'VBG' not in tags else tags['VBG']   # gerund or present participle verb
        vbn = 0 if 'VBN' not in tags else tags['VBN']   # past participle verb
        vbz = 0 if 'VBZ' not in tags else tags['VBZ']   # 3rd person singular present verb
        vbp = 0 if 'VBP' not in tags else tags['VBP']   # non-3rd person singular present verb
        md = 0 if 'MD' not in tags else tags['MD']   # modal verb

        verbs = vb + vbd + vbg + vbn + vbz + vbp + md

        if verbs > 0:
            md_ratio = md/verbs
            present_ratio = (vb + vbg + vbp + vbz)/verbs
            past_ratio = (vbd + vbn)/verbs

        # POS TAG DIVERSITY
        # how many different POS tags are there in relation to the number of tokens?
        pos_type_ratio = len(tags)/self.count_tokens()

        # WH-PRONOUNS
        # how many wh-pronouns are in the comment?
        wh_question = 0 if 'WRB' not in tags else tags['WRB']            # Why, Where, When, How
        wh_question = wh_question if 'WP' not in tags else tags['WP']    # What, Who, Whoever
        wh_question = wh_question if 'WDT' not in tags else tags['WDT']  # Which, Whatever


        return { "pos_type_ratio": pos_type_ratio, "JJR_ratio": jjr_ratio, "JJS_ratio": jjs_ratio,
                 "RBR_ratio": rbr_ratio, "RBS_ratio": rbs_ratio, "modal_count": md, "modal_ratio": md_ratio,
                 "present_ratio": present_ratio, "past_ratio": past_ratio, "wh_pronouns": wh_question}



    def count_ellipsis(self):   # Note: this could be done (more efficiently?) in normalize_ellipsis()
        sents = self.get_POStagged_sents()
        ellipsis_count = 0
        for sent in sents:
            ells = [1 for tup in sent if tup[0] == "..."]
            ellipsis_count += len(ells)

        return ellipsis_count

    def get_label(self):
        """
        :return: 0 or 1
        """
        return self.label

    def get_category(self):
        return 'not aggressive' if self.label == 0 else 'aggressive'

# P R I N T I N G

    def print_feature_dict(self):

        print "\n\n------------------------------------" \
              "\n {:<29} {:10}" \
              "\n------------------------------------".format("FEATURE", "VALUE")

        for key, value in sorted(self.features.items()):
            print " {:<25} {:10.4f}".format(key, value)

        print "------------------------------------\n"


    def print_normalized_sents(self):
        print "\n---------NORMALIZED SENTENCES-------------------------------------------------------------"
        for sent in self.sents_processed["normalized"]:
            print "  ", sent
        print "------------------------------------------------------------------------------------------\n"


    def print_POStagged_sents(self):
        print "\n---------POS TAGGED SENTENCES-------------------------------------------------------------"
        for sent in self.sents_processed["pos_tagged"]:
            print "  ", sent
        print "------------------------------------------------------------------------------------------\n"


    def print_sent_tokens_stripped(self):
        print "\n---------NORMALIZED TOKENS PER SENTENCE---------------------------------------------------"
        for sent in self.sents_processed["tokens_stripped"]:
            print "  ", sent
        print "------------------------------------------------------------------------------------------\n"


    def print_original_sents(self):
        print "\n---------ORIGINAL SENTENCES---------------------------------------------------------------"
        for sent in self.raw_sents:
            print "  ", sent
        print "------------------------------------------------------------------------------------------\n"
