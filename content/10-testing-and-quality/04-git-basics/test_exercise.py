def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import shutil

import pytest

if shutil.which("git") is None:
    pytest.skip("Git is not installed on this computer: install it from git-scm.com, then run this lesson again.", allow_module_level=True)


def test_start_repo_creates_a_repository(tmp_path):
    start_repo = _fn("start_repo")
    repo = tmp_path / "project"
    start_repo(repo)
    assert (repo / ".git").is_dir(), "start_repo should create the folder and run git init, so a .git folder exists"


def test_commit_file_and_history_newest_first(tmp_path):
    start_repo, commit_file, history = _fn("start_repo"), _fn("commit_file"), _fn("history")
    repo = tmp_path / "r"
    start_repo(repo)
    commit_file(repo, "notes.txt", "one\n", "Add notes")
    commit_file(repo, "notes.txt", "one\ntwo\n", "Add a second line")
    assert history(repo) == ["Add a second line", "Add notes"], f"history should list messages newest first, got {history(repo)!r}"
    assert (repo / "notes.txt").read_text() == "one\ntwo\n", "commit_file should write the new text to the file"


def test_history_of_an_empty_repository_is_empty(tmp_path):
    start_repo, history = _fn("start_repo"), _fn("history")
    repo = tmp_path / "empty"
    start_repo(repo)
    assert history(repo) == [], "a repository with no commits has an empty history ([]), not an error"


def test_uncommitted_lists_changed_and_new_files(tmp_path):
    start_repo, commit_file, uncommitted = _fn("start_repo"), _fn("commit_file"), _fn("uncommitted")
    repo = tmp_path / "work"
    start_repo(repo)
    assert uncommitted(repo) == [], "a fresh repository has nothing uncommitted"
    commit_file(repo, "a.txt", "1\n", "Add a")
    commit_file(repo, "b.txt", "1\n", "Add b")
    assert uncommitted(repo) == [], "after committing everything, nothing is uncommitted"
    (repo / "a.txt").write_text("changed\n")
    (repo / "c.txt").write_text("new\n")
    assert uncommitted(repo) == ["a.txt", "c.txt"], f"a modified file and a new file should be listed (sorted), got {uncommitted(repo)!r}"
