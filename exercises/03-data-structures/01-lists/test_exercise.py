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


def test_eggs_are_removed(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["milk eggs bread"], ["First: milk", "Last: apples", "Items: 3"])


def test_no_eggs_to_remove(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["milk bread"], ["First: milk", "Last: apples", "Items: 3"])


def test_only_eggs(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["eggs"], ["First: apples", "Last: apples", "Items: 1"])


def test_eggs_first(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["eggs tea coffee"], ["First: tea", "Last: apples", "Items: 3"])
