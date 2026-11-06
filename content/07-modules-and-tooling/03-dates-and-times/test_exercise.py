def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


from datetime import date


def test_days_until():
    days_until = _fn("days_until")
    assert days_until(date(2024, 3, 1), date(2024, 3, 15)) == 14, f"From 1 March to 15 March is 14 days but you returned {days_until(date(2024, 3, 1), date(2024, 3, 15))!r}."
    assert days_until(date(2024, 3, 1), date(2024, 3, 1)) == 0, "The same day is 0 days away."
    assert days_until(date(2024, 3, 10), date(2024, 3, 7)) == -3, "A target in the past gives a negative number."
    assert days_until(date(2024, 2, 28), date(2024, 3, 1)) == 2, "2024 is a leap year, so 28 February to 1 March is 2 days."


def test_days_until_returns_a_whole_number():
    days_until = _fn("days_until")
    result = days_until(date(2024, 3, 1), date(2024, 3, 15))
    assert isinstance(result, int), f"days_until should return an int, but returned {result!r}. Use the .days attribute of the timedelta."


def test_format_date():
    format_date = _fn("format_date")
    assert format_date(date(2024, 3, 5)) == "05 March 2024", f"format_date(date(2024, 3, 5)) should be '05 March 2024' but was {format_date(date(2024, 3, 5))!r}."
    assert format_date(date(1999, 12, 31)) == "31 December 1999", f"format_date(date(1999, 12, 31)) should be '31 December 1999' but was {format_date(date(1999, 12, 31))!r}."


def test_parse_date():
    parse_date = _fn("parse_date")
    result = parse_date("2024-03-05")
    assert result == date(2024, 3, 5), f"parse_date('2024-03-05') should be date(2024, 3, 5) but was {result!r}."
    assert type(result) is date, f"parse_date should return a date, not a {type(result).__name__}. Use .date() on the result of strptime."


def test_parse_date_rejects_other_formats():
    import pytest

    parse_date = _fn("parse_date")
    with pytest.raises(ValueError):
        parse_date("05/03/2024")


def test_add_business_days_over_a_weekend():
    add_business_days = _fn("add_business_days")
    assert add_business_days(date(2024, 3, 8), 1) == date(2024, 3, 11), f"One business day after Friday 8 March 2024 is Monday 11 March but you returned {add_business_days(date(2024, 3, 8), 1)!r}."
    assert add_business_days(date(2024, 3, 4), 5) == date(2024, 3, 11), f"Five business days after Monday 4 March is Monday 11 March but you returned {add_business_days(date(2024, 3, 4), 5)!r}."


def test_add_business_days_edge_cases():
    add_business_days = _fn("add_business_days")
    assert add_business_days(date(2024, 3, 6), 0) == date(2024, 3, 6), "Adding 0 business days returns the same date."
    assert add_business_days(date(2024, 3, 9), 1) == date(2024, 3, 11), f"One business day after Saturday 9 March is Monday 11 March but you returned {add_business_days(date(2024, 3, 9), 1)!r}."
    assert add_business_days(date(2024, 3, 6), 2) == date(2024, 3, 8), "Two business days after Wednesday 6 March is Friday 8 March."
