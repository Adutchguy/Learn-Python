def _run(monkeypatch, capsys, *typed):
    """Run the learner's game, typing `typed` one guess at a time; return its output lines."""
    values = iter(typed)

    def fake_input(prompt=""):
        try:
            return next(values)
        except StopIteration:
            raise EOFError(
                "Your game asked for another guess after the test had finished guessing. "
                "Does it stop when the guess is right, and after 7 guesses?"
            )

    monkeypatch.setattr("builtins.input", fake_input)
    import exercise  # noqa: F401

    return capsys.readouterr().out.splitlines()


def _check(monkeypatch, capsys, guesses, expected):
    out = _run(monkeypatch, capsys, *guesses)
    assert out == expected, (
        f"For the guesses {', '.join(guesses)} your game should print:\n"
        + "\n".join(expected)
        + "\nbut it printed:\n"
        + "\n".join(out)
    )


def test_win_on_the_first_guess(monkeypatch, capsys):
    _check(monkeypatch, capsys, ["42"], ["Correct! Guesses used: 1"])


def test_too_high_then_too_low_then_correct(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["50", "25", "42"],
        ["Too high!", "Too low!", "Correct! Guesses used: 3"],
    )


def test_game_ends_when_the_guess_is_right(monkeypatch, capsys):
    # More guesses are available, but the game must not ask for them once the number is found.
    _check(monkeypatch, capsys, ["10", "42"], ["Too low!", "Correct! Guesses used: 2"])


def test_win_on_the_seventh_and_last_guess(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["1", "2", "3", "4", "5", "6", "42"],
        ["Too low!"] * 6 + ["Correct! Guesses used: 7"],
    )


def test_out_of_guesses(monkeypatch, capsys):
    _check(
        monkeypatch,
        capsys,
        ["1", "2", "3", "4", "5", "6", "99"],
        ["Too low!"] * 6 + ["Too high!", "Out of guesses! The number was 42."],
    )
