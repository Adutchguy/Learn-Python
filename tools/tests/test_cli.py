"""Tests for the `python -m learn` command line, run against a tiny throwaway course."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from learn import cli  # noqa: E402
from learn.course import load_course, resolve  # noqa: E402
from learn.progress import Progress  # noqa: E402

LESSON_MD = """# {title}

*{module} · about {minutes} minutes*

## Why this matters

Text.

## Your turn

<details><summary>Hint 1</summary>

first {slug}

</details>

<details><summary>Hint 2</summary>

second {slug}

</details>

<details><summary>Hint 3</summary>

third {slug}

</details>
"""

TEST_PASSING = "def test_ok():\n    assert True, 'always'\n"
TEST_FAILING = "def test_nope():\n    assert False, 'expected to fail'\n"


def make_lesson(root, module, slug, title, minutes=5, passing=True):
    folder = root / "exercises" / module / slug
    folder.mkdir(parents=True)
    (folder / "LESSON.md").write_text(LESSON_MD.format(title=title, module=module[3:].title(), minutes=minutes, slug=slug), encoding="utf-8")
    (folder / "exercise.py").write_text("# your code\n", encoding="utf-8")
    (folder / "test_exercise.py").write_text(TEST_PASSING if passing else TEST_FAILING, encoding="utf-8")


@pytest.fixture
def course_root(tmp_path, monkeypatch):
    make_lesson(tmp_path, "01-basics", "01-alpha", "Alpha", 5)
    make_lesson(tmp_path, "01-basics", "02-beta", "Beta", 10, passing=False)
    make_lesson(tmp_path, "02-more", "01-gamma", "Gamma", 20)
    (tmp_path / "exercises" / "README.md").write_text("not a module", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("[pytest]\naddopts = --import-mode=importlib -p no:cacheprovider\n", encoding="utf-8")
    monkeypatch.setenv("LEARN_ROOT", str(tmp_path))
    return tmp_path


def run(*argv):
    return cli.main(list(argv))


def test_course_is_read_in_order(course_root):
    course = load_course(course_root)
    assert [lesson.id for lesson in course] == ["01-basics/01-alpha", "01-basics/02-beta", "02-more/01-gamma"], "lessons should be in course order"
    first = course[0]
    assert (first.title, first.module, first.minutes) == ("Alpha", "Basics", 5), "title, module and minutes come from LESSON.md"
    assert len(first.hints) == 3 and first.hints[0] == "first 01-alpha", "all three hints are read"


def test_resolve_by_number_id_and_word(course_root):
    course = load_course(course_root)
    assert resolve(course, "2").id == "01-basics/02-beta", "a number picks that lesson"
    assert resolve(course, "exercises/02-more/01-gamma/").title == "Gamma", "a pasted folder path works"
    assert resolve(course, "gamma").title == "Gamma", "a unique word works"
    with pytest.raises(LookupError):
        resolve(course, "9")
    with pytest.raises(LookupError):
        resolve(course, "nothing-like-this")
    with pytest.raises(LookupError, match="several"):
        resolve(course, "01-")


def test_next_shows_first_lesson_then_advances(course_root, capsys):
    assert run() == 0, "no command means 'next'"
    assert "Lesson 1 of 3: Alpha" in capsys.readouterr().out, "starts at the first lesson"
    assert run("check") == 0, "the passing lesson should pass"
    capsys.readouterr()
    run("next")
    assert "Lesson 2 of 3: Beta" in capsys.readouterr().out, "moves on after a pass"


def test_failing_check_returns_one_and_records_nothing(course_root, capsys):
    assert run("check", "beta") == 1, "a failing lesson exits 1"
    assert "Not quite yet" in capsys.readouterr().out, "failure advice is shown"
    assert not Progress(course_root / ".learn-progress.json").completed, "a failure must not count as complete"


def test_progress_survives_between_runs_and_status_counts(course_root, capsys):
    run("check", "alpha")
    run("check", "gamma")
    capsys.readouterr()
    assert Progress(course_root / ".learn-progress.json").completed == {"01-basics/01-alpha", "02-more/01-gamma"}, "both passes are saved"
    run("status")
    out = capsys.readouterr().out
    assert "2 of 3 lessons (67%)" in out, "overall progress is summarised"
    run("list")
    out = capsys.readouterr().out
    assert "[x]   1  Alpha" in out and ">[ ]   2  Beta" in out, "finished lessons are ticked and the next one is marked"


def test_hints_are_revealed_one_at_a_time(course_root, capsys):
    run("hint", "alpha")
    assert "first 01-alpha" in capsys.readouterr().out, "hint 1 first"
    run("hint", "alpha")
    out = capsys.readouterr().out
    assert "second 01-alpha" in out and "first 01-alpha" not in out, "then hint 2 only"
    run("hint", "alpha")
    run("hint", "alpha")
    assert "seen all 3 hints" in capsys.readouterr().out, "after the last hint, point back to the lesson"


def test_damaged_progress_file_is_ignored(course_root, capsys):
    (course_root / ".learn-progress.json").write_text("{not json", encoding="utf-8")
    assert run("next") == 0, "a damaged file should not crash the tool"
    assert "Lesson 1 of 3" in capsys.readouterr().out, "it just starts fresh"


def test_unknown_lesson_gives_a_friendly_error(course_root, capsys):
    assert run("check", "zzz") == 2, "bad lesson name exits 2"
    assert "No lesson matches" in capsys.readouterr().out, "the message explains what to do"


def test_finishing_everything(course_root, capsys):
    make_lesson(course_root, "03-end", "01-last", "Last")
    for word in ("alpha", "gamma", "last"):
        run("check", word)
    (course_root / "exercises" / "01-basics" / "02-beta" / "test_exercise.py").write_text(TEST_PASSING, encoding="utf-8")
    run("check", "beta")
    capsys.readouterr()
    run("next")
    assert "finished all 4 lessons" in capsys.readouterr().out, "completion message"


def test_no_exercises_folder(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LEARN_ROOT", str(tmp_path))
    assert run("next") == 2, "an empty root is reported, not a crash"
    assert "No lessons found" in capsys.readouterr().out, "tells the learner what is wrong"
