def _check_type(name, wanted, example):
    import exercise

    value = getattr(exercise, name)
    assert type(value) is wanted, (
        f"{name} should be a {wanted.__name__} (for example {example}), "
        f"but it holds {value!r}, which is a {type(value).__name__}."
    )


def test_whole_number_is_an_int():
    _check_type("whole_number", int, "7")


def test_decimal_number_is_a_float():
    _check_type("decimal_number", float, "2.5")


def test_text_is_a_str():
    _check_type("text", str, '"hello"')


def test_yes_or_no_is_a_bool():
    _check_type("yes_or_no", bool, "True")


def test_prints_the_type_of_42(capsys):
    import exercise  # noqa: F401

    out = capsys.readouterr().out
    assert out.strip() == "<class 'int'>", (
        f"Your program should print the type of 42, which is <class 'int'>. "
        f"Use print(type(42)). It printed {out!r}."
    )
