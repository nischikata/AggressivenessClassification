from __future__ import division
import numpy
from Utils.comment import Comment
# extract features for a single comment:

FEATURE_NAMES = ['as_is___exclamation_ratio', 'as_is___long_words_count', 'as_is___wh_pronouns' ,'as_is___ellipsis_count', 'as_is___period_ratio', 'as_is___questionmark_ratio', 'as_is___whitespace_ratio', 'as_is___highlighters_count', 'as_is___paras_count', 'as_is___sent_count', 'as_is___word_count', 'as_is___ttr', 'as_is___max_wordlength', 'as_is___average_wordlength', 'as_is___median_wordlength', 'as_is___spaced_words_count', 'as_is___edit_distance', 'as_is___lengthening_counts', 'as_is___longest_sent_len', 'as_is___avg_sent_len', 'as_is___median_sent_len', 'as_is___shortest_sent_len', 'as_is___subj_ratio', 'as_is___subj_pos_ratio', 'as_is___subj_neg_ratio', 'as_is___mdash_count', 'as_is___pos_type_ratio', 'as_is___JJR_ratio', 'as_is___JJS_ratio', 'as_is___RBR_ratio', 'as_is___RBS_ratio', 'as_is___modal_ratio', 'as_is___present_ratio', 'as_is___past_ratio', 'as_is___rep_punc_len_avg', 'as_is___non_alphanum_ratio', 'as_is___blacklist_CAPS', 'as_is___mixed_case_word_count', 'as_is___noise_count', 'as_is___urbdict_only', 'as_is___blacklist', 'as_is___no_dict', 'as_is___modified_tokens_count', 'as_is___in_dict', 'as_is___polite', 'as_is___imperative_count', 'per_sent___sent_endings_count', 'per_sent___ellipsis_count', 'per_sent___modal_count', 'per_sent___imperative_count', 'per_sent___one_char_token_count', 'per_sent___connectors_count', 'per_sent___wh_pronouns', 'per_sent___rep_punc_count', 'per_sent___paras_count', 'per_sent___urbdict_only', 'per_sent___blacklist', 'per_sent___no_dict', 'per_tokens___no_dict', 'per_tokens___urbdict_only', 'per_tokens___blacklist', 'per_tokens___all_caps_count', 'per_tokens___long_words_count', 'per_tokens___modified_tokens_count', 'per_tokens___num_count', 'per_imperatives___imperative_indirect', 'per_imperatives___imperative_strength', 'per_imperatives___imperative_polite']

def get_feature_names():
    return FEATURE_NAMES

def print_features():
    for i, f in enumerate(get_feature_names()):
        print i, "...", f


