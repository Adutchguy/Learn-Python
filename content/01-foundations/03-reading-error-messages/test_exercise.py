def test_program_runs_and_prints_the_right_lines(capsys):
    import exercise  # noqa: F401  (a bug in the learner's code shows up as an error right here)

    out = capsys.readouterr().out
    expected = "Starting the program\nHello, Ada\nHalf of 10 is 5.0\n"
    assert out == expected, (
        f"The program runs, but it should print:\n{expected}and it printed:\n{out}"
    )
