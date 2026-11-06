def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import functools


def test_fib_values():
    fib = _fn("fib")
    assert [fib(n) for n in range(8)] == [0, 1, 1, 2, 3, 5, 8, 13], f"fib(0..7) should be 0, 1, 1, 2, 3, 5, 8, 13, got {[fib(n) for n in range(8)]!r}"


def test_fib_is_cached_and_fast():
    fib = _fn("fib")
    assert hasattr(fib, "cache_info"), "decorate fib with @functools.cache so it remembers answers"
    assert fib(90) == 2880067194370816120, "fib(90) should be 2880067194370816120 (this finishes instantly only with caching)"
    assert fib.cache_info().hits > 0, "the cache should have been used (hits > 0)"


def test_square_and_cube_are_partials():
    import exercise

    for name, exponent in (("square", 2), ("cube", 3)):
        func = getattr(exercise, name, None)
        assert func is not None, f"define {name} with functools.partial(power, exp={exponent})"
        assert isinstance(func, functools.partial), f"{name} should be made with functools.partial"
        assert func(4) == 4 ** exponent, f"{name}(4) should be {4 ** exponent}, got {func(4)!r}"
        assert func.keywords == {"exp": exponent}, f"{name} should fix exp={exponent}, but its fixed keywords are {func.keywords!r}"


def test_product():
    product = _fn("product")
    assert product([2, 3, 4]) == 24, f"product([2, 3, 4]) should be 24, got {product([2, 3, 4])!r}"
    assert product([5]) == 5, "the product of one number is that number"
    assert product([]) == 1, "the product of no numbers is 1 (give reduce a starting value)"
    assert product([2, 0, 9]) == 0, "anything times zero is zero"
