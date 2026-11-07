def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import sys


def test_run_returns_code_and_output():
    code, out = _fn("run")([sys.executable, "-c", "print('hi')"])
    assert code == 0, f"A program that succeeds has return code 0 but you returned {code!r}."
    assert out == "hi\n", f"The captured output should be 'hi\\n' but is {out!r}. Use capture_output=True and text=True."


def test_run_reports_failure_without_raising():
    code, out = _fn("run")([sys.executable, "-c", "raise SystemExit(3)"])
    assert code == 3, f"The child exits with status 3, so run should return 3 but returned {code!r}."


def test_python_version_text():
    text = _fn("python_version")()
    want = "Python " + sys.version.split()[0]
    assert text == want, f"python_version() should return {want!r} but returned {text!r}."


def test_run_or_none_returns_output():
    result = _fn("run_or_none")([sys.executable, "-c", "print(40 + 2)"], 10)
    assert result == "42", f"The program prints 42, so run_or_none should return '42' but returned {result!r}."


def test_run_or_none_gives_up_on_a_slow_program():
    result = _fn("run_or_none")([sys.executable, "-c", "import time; time.sleep(5)"], 0.3)
    assert result is None, "A program that outlasts the timeout should give None. Catch subprocess.TimeoutExpired."


def test_run_or_none_handles_a_missing_program():
    result = _fn("run_or_none")(["this-program-does-not-exist-12345"], 5)
    assert result is None, "A program that does not exist should give None. Catch FileNotFoundError."


def test_echo_safely_treats_text_as_text():
    nasty = "x; echo INJECTED && $(whoami) `id`"
    result = _fn("echo_safely")(nasty)
    assert result == nasty, f"The text should come back exactly as given but came back as {result!r}. Pass it as its own list item."


def test_echo_safely_keeps_spaces():
    result = _fn("echo_safely")("two  spaces")
    assert result == "two  spaces", f"Spaces inside the text must survive, but you got {result!r}."