def get_feature_vector(comment):
    """
    Returns the feature vector for the given Comment
    :param comment: Comment object
    :return: numpy array
    """

    c_features = comment.get_features_dict()

    feature_list = []
    

    as_is = ['exclamation_ratio', 'long_words_count', 'wh_pronouns', 'ellipsis_count', 'period_ratio', 'questionmark_ratio', 'whitespace_ratio', 'highlighters_count',
             'paras_count', 'sent_count', 'word_count', 'ttr', 'max_wordlength', 'average_wordlength',
             'median_wordlength','spaced_words_count', 'edit_distance', 'lengthening_counts', 'longest_sent_len',
             'avg_sent_len', 'median_sent_len', 'shortest_sent_len', 'subj_ratio', 'subj_pos_ratio',
             'subj_neg_ratio', 'mdash_count', 'pos_type_ratio', 'JJR_ratio', 'JJS_ratio', 'RBR_ratio',
             'RBS_ratio', 'modal_ratio', 'present_ratio', 'past_ratio', 'rep_punc_len_avg', 'non_alphanum_ratio',
             'blacklist_CAPS', 'mixed_case_word_count', 'noise_count', 'urbdict_only', 'blacklist',  
             'no_dict', 'modified_tokens_count', 'in_dict', 'polite', 'imperative_count']

    per_sent = ['sent_endings_count', 'ellipsis_count', 'modal_count', 'imperative_count', 'one_char_token_count',
                'connectors_count', 'wh_pronouns', 'rep_punc_count', 'paras_count', 'urbdict_only', 'blacklist', 'no_dict'] 

    per_tokens = ['no_dict', 'urbdict_only', 'blacklist', 'all_caps_count',
                  'long_words_count', 'modified_tokens_count', 'num_count']

    per_imperatives = ['imperative_indirect', 'imperative_strength', 'imperative_polite']

    for f in as_is:
        feature_list.append(c_features[f])
        #feature_names.append("as_is___" + f)
        
    for f in per_sent:
        if c_features['sent_count'] > 0:
            feature_list.append(c_features[f]/c_features['sent_count'])
        else:
            # TODO throw exception, this should never happen!
            feature_list.append(0)
        
        #feature_names.append("per_sent___" + f)

    for f in per_tokens:
        if c_features['word_count'] > 0:
            feature_list.append(c_features[f]/c_features['word_count'])
        else:
            # TODO throw exception, this should never happen!
            feature_list.append(0)
        
        #feature_names.append("per_tokens___" + f)

    for f in per_imperatives:
        if c_features['imperative_count'] > 0:
            feature_list.append(c_features[f]/c_features['imperative_count'])
        else:
            # this might actually happen, thats ok
            feature_list.append(0)
        
        #feature_names.append("per_imperatives___" + f)
    
    return numpy.array(feature_list) #, feature_names
    

"""
#    TEST AREA: 
co = Comment("Hey what's up?", "1")
get_feature_vector(co)

print co.get_raw_preprocessed_comment()
print co.get_POStagged_sents()

print "fileid   ", co.fileid

co.print_feature_dict()
co.print_normalized_sents()
co.print_POStagged_sents()
co.print_sent_tokens_stripped()
co.print_original_sents()

FEATURE NAMES:
['as_is___exclamation_ratio', 'as_is___period_ratio', 'as_is___questionmark_ratio', 'as_is___whitespace_ratio', 'as_is___highlighters_count', 'as_is___paras_count', 'as_is___sent_count', 'as_is___word_count', 'as_is___ttr', 'as_is___max_wordlength', 'as_is___average_wordlength', 'as_is___median_wordlength', 'as_is___spaced_words_count', 'as_is___edit_distance', 'as_is___lengthening_counts', 'as_is___longest_sent_len', 'as_is___avg_sent_len', 'as_is___median_sent_len', 'as_is___shortest_sent_len', 'as_is___subj_ratio', 'as_is___subj_pos_ratio', 'as_is___subj_neg_ratio', 'as_is___mdash_count', 'as_is___pos_type_ratio', 'as_is___JJR_ratio', 'as_is___JJS_ratio', 'as_is___RBR_ratio', 'as_is___RBS_ratio', 'as_is___modal_ratio', 'as_is___present_ratio', 'as_is___past_ratio', 'as_is___rep_punc_len_avg', 'as_is___non_alphanum_ratio', 'as_is___blacklist_CAPS', 'as_is___mixed_case_word_count', 'as_is___noise_count', 'as_is___urbdict_only', 'as_is___blacklist', 'as_is___no_dict', 'as_is___modified_tokens_count', 'as_is___in_dict', 'as_is___polite', 'per_sent___sent_endings_count', 'per_sent___ellipsis_count', 'per_sent___modal_count', 'per_sent___imperative_count', 'per_sent___one_char_token_count', 'per_sent___connectors_count', 'per_sent___wh_pronouns', 'per_sent___rep_punc_count', 'per_sent___paras_count', 'per_sent___urbdict_only', 'per_sent___blacklist', 'per_sent___no_dict', 'per_tokens___no_dict', 'per_tokens___urbdict_only', 'per_tokens___blacklist', 'per_tokens___all_caps_count', 'per_tokens___long_words_count', 'per_tokens___modified_tokens_count', 'per_tokens___num_count', 'per_imperatives___imperative_indirect', 'per_imperatives___imperative_strength', 'per_imperatives___imperative_polite']

"""
