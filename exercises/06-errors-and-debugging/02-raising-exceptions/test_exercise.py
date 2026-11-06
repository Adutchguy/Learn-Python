def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import pytest


def test_validate_age_accepts_good_values():
    validate_age = _fn("validate_age")
    for age in [0, 35, 150]:
        assert validate_age(age) == age, f"validate_age({age}) should return {age}."


def test_validate_age_rejects_wrong_type():
    validate_age = _fn("validate_age")
    with pytest.raises(TypeError) as info:
        validate_age("35")
    assert "whole number" in str(info.value), f"The TypeError message should say the age must be a whole number, but it was {str(info.value)!r}."


def test_validate_age_rejects_out_of_range():
    validate_age = _fn("validate_age")
    for age in [-1, 151]:
        with pytest.raises(ValueError) as info:
            validate_age(age)
        assert "between 0 and 150" in str(info.value), f"validate_age({age}) should raise ValueError('age must be between 0 and 150') but the message was {str(info.value)!r}."


def test_out_of_stock_is_an_exception_type():
    import exercise

    assert hasattr(exercise, "OutOfStock"), "Define your own error with: class OutOfStock(Exception):"
    assert isinstance(exercise.OutOfStock, type) and issubclass(exercise.OutOfStock, Exception), "OutOfStock must be a class that inherits from Exception: class OutOfStock(Exception):"


def test_take_reduces_stock():
    take = _fn("take")
    stock = {"apple": 5}
    assert take(stock, "apple", 2) == 3, "take({'apple': 5}, 'apple', 2) should return 3."
    assert stock == {"apple": 3}, f"take should also update the dictionary, which is now {stock!r}."
    assert take(stock, "apple") == 2, "The quantity defaults to 1."


def test_take_raises_out_of_stock_with_a_clear_message():
    import exercise

    take = _fn("take")
    with pytest.raises(exercise.OutOfStock) as info:
        take({"apple": 2}, "apple", 5)
    assert str(info.value) == "only 2 apple left, wanted 5", f"The message should be 'only 2 apple left, wanted 5' but it was {str(info.value)!r}."
    with pytest.raises(exercise.OutOfStock):
        take({}, "pear")


def test_parse_percent_valid():
    parse_percent = _fn("parse_percent")
    assert parse_percent("45%") == 45, f"parse_percent('45%') should return 45 but returned {parse_percent('45%')!r}."
    assert parse_percent("0%") == 0 and parse_percent("100%") == 100, "0% and 100% are both allowed."


def test_parse_percent_malformed():
    parse_percent = _fn("parse_percent")
    for text in ["45", "abc%", "%", "4.5%"]:
        with pytest.raises(ValueError) as info:
            parse_percent(text)
        assert str(info.value) == f"not a percentage: {text!r}", f"parse_percent({text!r}) should raise ValueError('not a percentage: {text!r}') but the message was {str(info.value)!r}."


def test_parse_percent_out_of_range():
    parse_percent = _fn("parse_percent")
    with pytest.raises(ValueError) as info:
        parse_percent("150%")
    assert str(info.value).startswith("percentage out of range"), f"parse_percent('150%') should raise a ValueError starting with 'percentage out of range' but the message was {str(info.value)!r}."
