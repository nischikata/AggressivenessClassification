import pytest
import Features.Other.counters as count


# TODO: break up this large test into smaller pieces
@pytest.mark.parametrize("test_input, expected", [
    ("...?", None),
    ("You're so persecuted! Oh my!", {'ttr': 1, 'all_caps_count': {'count_all': 0, 'one_char_count': 0}, 'mixed_case_word_count': 0, 'noise_count': 0, 'one_char_token_count': 0, 'max_wordlength': 10, 'num_count': 0, 'word_count': 6, 'median_wordlength': 2.0, 'average_wordlength': 3.5, 'long_words_count': 1}),
    ("A 3 year old can calculate better than you!", {'ttr': 1, 'all_caps_count': {'count_all': 1, 'one_char_count': 1}, 'mixed_case_word_count': 0, 'noise_count': 0, 'one_char_token_count': 1, 'max_wordlength': 9, 'num_count': 1, 'word_count': 8, 'median_wordlength': 3.5, 'average_wordlength': 4.125, 'long_words_count': 1}),
    ("$hit.", {'ttr': 1, 'all_caps_count': {'count_all': 0, 'one_char_count': 0}, 'mixed_case_word_count': 0, 'noise_count': 1, 'median_wordlength': 4.0, 'long_words_count': 0, 'word_count': 1, 'one_char_token_count': 0, 'max_wordlength': 4, 'num_count': 0, 'average_wordlength': 4.0})
])
def test_get_wordcounts(test_input, expected):
    assert count.get_wordcounts(test_input) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("Hello World!", 0),
    ("HeLoO world!", 1),
    ("hello world!", 0),
    ("hE77o wORDL!", 2),
])
def test_mixed_case_words(test_input, expected):
    assert count.get_wordcounts(test_input)["mixed_case_word_count"] == expected


@pytest.mark.parametrize("test_input, expected", [
    ("Hello World!", 0),
    ("$HIT!", 1),
    ("$ H I T!", 0),
    ("hE77o wORDL!", 1),
    ("SH*T", 1)
])
def test_noise_words(test_input, expected):
    assert count.get_wordcounts(test_input)["noise_count"] == expected


@pytest.mark.parametrize("test_input, expected", [
    ("Hello World!", {'count_all': 0, 'one_char_count': 0}),
    ("T H I S   is   S T U P I D.", {'count_all': 10, 'one_char_count': 10}),
    ("THIS IS stupID!", {'count_all': 2, 'one_char_count': 0}),
])
def test_allcaps(test_input, expected):
    assert count.get_wordcounts(test_input)["all_caps_count"] == expected


@pytest.mark.parametrize("test_input, expected", [
    ("Hello hello!", 0.5),
    ("This is a test, test, TEST!", 2/3.0),       # 4/6
])
def test_ttr(test_input, expected):
    assert count.get_wordcounts(test_input)["ttr"] == expected


@pytest.mark.parametrize("test_input, expected", [
    ("Hello hello!", 1),
    ("Hello! How are you? What's your name? Nice to meet you!!", 4),
    ("Hey... What's up?", 1)# 4/6
])
def test_count_sents(test_input, expected):
    assert count.count_sents(test_input) == expected
