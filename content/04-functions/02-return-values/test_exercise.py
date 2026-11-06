def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_average():
    result = _fn("average")([2, 4, 9])
    assert result == 5.0, f"average([2, 4, 9]) should return 5.0 but returned {result!r}."


def test_average_of_one():
    result = _fn("average")([7])
    assert result == 7.0, f"average([7]) should return 7.0 but returned {result!r}."


def test_clamp_too_high():
    result = _fn("clamp")(15, 0, 10)
    assert result == 10, f"clamp(15, 0, 10) should return 10 but returned {result!r}."


def test_clamp_too_low():
    result = _fn("clamp")(-3, 0, 10)
    assert result == 0, f"clamp(-3, 0, 10) should return 0 but returned {result!r}."


def test_clamp_inside_the_range():
    result = _fn("clamp")(4, 0, 10)
    assert result == 4, f"clamp(4, 0, 10) should return 4 but returned {result!r}."


def test_min_max():
    result = _fn("min_max")([4, 1, 7])
    assert result == (1, 7), f"min_max([4, 1, 7]) should return (1, 7) but returned {result!r}."


def test_functions_return_rather_than_print(capsys):
    _fn("average")([1, 2])
    _fn("clamp")(1, 0, 5)
    _fn("min_max")([1, 2])
    out = capsys.readouterr().out
    assert out == "", f"These functions should return their answers, not print them, but something was printed: {out!r}."
