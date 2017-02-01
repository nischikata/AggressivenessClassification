from Utils.dictionaries import in_regularDict, in_urbanDict
from Features.Lexical.politness import is_polite
from Features.Lexical.blacklist import is_blacklisted

def get_lexical_features(token, feature_dict):
    """
    checks whether the given token is in a regular dictionary, the urban dictionary, blacklisted
    or in the polite words list
    :param token: expects a token without punctuation; ignores numeric values
    :param feature_dict: must look like this {"no_dict": 0, "in_dict": 0, "urbdict_only": 0, "blacklist": 0, "polite": 0}
    :return:
    >>> get_lexical_features("shit", {'blacklist': 0, 'urbdict_only': 0, 'in_dict': 1, 'polite': 0, 'no_dict': 11})
    {'blacklist': 1, 'urbdict_only': 0, 'no_dict': 11, 'polite': 0, 'in_dict': 2}

    >>> get_lexical_features("300", {'blacklist': 0, 'urbdict_only': 0, 'no_dict': 0, 'polite': 0, 'in_dict': 0})
    {'blacklist': 0, 'urbdict_only': 0, 'in_dict': 0, 'polite': 0, 'no_dict': 0}
    """
    if not any(c.isalpha() for c in token):
        return feature_dict


    if in_regularDict(token):
        feature_dict["in_dict"] += 1
    elif in_urbanDict(token):
        feature_dict["urbdict_only"] += 1
        feature_dict["in_dict"] += 1    #in_dict simply means it is in either dict: regular, urban or both
    else:
        feature_dict["no_dict"] += 1

    if is_polite(token):
        feature_dict["polite"] += 1

    if is_blacklisted(token):
        feature_dict["blacklist"] += 1

    return feature_dict
