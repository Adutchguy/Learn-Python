"""Load and verify the placement-test question bank (content/placement/questions.json).

Every question that shows code has its answer *checked by running that code*, so a wrong
answer key can never ship. Questions must also be listed in course order, because the
test stops after two misses and recommends starting at the lesson of the first miss.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from content import CONTENT

PLACEMENT_FILE = CONTENT / "placement" / "questions.json"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KINDS = ("output", "error")
RUN_TIMEOUT_SECONDS = 10


def load_questions(path: Path = PLACEMENT_FILE) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["questions"]


def run_code(code: str, stdin: str = "") -> tuple[int, str, str]:
    """Run a snippet in a fresh Python process; returns (exit code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "snippet.py"
        script.write_text(code + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-I", str(script)],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_SECONDS,
            cwd=tmp,
        )
    return result.returncode, result.stdout, result.stderr


def validate_questions(questions: list[dict], lesson_ids: list[str], execute: bool = True) -> list[str]:
    problems: list[str] = []
    order = {lesson_id: i for i, lesson_id in enumerate(lesson_ids)}
    seen_ids: set[str] = set()
    last_position = -1
    seen_beyond = False

    if not questions:
        return ["placement: there are no questions"]

    for index, q in enumerate(questions, 1):
        qid = q.get("id")
        where = f"placement question {index} ({qid})"

        if not isinstance(qid, str) or not ID_RE.match(qid):
            problems.append(f"{where}: 'id' must be lowercase words joined by hyphens")
        elif qid in seen_ids:
            problems.append(f"{where}: duplicate id")
        else:
            seen_ids.add(qid)

        for key in ("prompt", "explanation"):
            if not isinstance(q.get(key), str) or not q[key].strip():
                problems.append(f"{where}: '{key}' must be a non-empty string")

        code = q.get("code")
        if code is not None and not isinstance(code, str):
            problems.append(f"{where}: 'code' must be a string")
        kind = q.get("kind", "output")
        if kind not in KINDS:
            problems.append(f"{where}: 'kind' must be one of {', '.join(KINDS)}")
        if kind == "error" and not isinstance(code, str):
            problems.append(f"{where}: an 'error' question needs 'code'")
        if "stdin" in q and not isinstance(q["stdin"], str):
            problems.append(f"{where}: 'stdin' must be a string")

        lesson = q.get("lesson")
        if lesson is None:
            if not isinstance(q.get("topic"), str) or not q["topic"].strip():
                problems.append(f"{where}: a question beyond the published lessons needs a 'topic'")
            seen_beyond = True
        elif lesson not in order:
            problems.append(f"{where}: lesson {lesson!r} does not exist")
        else:
            if seen_beyond:
                problems.append(f"{where}: questions about published lessons must come before 'beyond' questions")
            if order[lesson] < last_position:
                problems.append(f"{where}: questions must be in course order (lesson {lesson!r} comes too late)")
            last_position = max(last_position, order[lesson])

        options = q.get("options")
        answer = q.get("answer")
        valid_options = (
            isinstance(options, list)
            and 2 <= len(options) <= 5
            and all(isinstance(o, str) and o.strip() for o in options)
        )
        if not valid_options:
            problems.append(f"{where}: 'options' must be 2 to 5 non-empty strings")
            continue
        if len(set(options)) != len(options):
            problems.append(f"{where}: options must all be different")
        if not isinstance(answer, int) or isinstance(answer, bool) or not 0 <= answer < len(options):
            problems.append(f"{where}: 'answer' must be the index of the correct option")
            continue

        if execute and isinstance(code, str) and kind in KINDS:
            problems.extend(_verify_by_running(where, q, kind, options, answer))

    return problems


def _verify_by_running(where: str, q: dict, kind: str, options: list[str], answer: int) -> list[str]:
    try:
        exit_code, out, err = run_code(q["code"], q.get("stdin", ""))
    except subprocess.TimeoutExpired:
        return [f"{where}: the code did not finish within {RUN_TIMEOUT_SECONDS} seconds"]

    if kind == "output":
        if exit_code != 0:
            return [f"{where}: the code crashed, but the question expects printed output:\n{err}"]
        actual = out.rstrip("\n")
        if options[answer] != actual:
            return [f"{where}: the answer key says {options[answer]!r} but the code prints {actual!r}"]
        matches = [i for i, o in enumerate(options) if o == actual]
        if len(matches) != 1:
            return [f"{where}: more than one option matches the real output"]
        return []

    # kind == "error"
    if exit_code == 0:
        return [f"{where}: the code runs without an error, but the question expects one"]
    last_line = err.strip().splitlines()[-1] if err.strip() else ""
    error_name = last_line.split(":", 1)[0].strip()
    if options[answer] != error_name:
        return [f"{where}: the answer key says {options[answer]!r} but the code raises {error_name!r}"]
    return []
