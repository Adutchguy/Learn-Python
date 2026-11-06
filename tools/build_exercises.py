#!/usr/bin/env python3
"""Generate the local-track `exercises/` folder from `content/`.

    python tools/build_exercises.py           # (re)write exercises/
    python tools/build_exercises.py --check   # fail if exercises/ is out of date (used in CI)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from content import EXERCISES, HAND_MAINTAINED, expected_exercise_files, load_all


def existing_files() -> set[Path]:
    if not EXERCISES.exists():
        return set()
    return {
        p.relative_to(EXERCISES)
        for p in EXERCISES.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    } - HAND_MAINTAINED


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--check", action="store_true", help="only verify; do not write")
    args = parser.parse_args()

    lessons, problems = load_all()
    if problems:
        print("Content is invalid; fix it first (python tools/validate_content.py):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    expected = expected_exercise_files(lessons)
    existing = existing_files()

    stale = sorted(existing - set(expected))
    missing = sorted(p for p in expected if not (EXERCISES / p).exists())
    changed = sorted(
        p
        for p in expected
        if (EXERCISES / p).exists()
        and (EXERCISES / p).read_text(encoding="utf-8").replace("\r\n", "\n") != expected[p]
    )

    if args.check:
        if stale or missing or changed:
            print("exercises/ is out of date. Run: python tools/build_exercises.py\n")
            for label, items in (("missing", missing), ("changed", changed), ("stale", stale)):
                for item in items:
                    print(f"  {label}: exercises/{item.as_posix()}")
            return 1
        print(f"OK: exercises/ matches content/ ({len(expected)} files).")
        return 0

    for path in stale:
        (EXERCISES / path).unlink()
    for folder in sorted({p.parent for p in stale}, key=lambda p: len(p.parts), reverse=True):
        target = EXERCISES / folder
        if target.exists() and not any(target.iterdir()):
            shutil.rmtree(target)
    for path, text in expected.items():
        target = EXERCISES / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {len(expected)} files for {len(lessons)} lesson(s) into exercises/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
