def test_prints_the_greeting(capsys):
    import exercise  # noqa: F401  (running the learner's program prints the greeting)

    out = capsys.readouterr().out
    assert out == "Hello, Python!\n", (
        f"Expected your program to print Hello, Python! on one line, "
        f"but it printed {out!r}."
    )
