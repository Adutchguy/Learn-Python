def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _make(tmp_path):
    (tmp_path / "a.txt").write_text("hello")            # 5 bytes
    (tmp_path / "B.TXT").write_text("hi")                # 2 bytes
    (tmp_path / "photo.jpg").write_bytes(b"x" * 100)     # 100 bytes
    (tmp_path / "README").write_text("read me")          # 7 bytes
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "big.bin").write_bytes(b"x" * 500)
    (tmp_path / "sub" / "small.txt").write_text("1234")  # 4 bytes
    return tmp_path


def test_files_by_extension_groups_and_sorts(tmp_path):
    root = _make(tmp_path)
    result = _fn("files_by_extension")(root)
    want = {".txt": ["B.TXT", "a.txt"], ".jpg": ["photo.jpg"], "": ["README"]}
    assert result == want, f"Expected {want} but got {result}. Group by suffix.lower() and sort the names."


def test_files_by_extension_ignores_subfolders(tmp_path):
    root = _make(tmp_path)
    result = _fn("files_by_extension")(root)
    assert ".bin" not in result and "sub" not in [n for names in result.values() for n in names], (
        "Only files directly in the folder count. The sub folder and the files inside it should be ignored (use iterdir and is_file)."
    )


def test_big_files_searches_subfolders(tmp_path):
    root = _make(tmp_path)
    result = _fn("big_files")(root, 100)
    assert result == ["photo.jpg", "sub/big.bin"], f"Files of at least 100 bytes are photo.jpg and sub/big.bin but you returned {result}."


def test_big_files_with_a_small_limit_lists_every_file(tmp_path):
    root = _make(tmp_path)
    result = _fn("big_files")(root, 0)
    want = ["B.TXT", "README", "a.txt", "photo.jpg", "sub/big.bin", "sub/small.txt"]
    assert result == want, f"With a limit of 0 every file should be listed (not folders) in sorted order: {want} but you returned {result}."


def test_total_size_adds_up_all_files(tmp_path):
    root = _make(tmp_path)
    result = _fn("total_size")(root)
    assert result == 5 + 2 + 100 + 7 + 500 + 4, f"The files add up to 618 bytes (including the sub folder) but you returned {result}."


def test_total_size_of_an_empty_folder(tmp_path):
    result = _fn("total_size")(tmp_path)
    assert result == 0, f"An empty folder has size 0 but you returned {result}."


def test_copy_matching_copies_only_that_extension(tmp_path):
    root = _make(tmp_path)
    dst = tmp_path / "backup" / "texts"
    result = _fn("copy_matching")(root, dst, ".txt")
    assert result == ["B.TXT", "a.txt"], f"The copied names should be ['B.TXT', 'a.txt'] but you returned {result}."
    assert sorted(p.name for p in dst.iterdir()) == ["B.TXT", "a.txt"], "The files should exist in the destination folder (create it with mkdir(parents=True, exist_ok=True))."
    assert (dst / "a.txt").read_text() == "hello", "The copy should have the same contents."
    assert (root / "a.txt").exists(), "Copying should leave the original in place."
