"""Tests for the fast-track validator, so a wrong example or a broken lesson link is caught in CI."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fasttrack  # noqa: E402
from content import load_all  # noqa: E402

LESSONS = ["00-start/01-how-this-works", "01-foundations/01-hello-world", "01-foundations/02-variables", "02-control-flow/01-if-else"]


def good():
    return {
        "intro": "For programmers.",
        "skip": ["01-foundations/01-hello-world"],
        "rows": [
            {
                "topic": "Numbers",
                "expect": "x",
                "python": "y",
                "code": "print(7 // 2)",
                "output": "3",
                "lessons": ["01-foundations/02-variables"],
            }
        ],
    }


def test_a_good_file_has_no_problems():
    assert fasttrack.validate_fasttrack(good(), LESSONS) == [], "a correct fast-track file should have no problems"


def test_unknown_skip_and_row_lessons_are_reported():
    data = good()
    data["skip"] = ["99-nope/01-x"]
    data["rows"][0]["lessons"] = ["99-nope/02-y"]
    problems = fasttrack.validate_fasttrack(data, LESSONS)
    assert any("skip list names a lesson that does not exist" in p for p in problems), f"unknown skipped lesson not reported: {problems}"
    assert any("does not exist" in p and "row 1" in p for p in problems), f"unknown row lesson not reported: {problems}"


def test_orientation_lesson_cannot_be_skipped():
    data = good()
    data["skip"] = ["00-start/01-how-this-works"]
    problems = fasttrack.validate_fasttrack(data, LESSONS)
    assert any("orientation" in p for p in problems), f"skipping the orientation lesson should be reported: {problems}"


def test_wrong_output_is_caught_by_running_the_code():
    data = good()
    data["rows"][0]["output"] = "4"
    problems = fasttrack.validate_fasttrack(data, LESSONS)
    assert any("prints '3', not the stated '4'" in p for p in problems), f"a wrong stated output should be reported: {problems}"


def test_failing_example_is_reported():
    data = good()
    data["rows"][0]["code"] = "print(1 / 0)"
    problems = fasttrack.validate_fasttrack(data, LESSONS)
    assert any("fails with an error" in p and "ZeroDivisionError" in p for p in problems), f"a crashing example should be reported: {problems}"


def test_code_and_output_come_together_and_rows_are_required():
    data = good()
    del data["rows"][0]["output"]
    assert any("given together" in p for p in fasttrack.validate_fasttrack(data, LESSONS)), "code without output should be reported"
    data = good()
    data["rows"] = []
    assert any("'rows' must be" in p for p in fasttrack.validate_fasttrack(data, LESSONS)), "no rows should be reported"


def test_the_real_file_is_valid():
    lessons, problems = load_all()
    assert problems == [] or all("review" in p for p in problems), f"lesson problems: {problems}"
    data = fasttrack.load_fasttrack()
    assert fasttrack.validate_fasttrack(data, [lesson.id for lesson in lessons]) == [], "content/fast-track/path.json should be valid"
