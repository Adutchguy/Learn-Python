"""Load and verify the spaced-review question bank (content/review/questions.json).

The review queue resurfaces short "what does this print?" questions after a lesson is
completed. Same format as the placement test, and every answer key is checked by running
the code. Additionally, every lesson must have at least one review question so that the
queue covers the whole course (projects and the orientation lesson are exempt).
"""

from __future__ import annotations

from pathlib import Path

from content import CONTENT
from placement import load_questions, validate_questions

REVIEW_FILE = CONTENT / "review" / "questions.json"
EXEMPT_LESSONS = {"00-start/01-how-this-works"}
PROJECT_TITLE_PREFIX = "Project:"


def load_review_questions(path: Path = REVIEW_FILE) -> list[dict]:
    return load_questions(path)


def validate_review(questions: list[dict], lessons: list, execute: bool = True) -> list[str]:
    """`lessons` are the loaded Lesson objects (anything with .id and .meta["title"])."""
    problems = [
        p.replace("placement question", "review question").replace("placement:", "review:")
        for p in validate_questions(questions, [lesson.id for lesson in lessons], execute=execute)
    ]
    for index, q in enumerate(questions, 1):
        if q.get("lesson") is None:
            problems.append(f"review question {index} ({q.get('id')}): every review question must belong to a lesson")

    covered = {q.get("lesson") for q in questions}
    for lesson in lessons:
        title = str(lesson.meta.get("title", ""))
        if lesson.id in covered or lesson.id in EXEMPT_LESSONS or title.startswith(PROJECT_TITLE_PREFIX):
            continue
        problems.append(f"review: lesson {lesson.id} has no review question (add one to content/review/questions.json)")
    return problems
