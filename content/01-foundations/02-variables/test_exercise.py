def test_total_variable_exists():
    import exercise

    assert hasattr(exercise, "total"), (
        "Your program should create a variable called total. "
        "Write a line that starts with: total = "
    )


def test_total_has_the_right_value():
    import exercise

    assert hasattr(exercise, "total"), "Create a variable called total first."
    expected = exercise.price * exercise.quantity
    assert exercise.total == expected, (
        f"total should be price * quantity = {expected}, but it is {exercise.total!r}."
    )


def test_total_is_printed(capsys):
    import exercise

    out = capsys.readouterr().out
    assert out.strip() == "15.0", (
        f"Your program should print the total (15.0), but it printed {out!r}."
    )
