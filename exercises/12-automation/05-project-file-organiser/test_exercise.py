def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


from pathlib import Path


def _messy(tmp_path):
    for name in ("cat.JPG", "notes.txt", "report.pdf", "backup.zip", "mystery.xyz", "noext"):
        (tmp_path / name).write_text(name)
    (tmp_path / "old_folder").mkdir()
    return tmp_path


def test_category_for_known_types():
    category = _fn("category_for")
    want = {
        "a.jpg": "Images", "b.JPEG": "Images", "c.png": "Images", "d.gif": "Images",
        "e.pdf": "Documents", "f.txt": "Documents", "g.md": "Documents", "h.docx": "Documents",
        "i.zip": "Archives", "j.tar": "Archives", "k.gz": "Archives",
    }
    for name, expected in want.items():
        assert category(name) == expected, f"category_for({name!r}) should be {expected!r} but returned {category(name)!r}."


def test_category_for_everything_else_is_other():
    category = _fn("category_for")
    for name in ("mystery.xyz", "README", "archive.tar.bz2x"):
        assert category(name) == "Other", f"category_for({name!r}) should be 'Other' but returned {category(name)!r}."


def test_unique_destination_returns_a_free_path_unchanged(tmp_path):
    path = tmp_path / "photo.jpg"
    assert _fn("unique_destination")(path) == path, "If nothing exists at the path it should be returned unchanged."


def test_unique_destination_finds_the_next_free_number(tmp_path):
    (tmp_path / "photo.jpg").write_text("1")
    assert _fn("unique_destination")(tmp_path / "photo.jpg") == tmp_path / "photo (1).jpg", "When photo.jpg exists the answer should be 'photo (1).jpg'."
    (tmp_path / "photo (1).jpg").write_text("2")
    assert _fn("unique_destination")(tmp_path / "photo.jpg") == tmp_path / "photo (2).jpg", "When photo (1).jpg exists too the answer should be 'photo (2).jpg'."


def test_plan_moves_lists_files_only_in_order(tmp_path):
    root = _messy(tmp_path)
    plan = _fn("plan_moves")(root)
    names = [source.name for source, _ in plan]
    assert names == ["backup.zip", "cat.JPG", "mystery.xyz", "noext", "notes.txt", "report.pdf"], (
        f"The plan should list the 6 files (not the folder), sorted by name, but lists {names}."
    )
    assert dict((s.name, d) for s, d in plan)["cat.JPG"] == root / "Images" / "cat.JPG", "cat.JPG should be planned for folder / 'Images' / 'cat.JPG'."
    assert all(isinstance(s, Path) and isinstance(d, Path) for s, d in plan), "Both parts of each pair should be Path objects."


def test_plan_moves_does_not_touch_anything(tmp_path):
    root = _messy(tmp_path)
    _fn("plan_moves")(root)
    assert sorted(p.name for p in root.iterdir()) == sorted(["cat.JPG", "notes.txt", "report.pdf", "backup.zip", "mystery.xyz", "noext", "old_folder"]), (
        "plan_moves only plans: it must not create folders or move files."
    )


def test_organise_moves_the_files(tmp_path):
    root = _messy(tmp_path)
    lines = _fn("organise")(root)
    assert lines == [
        "backup.zip -> Archives", "cat.JPG -> Images", "mystery.xyz -> Other",
        "noext -> Other", "notes.txt -> Documents", "report.pdf -> Documents",
    ], f"The returned lines are not what was expected: {lines}"
    assert (root / "Images" / "cat.JPG").read_text() == "cat.JPG", "cat.JPG should now be inside the Images folder."
    assert (root / "Documents" / "notes.txt").exists() and (root / "Archives" / "backup.zip").exists() and (root / "Other" / "mystery.xyz").exists(), "Every file should be inside its category folder."
    assert not (root / "cat.JPG").exists(), "The file should have been moved, not copied."
    assert (root / "old_folder").is_dir(), "Existing folders must be left alone."


def test_organise_never_overwrites(tmp_path):
    root = tmp_path
    (root / "Images").mkdir()
    (root / "Images" / "cat.jpg").write_text("old")
    (root / "cat.jpg").write_text("new")
    _fn("organise")(root)
    assert (root / "Images" / "cat.jpg").read_text() == "old", "The existing file must not be overwritten."
    assert (root / "Images" / "cat (1).jpg").read_text() == "new", "The moved file should get the free name 'cat (1).jpg'."


def test_organise_dry_run_changes_nothing(tmp_path):
    root = _messy(tmp_path)
    lines = _fn("organise")(root, dry_run=True)
    assert len(lines) == 6 and lines[1] == "cat.JPG -> Images", f"A dry run should still report the plan, but returned {lines}."
    assert not (root / "Images").exists(), "A dry run must not create folders."
    assert (root / "cat.JPG").exists(), "A dry run must not move files."


def test_main_prints_lines_and_a_summary(tmp_path, capsys):
    root = _messy(tmp_path)
    code = _fn("main")([str(root)])
    lines = capsys.readouterr().out.splitlines()
    assert code == 0, f"main should return 0 but returned {code!r}."
    assert lines[-1] == "6 file(s) moved", f"The last line should be '6 file(s) moved' but is {lines[-1]!r}."
    assert "cat.JPG -> Images" in lines, "main should print each line from organise."
    assert (root / "Images" / "cat.JPG").exists(), "main should really move the files."


def test_main_dry_run(tmp_path, capsys):
    root = _messy(tmp_path)
    _fn("main")([str(root), "--dry-run"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[-1] == "6 file(s) would be moved", f"A dry run should end with '6 file(s) would be moved' but ends with {lines[-1]!r}."
    assert (root / "cat.JPG").exists() and not (root / "Images").exists(), "With --dry-run nothing may be moved."
