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


def test_repeated_word(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["The cat the"], ["cat: 1", "the: 2", "Unique words: 2"])


def test_all_different(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["one two three"],
        ["one: 1", "three: 1", "two: 1", "Unique words: 3"],
    )


def test_capitals_are_ignored(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["Go go GO"], ["go: 3", "Unique words: 1"])


def test_longer_sentence(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["to be or not to be"],
        ["be: 2", "not: 1", "or: 1", "to: 2", "Unique words: 4"],
    )
