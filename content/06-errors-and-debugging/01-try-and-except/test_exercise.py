def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_to_int_converts_valid_text():
    to_int = _fn("to_int")
    assert to_int("42") == 42, f"to_int('42') should return 42 but returned {to_int('42')!r}."
    assert to_int(" 7 ") == 7, f"to_int(' 7 ') should return 7 (int() ignores spaces) but returned {to_int(' 7 ')!r}."


def test_to_int_uses_the_default_for_bad_text():
    to_int = _fn("to_int")
    for text in ["abc", "", "3.5"]:
        assert to_int(text) == 0, f"to_int({text!r}) should return the default 0 but returned {to_int(text)!r}."
    assert to_int("x", default=-1) == -1, "to_int('x', default=-1) should return -1."
    assert to_int("x", -5) == -5, "to_int('x', -5) should return -5: the default can be given by position too."


def test_to_int_only_catches_value_errors():
    import pytest

    to_int = _fn("to_int")
    with pytest.raises(TypeError):
        to_int(None)


def test_safe_divide():
    safe_divide = _fn("safe_divide")
    assert safe_divide(10, 4) == 2.5, f"safe_divide(10, 4) should be 2.5 but was {safe_divide(10, 4)!r}."
    assert safe_divide(0, 5) == 0, "safe_divide(0, 5) should be 0."
    assert safe_divide(1, 0) is None, f"safe_divide(1, 0) should return None but returned {safe_divide(1, 0)!r}."


def test_get_age_valid_and_missing():
    get_age = _fn("get_age")
    assert get_age({"age": "42"}) == 42, f"get_age({{'age': '42'}}) should return 42 but returned {get_age({'age': '42'})!r}."
    assert get_age({"name": "Ada"}) == "unknown", "A dictionary with no 'age' key should give 'unknown'."


def test_get_age_invalid_values():
    get_age = _fn("get_age")
    assert get_age({"age": "abc"}) == "invalid", "get_age({'age': 'abc'}) should give 'invalid' (ValueError)."
    assert get_age({"age": None}) == "invalid", "get_age({'age': None}) should give 'invalid' (int(None) raises TypeError, which you must catch too)."
