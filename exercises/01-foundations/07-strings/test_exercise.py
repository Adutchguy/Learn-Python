def _run(monkeypatch, capsys, typed):
    """Run the learner's program as if the user had typed `typed`; return what it printed."""
    monkeypatch.setattr("builtins.input", lambda prompt="": typed)
    import exercise  # noqa: F401

    return capsys.readouterr().out


def _check(monkeypatch, capsys, typed, expected):
    out = _run(monkeypatch, capsys, typed)
    assert out == expected, (
        f"For the input {typed!r} your program should print:\n{expected}but it printed:\n{out}"
    )


def test_messy_name(monkeypatch, capsys):
    _check(monkeypatch, capsys, "  aDa LoVElace  ", "Ada Lovelace\nLength: 12\n")


def test_lowercase_name(monkeypatch, capsys):
    _check(monkeypatch, capsys, "grace hopper", "Grace Hopper\nLength: 12\n")


def test_trailing_space(monkeypatch, capsys):
    _check(monkeypatch, capsys, "alan turing ", "Alan Turing\nLength: 11\n")


def test_single_word(monkeypatch, capsys):
    _check(monkeypatch, capsys, "  LINUS", "Linus\nLength: 5\n")
