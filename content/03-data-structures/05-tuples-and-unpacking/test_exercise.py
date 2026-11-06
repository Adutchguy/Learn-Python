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


def test_three_people(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["Ada Bo Cy", "90 85 70"],
        ["Ada: 90", "Bo: 85", "Cy: 70", "Best: Ada (90)"],
    )


def test_winner_is_not_first(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["Dee Eli Fay", "55 91 78"],
        ["Dee: 55", "Eli: 91", "Fay: 78", "Best: Eli (91)"],
    )


def test_single_person(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["Zoe", "100"], ["Zoe: 100", "Best: Zoe (100)"])


def test_scores_compare_as_numbers_not_text(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["Al Bea", "9 100"],
        ["Al: 9", "Bea: 100", "Best: Bea (100)"],
    )
