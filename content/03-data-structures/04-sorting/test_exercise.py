def _run(monkeypatch, capsys, *typed):
    """Run the learner's program, typing `typed` one value at a time; return what it printed."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError("Your program asked for more input than expected. Keep the input() lines as they are.")

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.strip()


def _check(monkeypatch, capsys, typed, expected):
    out = _run(monkeypatch, capsys, *typed)
    want = "\n".join(expected)
    assert out == want, (
        f"With the input {list(typed)!r} your program should print:\n{want}\n\nbut it printed:\n{out}"
    )


def test_mixed_case_names(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["bob alice Carol dave"],
        ["Sorted: alice, bob, Carol, dave", "By length: bob, dave, alice, Carol", "Reverse: dave, Carol, bob, alice"],
    )


def test_capitals_do_not_jump_the_queue(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["Zed amy Bo"],
        ["Sorted: amy, Bo, Zed", "By length: Bo, Zed, amy", "Reverse: Zed, Bo, amy"],
    )


def test_single_name(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["Sam"], ["Sorted: Sam", "By length: Sam", "Reverse: Sam"])
