"""Tests for the review-question verifier: coverage of every lesson, and answer keys that are run."""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import content  # noqa: E402
import review  # noqa: E402


def lesson(lesson_id, title="Demo"):
    return SimpleNamespace(id=lesson_id, meta={"title": title})


LESSONS = [lesson("00-start/01-how-this-works"), lesson("01-foundations/01-a"), lesson("01-foundations/02-b"), lesson("01-foundations/03-project", "Project: Demo")]

GOOD = {
    "id": "a-1",
    "lesson": "01-foundations/01-a",
    "prompt": "What does this print?",
    "code": "print(2 * 3)",
    "options": ["5", "6", "23"],
    "answer": 1,
    "explanation": "2 * 3 is 6.",
}
GOOD_B = {**GOOD, "id": "b-1", "lesson": "01-foundations/02-b"}


def check(questions, lessons=LESSONS):
    return review.validate_review(questions, lessons)


def test_full_coverage_passes_and_projects_and_orientation_are_exempt():
    assert check([GOOD, GOOD_B]) == []


def test_a_lesson_without_a_question_is_reported():
    problems = check([GOOD])
    assert any("01-foundations/02-b has no review question" in p for p in problems), problems


def test_every_question_needs_a_lesson():
    problems = check([GOOD, GOOD_B, {**GOOD, "id": "free", "lesson": None, "topic": "Later"}])
    assert any("must belong to a lesson" in p for p in problems), problems


def test_wrong_answer_key_is_caught_by_running_the_code():
    problems = check([{**GOOD, "answer": 0}, GOOD_B])
    assert any("the code prints '6'" in p for p in problems), problems
    assert all("review question" in p or "review:" in p for p in problems), problems


def test_the_real_review_bank_covers_every_lesson_and_every_answer_is_right():
    lessons, problems = content.load_all()
    assert problems == [], problems
    questions = review.load_review_questions()
    assert review.validate_review(questions, lessons) == []
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), "review question ids must be unique"
