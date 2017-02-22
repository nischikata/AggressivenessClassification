flatten = lambda l: [item for sublist in l for item in sublist]


def get_text_label(num_label):
    if num_label == 0:
        return "not aggressive"
    else:
        return "aggressive"


def is_number_or_monetary(s):
    if len(s) > 1 and s[0] == '$':
        s = s[1:]
    try:
        float(s)
        return True
    except ValueError:
        return False