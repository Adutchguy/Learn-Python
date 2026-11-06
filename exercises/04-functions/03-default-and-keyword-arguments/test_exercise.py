def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_power_default():
    result = _fn("power")(3)
    assert result == 9, f"power(3) should return 9 (the default exponent is 2) but returned {result!r}."


def test_power_with_exponent():
    result = _fn("power")(2, 10)
    assert result == 1024, f"power(2, 10) should return 1024 but returned {result!r}."


def test_power_with_keyword():
    result = _fn("power")(exponent=3, base=2)
    assert result == 8, f"power(exponent=3, base=2) should return 8 but returned {result!r}."


def test_join_words_default_separator():
    result = _fn("join_words")("a", "b", "c")
    assert result == "a b c", f"join_words('a', 'b', 'c') should return 'a b c' but returned {result!r}."


def test_join_words_with_separator():
    result = _fn("join_words")("a", "b", "c", sep="-")
    assert result == "a-b-c", f"join_words('a', 'b', 'c', sep='-') should return 'a-b-c' but returned {result!r}."


def test_join_words_with_one_word_or_none():
    join_words = _fn("join_words")
    assert join_words("solo") == "solo", f"join_words('solo') should return 'solo' but returned {join_words('solo')!r}."
    assert join_words() == "", f"join_words() with no words should return '' but returned {join_words()!r}."


def test_profile_with_details():
    result = _fn("profile")("Ada", city="London", age=36)
    assert result == "Ada (age=36, city=London)", (
        f"profile('Ada', city='London', age=36) should return 'Ada (age=36, city=London)' but returned {result!r}."
    )


def test_profile_without_details():
    result = _fn("profile")("Ada")
    assert result == "Ada", f"profile('Ada') should return 'Ada' but returned {result!r}."
