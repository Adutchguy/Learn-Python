def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_find_numbers():
    result = _fn("find_numbers")("3 cats and 12 dogs")
    assert result == [3, 12], f"find_numbers('3 cats and 12 dogs') should return [3, 12] but returned {result!r}."


def test_find_numbers_none_and_long():
    find_numbers = _fn("find_numbers")
    assert find_numbers("no digits here") == [], f"find_numbers('no digits here') should return [] but returned {find_numbers('no digits here')!r}."
    assert find_numbers("room 404, floor 7") == [404, 7], f"find_numbers('room 404, floor 7') should return [404, 7] but returned {find_numbers('room 404, floor 7')!r}."


def test_find_hashtags():
    result = _fn("find_hashtags")("I love #python and #coding!")
    assert result == ["python", "coding"], f"find_hashtags should return ['python', 'coding'] but returned {result!r}."


def test_find_hashtags_with_underscores_and_none():
    find_hashtags = _fn("find_hashtags")
    assert find_hashtags("#learn_python rocks") == ["learn_python"], f"find_hashtags('#learn_python rocks') should return ['learn_python'] but returned {find_hashtags('#learn_python rocks')!r}."
    assert find_hashtags("no tags") == [], f"find_hashtags('no tags') should return [] but returned {find_hashtags('no tags')!r}."


def test_parse_date():
    result = _fn("parse_date")("2026-11-06")
    assert result == (2026, 11, 6), f"parse_date('2026-11-06') should return (2026, 11, 6) but returned {result!r}."


def test_parse_date_rejects_other_text():
    parse_date = _fn("parse_date")
    for text in ["tomorrow", "2026-1-6", "06-11-2026", "2026-11-06 extra", ""]:
        assert parse_date(text) is None, f"parse_date({text!r}) should return None but returned {parse_date(text)!r}."
