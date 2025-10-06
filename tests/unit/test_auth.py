from simplechat.auth import NAMES_ADJECTIVE, NAMES_NOUN, handle_generate_random_name


def test_adjective_noun_length():
    """
    GIVEN lists of adjectives and nouns
    WHEN every combination is generated
    THEN ensure all entries are strings of appropriate length
    """
    for adjective in NAMES_ADJECTIVE:
        for noun in NAMES_NOUN:
            name = f"{adjective} {noun}"
            assert isinstance(name, str)
            assert len(name) > 3
            assert len(name) < 32


def test_generate_random_name():
    """
    GIVEN a random name generation function
    WHEN the function is called
    THEN check that a string is returned within the expected length
    """
    random_name = handle_generate_random_name()
    assert len(random_name) > 3
    assert len(random_name) < 32
    assert isinstance(random_name, str)
