from Utils.text_mods import replace_dont

def test_dont():
    assert replace_dont("You don't do it right.") == 'You do not do it right.'