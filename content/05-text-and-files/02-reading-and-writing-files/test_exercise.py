def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_save_lines_writes_one_line_each(tmp_path):
    path = tmp_path / "notes.txt"
    _fn("save_lines")(path, ["alpha", "beta", "gamma"])
    text = path.read_text()
    assert text == "alpha\nbeta\ngamma\n", f"save_lines should write each line followed by a newline. The file contains {text!r}."


def test_save_lines_replaces_old_content(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("old stuff\n")
    _fn("save_lines")(path, ["new"])
    text = path.read_text()
    assert text == "new\n", f"save_lines should replace the old content. The file contains {text!r}."


def test_load_lines(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("one\ntwo\nthree\n")
    result = _fn("load_lines")(path)
    assert result == ["one", "two", "three"], f"load_lines should return ['one', 'two', 'three'] (no newlines) but returned {result!r}."


def test_load_lines_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("")
    result = _fn("load_lines")(path)
    assert result == [], f"load_lines of an empty file should return [] but returned {result!r}."


def test_append_line_keeps_existing_content(tmp_path):
    path = tmp_path / "log.txt"
    path.write_text("first\n")
    _fn("append_line")(path, "second")
    text = path.read_text()
    assert text == "first\nsecond\n", f"append_line should add to the end and keep 'first'. The file contains {text!r}."


def test_append_line_creates_the_file(tmp_path):
    path = tmp_path / "new.txt"
    _fn("append_line")(path, "hello")
    text = path.read_text()
    assert text == "hello\n", f"append_line should create a missing file. The file contains {text!r}."


def test_round_trip(tmp_path):
    path = tmp_path / "round.txt"
    lines = ["a b c", "", "last"]
    _fn("save_lines")(path, lines)
    result = _fn("load_lines")(path)
    assert result == lines, f"Saving {lines!r} and loading it back should give the same list but gave {result!r}."
