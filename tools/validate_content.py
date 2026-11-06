#!/usr/bin/env python3
"""Validate everything under content/: lessons and the placement-test questions.

The placement questions are checked by actually running their code, so this takes a couple of seconds.
Exit code 1 if anything is wrong.
"""

from __future__ import annotations

import sys

from content import load_all
from placement import PLACEMENT_FILE, load_questions, validate_questions


def main() -> int:
    lessons, problems = load_all()

    questions = []
    if PLACEMENT_FILE.exists():
        try:
            questions = load_questions()
        except (ValueError, KeyError) as exc:
            problems.append(f"placement/questions.json: could not be read ({exc})")
        else:
            problems.extend(validate_questions(questions, [lesson.id for lesson in lessons]))
    else:
        problems.append("placement/questions.json is missing")

    if problems:
        print(f"Found {len(problems)} problem(s) in content/:\n")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    modules = {lesson.module.slug for lesson in lessons}
    print(
        f"OK: {len(lessons)} lesson(s) in {len(modules)} module(s) are valid; "
        f"{len(questions)} placement question(s) verified by running their code."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
