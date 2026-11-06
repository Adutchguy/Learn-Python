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


def test_mixed_numbers(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["5 3 8 2"], ["Total: 18", "Largest: 8", "Evens: 2"])


def test_no_evens(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["1 3 5"], ["Total: 9", "Largest: 5", "Evens: 0"])


def test_one_number(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["7"], ["Total: 7", "Largest: 7", "Evens: 0"])


def test_negative_numbers(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["-4 -10 6"], ["Total: -8", "Largest: 6", "Evens: 3"])
