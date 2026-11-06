def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _printed(capsys, name, *args):
    capsys.readouterr()
    _fn(name)(*args)
    return capsys.readouterr().out


def test_greet(capsys):
    out = _printed(capsys, "greet", "Ada")
    assert out == "Hello, Ada!\n", f"greet('Ada') should print 'Hello, Ada!' but printed {out!r}."


def test_greet_uses_its_parameter(capsys):
    out = _printed(capsys, "greet", "Zed")
    assert out == "Hello, Zed!\n", f"greet('Zed') should print 'Hello, Zed!' but printed {out!r}."


def test_banner(capsys):
    out = _printed(capsys, "banner", "Hello")
    want = "=========\n| Hello |\n=========\n"
    assert out == want, f"banner('Hello') should print:\n{want}but printed:\n{out}"


def test_banner_adjusts_to_the_text(capsys):
    out = _printed(capsys, "banner", "Hi")
    want = "======\n| Hi |\n======\n"
    assert out == want, f"banner('Hi') should print:\n{want}but printed:\n{out}"
