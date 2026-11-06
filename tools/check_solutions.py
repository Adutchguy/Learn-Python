#!/usr/bin/env python3
"""Prove that every exercise is well formed.

For each lesson, run its tests twice with real pytest:

* with ``solution.py`` as the learner's code  -> every test must PASS
* with ``starter.py``  as the learner's code  -> at least one test must FAIL
  (otherwise the exercise is already solved before the learner starts)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from content import EXERCISES, ROOT, load_all

PYTEST_PASSED = 0
PYTEST_TESTS_FAILED = 1


def run_pytest(lesson_id: str, learner_code: str, tests: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copy(ROOT / "pytest.ini", work / "pytest.ini")
        shutil.copy(EXERCISES / "conftest.py", work / "conftest.py")
        (work / "exercise.py").write_text(learner_code, encoding="utf-8", newline="\n")
        (work / "test_exercise.py").write_text(tests, encoding="utf-8", newline="\n")
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-o", "testpaths=.", "--rootdir", str(work), str(work)],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )


def main() -> int:
    lessons, problems = load_all()
    if problems:
        print("Content is invalid; fix it first (python tools/validate_content.py):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    failures = 0
    for lesson in lessons:
        solved = run_pytest(lesson.id, lesson.solution, lesson.tests)
        if solved.returncode != PYTEST_PASSED:
            failures += 1
            print(f"FAIL  {lesson.id}: the reference solution does not pass its own tests\n{solved.stdout}{solved.stderr}")
            continue
        started = run_pytest(lesson.id, lesson.starter, lesson.tests)
        if started.returncode != PYTEST_TESTS_FAILED:
            failures += 1
            why = "already passes" if started.returncode == PYTEST_PASSED else "errors instead of failing cleanly"
            print(f"FAIL  {lesson.id}: the starter code {why} (pytest exit code {started.returncode})\n{started.stdout}{started.stderr}")
            continue
        print(f"ok    {lesson.id}: solution passes, starter fails")

    if failures:
        print(f"\n{failures} lesson(s) need attention.")
        return 1
    print(f"\nAll {len(lessons)} lesson(s) check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
