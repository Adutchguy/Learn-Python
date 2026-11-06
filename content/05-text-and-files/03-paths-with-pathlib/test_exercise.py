def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


from pathlib import Path


def test_notes_path(tmp_path):
    result = _fn("notes_path")(tmp_path, "todo")
    assert isinstance(result, Path), f"notes_path should return a Path object but returned {result!r}."
    assert result == tmp_path / "todo.txt", f"notes_path(folder, 'todo') should be folder / 'todo.txt' but was {result!r}."


def test_notes_path_accepts_text_folders(tmp_path):
    result = _fn("notes_path")(str(tmp_path), "ideas")
    assert result == tmp_path / "ideas.txt", f"notes_path should also work when the folder is given as text. Got {result!r}."


def test_list_text_files(tmp_path):
    for name in ["b.txt", "a.txt", "data.csv", "c.txt"]:
        (tmp_path / name).write_text("x")
    result = _fn("list_text_files")(tmp_path)
    assert result == ["a.txt", "b.txt", "c.txt"], f"list_text_files should return ['a.txt', 'b.txt', 'c.txt'] but returned {result!r}."


def test_list_text_files_empty_folder(tmp_path):
    result = _fn("list_text_files")(tmp_path)
    assert result == [], f"list_text_files of a folder with no .txt files should return [] but returned {result!r}."


def test_copy_text(tmp_path):
    source = tmp_path / "in.txt"
    source.write_text("hello\nworld\n")
    destination = tmp_path / "out.txt"
    _fn("copy_text")(source, destination)
    assert destination.read_text() == "hello\nworld\n", f"The copy should contain the same text. It contains {destination.read_text()!r}."
    assert source.read_text() == "hello\nworld\n", "copy_text should leave the source file as it was."


def test_copy_text_into_a_new_folder(tmp_path):
    source = tmp_path / "in.txt"
    source.write_text("data")
    destination = tmp_path / "backup" / "in.txt"
    _fn("copy_text")(source, destination)
    assert destination.exists(), "copy_text should create the destination folder (backup) when it does not exist yet."
    assert destination.read_text() == "data", f"The copy should contain 'data' but contains {destination.read_text()!r}."
