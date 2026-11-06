"""Tests for the placement-test verifier: a wrong answer key must never ship."""

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import content  # noqa: E402
import placement  # noqa: E402

LESSONS = ["00-start/01-a", "01-foundations/01-b", "01-foundations/02-c"]

GOOD = {
    "id": "adds",
    "lesson": "01-foundations/01-b",
    "prompt": "What does this print?",
    "code": "print(1 + 2)",
    "options": ["3", "12", "It causes an error"],
    "answer": 0,
    "explanation": "1 + 2 is 3.",
}


def check(*questions, execute=True):
    return placement.validate_questions([copy.deepcopy(q) for q in questions], LESSONS, execute=execute)


def test_a_good_question_passes():
    assert check(GOOD) == []


def test_wrong_answer_key_is_caught_by_running_the_code():
    bad = {**GOOD, "answer": 1}
    problems = check(bad)
    assert any("the code prints '3'" in p for p in problems), problems


def test_error_questions_check_the_exception_name():
    q = {
        **GOOD,
        "id": "boom",
        "kind": "error",
        "code": "print(nope)",
        "options": ["SyntaxError", "NameError", "TypeError"],
        "answer": 1,
    }
    assert check(q) == []
    assert any("raises 'NameError'" in p for p in check({**q, "answer": 2}))
    assert any("runs without an error" in p for p in check({**q, "code": "print(1)"}))


def test_stdin_is_fed_to_the_code():
    q = {**GOOD, "id": "echo", "code": "print(input() * 2)", "stdin": "ab\n", "options": ["abab", "ab", "2"], "answer": 0}
    assert check(q) == []


def test_unknown_lesson_duplicate_id_and_bad_options_are_reported():
    assert any("does not exist" in p for p in check({**GOOD, "lesson": "01-foundations/99-nope"}))
    assert any("duplicate id" in p for p in check(GOOD, {**GOOD, "lesson": "01-foundations/02-c"}))
    assert any("must all be different" in p for p in check({**GOOD, "options": ["3", "3", "x"]}, execute=False))
    assert any("2 to 5" in p for p in check({**GOOD, "options": ["3"]}, execute=False))
    assert any("index of the correct option" in p for p in check({**GOOD, "answer": 7}, execute=False))


def test_questions_must_follow_course_order():
    early = {**GOOD, "id": "early", "lesson": "01-foundations/01-b"}
    late = {**GOOD, "id": "late", "lesson": "01-foundations/02-c"}
    assert check(early, late) == []
    assert any("course order" in p for p in check(late, early))


def test_beyond_the_course_questions_need_a_topic_and_must_come_last():
    beyond = {**GOOD, "id": "beyond", "lesson": None}
    assert any("needs a 'topic'" in p for p in check(beyond))
    assert check({**beyond, "topic": "Functions"}) == []
    later = {**GOOD, "id": "later", "lesson": "01-foundations/02-c"}
    assert any("must come before" in p for p in check({**beyond, "topic": "Functions"}, later))


def test_runaway_code_times_out_instead_of_hanging(monkeypatch):
    monkeypatch.setattr(placement, "RUN_TIMEOUT_SECONDS", 1)
    q = {**GOOD, "id": "loop", "code": "while True:\n    pass"}
    assert any("did not finish" in p for p in check(q))


def test_the_real_question_bank_is_valid_and_placement_is_not_treated_as_a_module():
    lessons, problems = content.load_all()
    assert problems == [], problems
    questions = placement.load_questions()
    assert placement.validate_questions(questions, [lesson.id for lesson in lessons]) == []
    assert all(lesson.module.slug != "placement" for lesson in lessons)
