from __future__ import division
import numpy
from comment import Comment
# extract features for a single comment:



def get_feature_vector(comment):
    """
    Returns the feature vector for the given Comment
    :param comment: Comment object
    :return: numpy array
    """

    c_features = comment.get_features_dict()

    feature_list = []

    as_is = ['exclamation_ratio', 'period_ratio', 'questionmark_ratio', 'whitespace_ratio', 'highlighters_count',
             'paras_count', 'sent_count', 'word_count', 'ttr', 'max_wordlength', 'average_wordlength',
             'median_wordlength','spaced_words_count', 'edit_distance', 'lengthening_counts', 'longest_sent_len',
             'avg_sent_len', 'median_sent_len', 'shortest_sent_len', 'subj_ratio', 'subj_pos_ratio',
             'subj_neg_ratio', 'mdash_count', 'pos_type_ratio', 'JJR_ratio', 'JJS_ratio', 'RBR_ratio',
             'RBS_ratio', 'modal_ratio', 'present_ratio', 'past_ratio', 'rep_punc_len_avg']

    per_sent = ['sent_endings_count', 'ellipsis_count', 'modal_count', 'imperative_count', 'one_char_token_count',
                'connectors_count', 'wh_pronouns', 'rep_punc_count']

    per_tokens = ['no_dict', 'urbdict_only', 'in_dict', 'polite', 'blacklist', 'noise_count', 'all_caps_count',
                  'long_words_count', 'modified_tokens_count', 'mixed_case_word_count', 'num_count']

    per_imperatives = ['imperative_indirect', 'imperative_strength', 'imperative_polite']

    for f in as_is:
        feature_list.append(c_features[f])

    for f in per_sent:
        if c_features['sent_count'] > 0:
            feature_list.append(c_features[f]/c_features['sent_count'])
        else:
            # TODO throw exception, this should never happen!
            feature_list.append(0)

    for f in per_tokens:
        if c_features['word_count'] > 0:
            feature_list.append(c_features[f]/c_features['word_count'])
        else:
            # TODO throw exception, this should never happen!
            feature_list.append(0)

    for f in per_imperatives:
        if c_features['imperative_count'] > 0:
            feature_list.append(c_features[f]/c_features['imperative_count'])
        else:
            # this might actually happen, thats ok
            feature_list.append(0)

    return numpy.array(feature_list)

"""

#co = Comment("NO TRUMP IS NOT A THREAT TO AMERICA BUT A CROOKED PAPER LIKE NYT SURE IS AND IT'S EDITOR IS A BIG ONESIDED JACKASS WHO WILL NOT BE IN BUSINES I HOPE AND PRAY TOO MUCH LONGER BECAUSE INSTEAD OF BEING HONEST AND NETURAL & UNBIAS EDITOR FOR THE PAPER FOR WHAT IT SHOULD BE IS IN REALITY A PART OF THE ILLUMINATE ONE WORLD GLOBIST SATAN WORSHIIPERS GROUP MEMBER WITH THE CLINTONS, SOROS, OBAMA, REID. NANCY P. THE BUSHES, ROTHSCHILD AND THE REST OF THEM THAT KILLED THE JUDGE AND FOSTER AND MANY MORE PEOPLE I HOPE I GET TO SEE ALL OF YOU STAND TRIAL FOR TREASON AGAINST WE THE PEOPLE AND OUR COUNTRY. I HOPE GOD GIVES US THIS CHANCE TO SEE YOU SATAN PEOPLE DROP IN SATAN'S FIRE HOLE. AND WE TAKE OUR COUNTRY BACK AND OUR GOD.", "123")
co = Comment("YOUR @$$ IS FAT!!!! YO!!?", "1")
get_feature_vector(co)
print co.get_raw_preprocessed_comment()
print co.get_POStagged_sents()

print "fileid   ", co.fileid

co.print_feature_dict()
co.print_normalized_sents()
co.print_POStagged_sents()
co.print_sent_tokens_stripped()
co.print_original_sents()

"""