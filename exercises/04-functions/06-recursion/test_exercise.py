def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _check(name, argument, expected):
    result = _fn(name)(argument)
    assert result == expected, f"{name}({argument}) should return {expected} but returned {result!r}."


def test_factorial():
    _check("factorial", 5, 120)


def test_factorial_of_zero_and_one():
    _check("factorial", 0, 1)
    _check("factorial", 1, 1)


def test_factorial_of_ten():
    _check("factorial", 10, 3628800)


def test_sum_digits():
    _check("sum_digits", 493, 16)


def test_sum_digits_of_a_single_digit_and_zero():
    _check("sum_digits", 7, 7)
    _check("sum_digits", 0, 0)


def test_fibonacci_start():
    for n, expected in [(0, 0), (1, 1), (2, 1), (3, 2)]:
        _check("fibonacci", n, expected)


def test_fibonacci_further_on():
    _check("fibonacci", 7, 13)
    _check("fibonacci", 15, 610)


def test_functions_really_use_recursion():
    import exercise

    for name in ("factorial", "sum_digits", "fibonacci"):
        code = getattr(exercise, name).__code__
        assert name in code.co_names, f"{name} should call itself (recursion), but it never refers to {name}."
