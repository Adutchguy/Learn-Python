def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


CSV_TEXT = "name,score\nAda,90\nBo,55\nCy,70\n"


def _make(tmp_path, text=CSV_TEXT):
    path = tmp_path / "scores.csv"
    path.write_text(text)
    return path


def test_load_students(tmp_path):
    result = _fn("load_students")(_make(tmp_path))
    want = [("Ada", 90), ("Bo", 55), ("Cy", 70)]
    assert result == want, f"load_students should return {want!r} (scores as ints) but returned {result!r}."


def test_load_students_with_a_comma_in_a_name(tmp_path):
    path = _make(tmp_path, 'name,score\n"Doe, Jo",64\n')
    result = _fn("load_students")(path)
    assert result == [("Doe, Jo", 64)], f"A quoted name containing a comma should stay in one piece. Got {result!r}. Use the csv module rather than split(',')."


def test_class_average(tmp_path):
    result = _fn("class_average")(_make(tmp_path))
    assert abs(result - 71.6666) < 0.01, f"class_average should return about 71.67 but returned {result!r}."


def test_save_passed_keeps_the_header_and_the_right_rows(tmp_path):
    source = _make(tmp_path)
    destination = tmp_path / "passed.csv"
    _fn("save_passed")(source, destination, 70)
    text = destination.read_text().replace("\r\n", "\n")
    assert text == "name,score\nAda,90\nCy,70\n", f"passed.csv should contain the header plus Ada and Cy (70 counts as a pass) but contains {text!r}."


def test_save_passed_when_nobody_passes(tmp_path):
    source = _make(tmp_path)
    destination = tmp_path / "none.csv"
    _fn("save_passed")(source, destination, 100)
    text = destination.read_text().replace("\r\n", "\n")
    assert text == "name,score\n", f"With nobody passing the file should contain only the header but contains {text!r}."


def test_source_file_is_unchanged(tmp_path):
    source = _make(tmp_path)
    _fn("save_passed")(source, tmp_path / "out.csv", 80)
    assert source.read_text() == CSV_TEXT, "save_passed must not change the source file."
