def test_lucky_number_is_3():
    import exercise

    assert exercise.lucky_number == 3, (
        f"lucky_number should be 3, but it is {exercise.lucky_number!r}. "
        "Change the 0 on the line lucky_number = 0 to a 3."
    )


def test_program_prints_the_right_lines(capsys):
    import exercise  # noqa: F401

    out = capsys.readouterr().out
    expected = "I am learning Python.\nMy lucky number is 3\n"
    assert out == expected, (
        f"Expected your program to print:\n{expected}but it printed:\n{out}"
    )
