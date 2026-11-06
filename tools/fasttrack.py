"""Load and verify the programmers' fast-track (content/fast-track/path.json).

The fast track is a page for people who already code. It lists lessons that experienced programmers
can skim (and the site can mark as skipped in one click), and a table of "what is different in
Python" examples. Every example's printed output is checked by *running* the code, and every lesson
id must exist, so the page can never show a wrong example or a broken link.
"""

from __future__ import annotations

import json
from pathlib import Path

from content import CONTENT
from placement import run_code

FASTTRACK_FILE = CONTENT / "fast-track" / "path.json"
ORIENTATION_PREFIX = "00-"


def load_fasttrack(path: Path = FASTTRACK_FILE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_fasttrack(data: dict, lesson_ids: list[str], execute: bool = True) -> list[str]:
    problems: list[str] = []
    known = set(lesson_ids)

    if not _text(data.get("intro")):
        problems.append("fast-track: 'intro' must be a non-empty string")

    skip = data.get("skip")
    if not isinstance(skip, list) or not skip:
        problems.append("fast-track: 'skip' must be a non-empty list of lesson ids")
        skip = []
    seen: set[str] = set()
    for lesson_id in skip:
        if lesson_id not in known:
            problems.append(f"fast-track: skip list names a lesson that does not exist: {lesson_id!r}")
        elif lesson_id.startswith(ORIENTATION_PREFIX):
            problems.append(f"fast-track: the orientation lesson {lesson_id!r} must never be skipped")
        if lesson_id in seen:
            problems.append(f"fast-track: {lesson_id!r} is listed twice in 'skip'")
        seen.add(lesson_id)
    if skip and len(known - set(skip)) < 2:
        problems.append("fast-track: the skip list leaves almost nothing to learn")

    rows = data.get("rows")
    if not isinstance(rows, list) or not rows:
        return problems + ["fast-track: 'rows' must be a non-empty list"]
    topics: set[str] = set()
    for index, row in enumerate(rows, 1):
        where = f"fast-track row {index} ({row.get('topic') if isinstance(row, dict) else row!r})"
        if not isinstance(row, dict):
            problems.append(f"{where}: must be an object")
            continue
        for key in ("topic", "expect", "python"):
            if not _text(row.get(key)):
                problems.append(f"{where}: '{key}' must be a non-empty string")
        if row.get("topic") in topics:
            problems.append(f"{where}: duplicate topic")
        topics.add(row.get("topic"))

        lessons = row.get("lessons")
        if not isinstance(lessons, list) or not lessons:
            problems.append(f"{where}: 'lessons' must list at least one lesson id")
        else:
            for lesson_id in lessons:
                if lesson_id not in known:
                    problems.append(f"{where}: lesson {lesson_id!r} does not exist")

        has_code, has_output = "code" in row, "output" in row
        if has_code != has_output:
            problems.append(f"{where}: 'code' and 'output' must be given together")
        elif has_code:
            if not _text(row["code"]) or not isinstance(row["output"], str):
                problems.append(f"{where}: 'code' and 'output' must be strings")
            elif execute:
                try:
                    exit_code, out, err = run_code(row["code"])
                except Exception as exc:  # timeouts and similar
                    problems.append(f"{where}: the example could not be run ({exc})")
                    continue
                if exit_code != 0:
                    problems.append(f"{where}: the example fails with an error: {err.strip().splitlines()[-1] if err.strip() else exit_code}")
                elif out.rstrip("\n") != row["output"]:
                    problems.append(f"{where}: the example prints {out.rstrip(chr(10))!r}, not the stated {row['output']!r}")
    return problems
