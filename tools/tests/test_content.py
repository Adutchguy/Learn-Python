"""Tests for the content validator itself, so bad lessons are caught before learners see them."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import content  # noqa: E402

GOOD_LESSON_MD = """---
title: Demo
minutes: 5
prereqs: []
concepts: [demo]
local_only: false
hints: [one, two, three]
---

## Your turn

Do it.

## Recap

Done.
"""

GOOD_TESTS = 'def test_it():\n    import exercise\n    assert exercise.x == 1, "set x to 1"\n'


def make_course(tmp_path, lesson_md=GOOD_LESSON_MD, tests=GOOD_TESTS, starter="x = 0\n", solution="x = 1\n"):
    module = tmp_path / "01-basics"
    lesson = module / "01-demo"
    lesson.mkdir(parents=True)
    (module / "module.json").write_text('{"title": "Basics", "description": "d"}')
    (lesson / "lesson.md").write_text(lesson_md)
    (lesson / "starter.py").write_text(starter)
    (lesson / "solution.py").write_text(solution)
    (lesson / "test_exercise.py").write_text(tests)
    return tmp_path


def problems_for(tmp_path, **kwargs):
    _, problems = content.load_all(make_course(tmp_path, **kwargs))
    return problems


def test_a_good_lesson_has_no_problems(tmp_path):
    assert problems_for(tmp_path) == []


def test_every_real_lesson_in_the_repo_is_valid():
    lessons, problems = content.load_all()
    assert problems == []
    assert len(lessons) >= 3


def test_assert_without_message_is_rejected(tmp_path):
    bad = "def test_it():\n    import exercise\n    assert exercise.x == 1\n"
    assert any("helpful message" in p for p in problems_for(tmp_path, tests=bad))


def test_wrong_number_of_hints_is_rejected(tmp_path):
    bad = GOOD_LESSON_MD.replace("hints: [one, two, three]", "hints: [one]")
    assert any("hints" in p for p in problems_for(tmp_path, lesson_md=bad))


def test_missing_required_section_is_rejected(tmp_path):
    bad = GOOD_LESSON_MD.replace("## Recap", "## Summary")
    assert any("## Recap" in p for p in problems_for(tmp_path, lesson_md=bad))


def test_unknown_prerequisite_is_rejected(tmp_path):
    bad = GOOD_LESSON_MD.replace("prereqs: []", 'prereqs: ["01-basics/99-nope"]')
    assert any("does not exist" in p for p in problems_for(tmp_path, lesson_md=bad))


def test_identical_starter_and_solution_is_rejected(tmp_path):
    assert any("identical" in p for p in problems_for(tmp_path, starter="x = 1\n", solution="x = 1\n"))


def test_syntax_error_in_starter_is_reported_with_line(tmp_path):
    assert any("starter.py" in p and "syntax error" in p for p in problems_for(tmp_path, starter="x = (\n"))


def test_missing_frontmatter_is_rejected(tmp_path):
    assert any("frontmatter" in p for p in problems_for(tmp_path, lesson_md="# no frontmatter\n"))


def test_bad_folder_name_is_rejected(tmp_path):
    course = make_course(tmp_path)
    (course / "01-basics" / "01-demo").rename(course / "01-basics" / "Demo Lesson")
    _, problems = content.load_all(course)
    assert any("folder name" in p for p in problems)


def test_bad_yaml_in_frontmatter_is_a_problem_not_a_crash():
    bad = GOOD_LESSON_MD.replace("concepts: [demo]", "concepts: [*args]")
    try:
        content.split_frontmatter(bad)
    except ValueError as exc:
        assert "not valid YAML" in str(exc)
    else:
        raise AssertionError("expected a ValueError for invalid YAML")
