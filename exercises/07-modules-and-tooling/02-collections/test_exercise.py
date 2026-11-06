def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_top_words():
    top_words = _fn("top_words")
    text = "the cat and the dog and the bird"
    assert top_words(text, 2) == [("the", 3), ("and", 2)], f"top_words(..., 2) should be [('the', 3), ('and', 2)] but was {top_words(text, 2)!r}."


def test_top_words_ignores_capitals():
    top_words = _fn("top_words")
    assert top_words("The the THE a", 1) == [("the", 3)], f"top_words('The the THE a', 1) should be [('the', 3)] but was {top_words('The the THE a', 1)!r}. Lower-case the text first."


def test_top_words_asking_for_more_than_exist():
    top_words = _fn("top_words")
    assert top_words("a b a", 10) == [("a", 2), ("b", 1)], f"Asking for more words than exist should return all of them, but got {top_words('a b a', 10)!r}."


def test_group_by_length():
    group_by_length = _fn("group_by_length")
    result = group_by_length(["a", "bb", "cc", "d", "eee"])
    assert result == {1: ["a", "d"], 2: ["bb", "cc"], 3: ["eee"]}, f"Expected {{1: ['a', 'd'], 2: ['bb', 'cc'], 3: ['eee']}} but got {result!r}."
    assert group_by_length([]) == {}, "No words should give an empty dictionary."


def test_group_by_length_returns_a_plain_dict():
    group_by_length = _fn("group_by_length")
    result = group_by_length(["a"])
    assert type(result) is dict, f"Return an ordinary dict (use dict(groups)) but you returned a {type(result).__name__}."


def test_rotate_right_and_left():
    rotate = _fn("rotate")
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3], f"rotate([1, 2, 3, 4, 5], 2) should be [4, 5, 1, 2, 3] but was {rotate([1, 2, 3, 4, 5], 2)!r}."
    assert rotate([1, 2, 3, 4, 5], -1) == [2, 3, 4, 5, 1], f"rotate([1, 2, 3, 4, 5], -1) should be [2, 3, 4, 5, 1] but was {rotate([1, 2, 3, 4, 5], -1)!r}."


def test_rotate_edge_cases_and_original_unchanged():
    rotate = _fn("rotate")
    assert rotate([], 3) == [], "Rotating an empty list gives an empty list."
    original = [1, 2, 3]
    result = rotate(original, 1)
    assert isinstance(result, list), f"rotate should return a list but returned {type(result).__name__}."
    assert original == [1, 2, 3], f"rotate must not change the list it is given, but it is now {original!r}."
