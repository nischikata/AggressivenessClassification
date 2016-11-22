from Features.Grammatical.imperative import is_imperative
import pytest

# def test_polite():
#     assert is_imperative("Please be quiet.")["polite"] == True


# PARAMETRIZED TESTS:
# http://docs.pytest.org/en/latest/parametrize.html

@pytest.mark.parametrize("test_input,expected", [
    ("Shut up!", True),
    ("You be quiet now!", True),
    ("That's enough!", False),
    ("Do you know him?", False),
    ("Would you just look at this beautiful book?!", False),
])
def test_imperative(test_input, expected):
    assert is_imperative(test_input)["imperative"] == expected


@pytest.mark.parametrize("polite_input, expected_politeness", [
    ("Please be quiet.", True),
    ("Have a seat, please.", True),
    ("Be quiet, will you?", False),
    ("Do sit down.", True),
    ("Do you know him.", False),
])

def test_polite(polite_input, expected_politeness):
    assert is_imperative(polite_input)["polite"] == expected_politeness
