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


def add_lesson(course, module_slug, lesson_slug, lesson_md, optional=False, title="Extra"):
    module = course / module_slug
    lesson = module / lesson_slug
    lesson.mkdir(parents=True)
    flag = ', "optional": true' if optional else ""
    (module / "module.json").write_text('{"title": "' + title + '", "description": "d"' + flag + "}")
    (lesson / "lesson.md").write_text(lesson_md)
    (lesson / "starter.py").write_text("x = 0\n")
    (lesson / "solution.py").write_text("x = 1\n")
    (lesson / "test_exercise.py").write_text(GOOD_TESTS)


def test_declared_packages_are_accepted(tmp_path):
    good = GOOD_LESSON_MD.replace("local_only: false", 'local_only: false\npackages: ["numpy", "pandas"]')
    assert problems_for(tmp_path, lesson_md=good) == []


def test_unknown_package_is_rejected(tmp_path):
    bad = GOOD_LESSON_MD.replace("local_only: false", 'local_only: false\npackages: ["scikit-learn"]')
    assert any("not allowed" in p for p in problems_for(tmp_path, lesson_md=bad))


def test_packages_must_be_a_list(tmp_path):
    bad = GOOD_LESSON_MD.replace("local_only: false", "local_only: false\npackages: numpy")
    assert any("'packages' must be a non-empty list" in p for p in problems_for(tmp_path, lesson_md=bad))


def test_optional_module_flag_must_be_true_or_false(tmp_path):
    course = make_course(tmp_path)
    (course / "01-basics" / "module.json").write_text('{"title": "B", "description": "d", "optional": "yes"}')
    _, problems = content.load_all(course)
    assert any("'optional' must be true or false" in p for p in problems)


def test_optional_modules_are_marked_and_labelled(tmp_path):
    course = make_course(tmp_path)
    add_lesson(course, "11-track", "01-extra", GOOD_LESSON_MD, optional=True, title="Fancy Track")
    lessons, problems = content.load_all(course)
    assert problems == []
    extra = [lesson for lesson in lessons if lesson.id == "11-track/01-extra"][0]
    assert extra.module.optional is True, "the module is flagged optional"
    assert "*Optional track: Fancy Track" in content.render_lesson_markdown(extra), "the local LESSON.md says so"


def test_a_core_lesson_cannot_require_an_optional_one(tmp_path):
    course = make_course(tmp_path)
    add_lesson(course, "11-track", "01-extra", GOOD_LESSON_MD, optional=True)
    # a later core module that requires the optional lesson
    late = GOOD_LESSON_MD.replace("prereqs: []", 'prereqs: ["11-track/01-extra"]')
    add_lesson(course, "12-core", "01-late", late, optional=False, title="Late")
    _, problems = content.load_all(course)
    assert any("cannot require the optional lesson" in p for p in problems)


def test_lesson_markdown_mentions_needed_packages(tmp_path):
    course = make_course(tmp_path, lesson_md=GOOD_LESSON_MD.replace("local_only: false", 'local_only: false\npackages: ["pandas"]'))
    lessons, _ = content.load_all(course)
    assert "requirements-tracks.txt" in content.render_lesson_markdown(lessons[0]), "the local lesson says how to install them"
