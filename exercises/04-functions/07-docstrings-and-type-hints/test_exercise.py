def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _hints(func):
    return func.__annotations__


def test_bmi_still_works():
    result = _fn("bmi")(70, 1.75)
    assert abs(result - 22.857) < 0.01, f"bmi(70, 1.75) should still return about 22.86 but returned {result!r}."


def test_bmi_has_a_docstring():
    doc = (_fn("bmi").__doc__ or "").strip()
    assert len(doc) >= 10, "bmi needs a docstring: put a sentence in triple quotes on the first line inside the function."


def test_bmi_has_type_hints():
    hints = _hints(_fn("bmi"))
    assert hints.get("weight") is float and hints.get("height") is float, (
        f"bmi's parameters should be hinted as float (weight: float, height: float). Found {hints!r}."
    )
    assert hints.get("return") is float, f"bmi should be hinted to return a float (-> float). Found {hints!r}."


def test_to_fahrenheit():
    func = _fn("to_fahrenheit")
    assert func(100) == 212.0, f"to_fahrenheit(100) should return 212.0 but returned {func(100)!r}."
    assert func(0) == 32.0, f"to_fahrenheit(0) should return 32.0 but returned {func(0)!r}."
    assert func(-40) == -40.0, f"to_fahrenheit(-40) should return -40.0 but returned {func(-40)!r}."


def test_to_fahrenheit_has_a_docstring():
    doc = (_fn("to_fahrenheit").__doc__ or "").strip()
    assert len(doc) >= 10, "to_fahrenheit needs a docstring: put a sentence in triple quotes on the first line inside the function."


def test_to_fahrenheit_has_type_hints():
    hints = _hints(_fn("to_fahrenheit"))
    assert hints.get("celsius") is float and hints.get("return") is float, (
        f"to_fahrenheit should be hinted celsius: float and -> float. Found {hints!r}."
    )
