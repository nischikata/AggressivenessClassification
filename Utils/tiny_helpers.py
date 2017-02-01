flatten = lambda l: [item for sublist in l for item in sublist]


def get_text_label(num_label):
    if num_label == 0:
        return "not aggressive"
    else:
        return "aggressive"