def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import os


def test_copy_text(tmp_path):
    copy_text = _fn("copy_text")
    src, dst = tmp_path / "a.txt", tmp_path / "b.txt"
    src.write_text("line one\nline two\n")
    copy_text(str(src), str(dst))
    assert dst.exists(), "copy_text should create the destination file."
    assert dst.read_text() == "line one\nline two\n", f"The copy should hold the same text but holds {dst.read_text()!r}."
    assert src.read_text() == "line one\nline two\n", "The source file must stay unchanged."


def test_working_in_changes_and_restores_the_directory(tmp_path, monkeypatch):
    working_in = _fn("working_in")
    monkeypatch.chdir(tmp_path)  # remembered, and restored when the check ends
    inner = tmp_path / "inner"
    inner.mkdir()
    before = os.getcwd()
    with working_in(str(inner)):
        now = os.path.realpath(os.getcwd())
        assert now == os.path.realpath(str(inner)), f"Inside the block the current folder should be {inner} but it is {now}."
    assert os.getcwd() == before, f"After the block the current folder should be back to {before} but it is {os.getcwd()}."


def test_working_in_restores_after_an_error(tmp_path, monkeypatch):
    import pytest

    working_in = _fn("working_in")
    monkeypatch.chdir(tmp_path)
    inner = tmp_path / "inner"
    inner.mkdir()
    before = os.getcwd()
    with pytest.raises(RuntimeError):
        with working_in(str(inner)):
            raise RuntimeError("boom")
    assert os.getcwd() == before, "The folder must be restored even when the block raises an error. Put the chdir back in a finally clause."


def test_log_block_records_start_and_end():
    log_block = _fn("log_block")
    lines = []
    with log_block("load", lines):
        lines.append("working")
    assert lines == ["start load", "working", "end load"], f"lines should be ['start load', 'working', 'end load'] but are {lines!r}."


def test_log_block_ends_even_after_an_error():
    import pytest

    log_block = _fn("log_block")
    lines = []
    with pytest.raises(ValueError):
        with log_block("risky", lines):
            raise ValueError("bad")
    assert lines == ["start risky", "end risky"], f"lines should be ['start risky', 'end risky'] but are {lines!r}. Put the 'end' line in a finally clause."
