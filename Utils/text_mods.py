from string import punctuation
# Text modification module

def replace_dont(string_sent):
    """
    >>> sent = "Don't do it."
    >>> replace_dont(sent)
    'Do not do it.'
    >>>
    >>> sent = "Please don't do it."
    >>> replace_dont(sent)
    'Please do not do it.'
    """
    i = string_sent.lower().find("don't")
    return string_sent[:i] + string_sent[i:].replace("on't", "o not", 1)  # only replace the first occurrence


#tinas_punctuation = '!"\'()-./:;?[\\]`'

def strip_punctuation(string_text, punc = punctuation):
    return ''.join(c for c in string_text if c not in punc)


