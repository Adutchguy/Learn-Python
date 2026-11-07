def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _file(tmp_path, count=8):
    path = tmp_path / "notes.txt"
    path.write_text("\n".join(f"line {i}" for i in range(1, count + 1)) + "\n")
    return path


def test_parser_defaults():
    args = _fn("build_parser")().parse_args(["notes.txt"])
    assert args.path == "notes.txt", f"args.path should be 'notes.txt' but is {args.path!r}."
    assert args.limit == 5, f"The default for --limit should be 5 but is {args.limit!r}."
    assert args.verbose is False, f"--verbose should be False when it is not given but is {args.verbose!r}. Use action='store_true'."


def test_parser_reads_options():
    args = _fn("build_parser")().parse_args(["data.csv", "-n", "3", "--verbose"])
    assert args.limit == 3 and isinstance(args.limit, int), f"-n 3 should give the whole number 3 (use type=int) but gave {args.limit!r}."
    assert args.verbose is True, "Giving -v or --verbose should set verbose to True."
    args = _fn("build_parser")().parse_args(["data.csv", "--limit", "7", "-v"])
    assert args.limit == 7 and args.verbose is True, "The long names --limit and --verbose should work as well as -n and -v."


def test_parser_requires_a_path():
    import pytest

    with pytest.raises(SystemExit):
        _fn("build_parser")().parse_args([])


def test_parser_rejects_a_non_number_limit():
    import pytest

    with pytest.raises(SystemExit):
        _fn("build_parser")().parse_args(["notes.txt", "-n", "lots"])


def test_main_prints_the_first_lines(tmp_path, capsys):
    path = _file(tmp_path)
    code = _fn("main")([str(path), "-n", "3"])
    out = capsys.readouterr().out
    assert out == "line 1\nline 2\nline 3\n", f"main should print the first 3 lines but printed {out!r}."
    assert code == 0, f"main should return 0 on success but returned {code!r}."


def test_main_default_limit_is_five(tmp_path, capsys):
    path = _file(tmp_path)
    _fn("main")([str(path)])
    out = capsys.readouterr().out
    assert out.splitlines() == [f"line {i}" for i in range(1, 6)], f"Without -n it should print 5 lines but printed {out.splitlines()}."


def test_main_verbose_announces_the_file(tmp_path, capsys):
    path = _file(tmp_path, count=2)
    _fn("main")([str(path), "--verbose"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == f"Reading {path}", f"With --verbose the first line should be 'Reading {path}' but is {lines[0]!r}."
    assert lines[1:] == ["line 1", "line 2"], f"After that come the file's lines but you printed {lines[1:]}."


def test_main_reports_a_missing_file_on_stderr(tmp_path, capsys):
    code = _fn("main")([str(tmp_path / "nope.txt")])
    captured = capsys.readouterr()
    assert code == 1, f"For a missing file main should return 1 but returned {code!r}."
    assert captured.out == "", f"Nothing should go to normal output for an error but this did: {captured.out!r}. Print errors with file=sys.stderr."
    assert captured.err.strip() != "", "Print an error message to standard error (print(..., file=sys.stderr))."
