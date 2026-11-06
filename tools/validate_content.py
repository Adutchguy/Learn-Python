#!/usr/bin/env python3
"""Validate everything under content/. Exit code 1 if anything is wrong."""

from __future__ import annotations

import sys

from content import load_all


def main() -> int:
    lessons, problems = load_all()
    if problems:
        print(f"Found {len(problems)} problem(s) in content/:\n")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    modules = {lesson.module.slug for lesson in lessons}
    print(f"OK: {len(lessons)} lesson(s) in {len(modules)} module(s) are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
