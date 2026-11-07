"""Tests for the lesson scaffold tool: it must produce files the validator accepts once they are edited,
and must never let an unedited scaffold through."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import content  # noqa: E402
import new_lesson  # noqa: E402


@pytest.fixture
def course(tmp_path, monkeypatch):
    for name, title in (("01-basics", "Basics"), ("02-more", "More")):
        (tmp_path / name).mkdir()
        (tmp_path / name / "module.json").write_text(f'{{"title": "{title}", "description": "d"}}')
    (tmp_path / "review").mkdir()  # course-wide folders are not modules
    monkeypatch.setattr(new_lesson, "CONTENT", tmp_path)
    return tmp_path


def run(*args):
    return new_lesson.main(list(args))


def finish(lesson_dir):
    """What a contributor does: remove the placeholder marker."""
    md = lesson_dir / "lesson.md"
    md.write_text("\n".join(l for l in md.read_text().splitlines() if "SCAFFOLD" not in l) + "\n")


def test_creates_the_four_files_and_numbers_the_lesson(course, capsys):
    assert run("Variables and things", "--module", "basics") == 0
    lesson = course / "01-basics" / "01-variables-and-things"
    assert {p.name for p in lesson.iterdir()} == set(content.LESSON_FILES)
    assert run("Second one", "--module", "01") == 0
    assert (course / "01-basics" / "02-second-one").is_dir()
    assert "Next steps" in capsys.readouterr().out


def test_prereq_is_the_previous_lesson_even_across_modules(course):
    run("First", "--module", "01-basics")
    run("Second", "--module", "01-basics")
    run("Third", "--module", "02-more")
    assert 'prereqs: ["01-basics/01-first"]' in (course / "01-basics/02-second/lesson.md").read_text()
    assert 'prereqs: ["01-basics/02-second"]' in (course / "02-more/01-third/lesson.md").read_text()


def test_unedited_scaffold_is_rejected_by_the_validator(course):
    run("First", "--module", "basics")
    _, problems = content.load_all(course)
    assert any("SCAFFOLD" in p for p in problems)


def test_edited_scaffold_validates_and_the_starter_fails_while_the_solution_passes(course):
    run("First", "--module", "basics", "--minutes", "8")
    lesson = course / "01-basics/01-first"
    finish(lesson)
    _, problems = content.load_all(course)
    assert problems == []
    assert "minutes: 8" in (lesson / "lesson.md").read_text()
    assert (lesson / "starter.py").read_text() != (lesson / "solution.py").read_text()


def test_new_optional_module_gets_the_flag_and_number(course):
    run("Plotting", "--new-module", "Plot things", "--optional", "--description", "Charts.")
    module = course / "03-plot-things"
    assert '"optional": true' in (module / "module.json").read_text()
    assert (module / "01-plotting" / "lesson.md").is_file()
    finish(module / "01-plotting")
    _, problems = content.load_all(course)
    assert problems == []


def test_packages_and_local_only_land_in_the_frontmatter(course):
    run("Frames", "--module", "basics", "--packages", "numpy", "pandas", "--local-only")
    text = (course / "01-basics/01-frames/lesson.md").read_text()
    assert "packages: [numpy, pandas]" in text
    assert "local_only: true" in text
    finish(course / "01-basics/01-frames")
    _, problems = content.load_all(course)
    assert problems == []


def test_titles_with_yaml_special_characters_are_quoted(course):
    run("Colons: a story", "--module", "basics")
    finish(course / "01-basics/01-colons-a-story")
    lessons, problems = content.load_all(course)
    assert problems == []
    assert lessons[0].meta["title"] == "Colons: a story"


def test_unknown_module_is_a_clear_error(course):
    with pytest.raises(SystemExit) as err:
        run("X", "--module", "nope")
    assert "Choose from" in str(err.value)
