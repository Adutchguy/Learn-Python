"""Load and validate lesson content.

`content/` is the single source of truth. Every other artifact (the local
`exercises/` track and the website) is derived from it.

Layout::

    content/<NN-module>/module.json
    content/<NN-module>/<NN-lesson>/lesson.md        (YAML frontmatter + Markdown)
    content/<NN-module>/<NN-lesson>/starter.py       (what the learner starts with)
    content/<NN-module>/<NN-lesson>/solution.py      (reference answer)
    content/<NN-module>/<NN-lesson>/test_exercise.py (pytest-compatible tests)
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
EXERCISES = ROOT / "exercises"

LESSON_FILES = ("lesson.md", "starter.py", "solution.py", "test_exercise.py")
SLUG_RE = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_HEADINGS = ("## Your turn", "## Recap")
HINT_COUNT = 3


@dataclass
class Module:
    dir: Path
    slug: str
    title: str
    description: str


@dataclass
class Lesson:
    id: str  # "<module-slug>/<lesson-slug>"
    dir: Path
    module: Module
    meta: dict
    body: str
    starter: str
    solution: str
    tests: str
    errors: list[str] = field(default_factory=list)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split ``---\\nyaml\\n---\\nbody`` into (meta, body)."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("lesson.md must start with a '---' frontmatter block")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter block is not closed with '---'")
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return meta, text[end + 5 :]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def load_all(content_dir: Path = CONTENT) -> tuple[list[Lesson], list[str]]:
    """Load every lesson in order. Returns (lessons, problems)."""
    problems: list[str] = []
    lessons: list[Lesson] = []

    for module_dir in sorted(p for p in content_dir.iterdir() if p.is_dir()):
        rel = module_dir.relative_to(content_dir)
        if not SLUG_RE.match(module_dir.name):
            problems.append(f"{rel}: folder name must look like '01-some-name'")
            continue
        module_json = module_dir / "module.json"
        if not module_json.exists():
            problems.append(f"{rel}: missing module.json")
            continue
        try:
            raw = json.loads(_read(module_json))
            module = Module(module_dir, module_dir.name, str(raw["title"]), str(raw["description"]))
        except (ValueError, KeyError) as exc:
            problems.append(f"{rel}/module.json: needs 'title' and 'description' ({exc})")
            continue

        for lesson_dir in sorted(p for p in module_dir.iterdir() if p.is_dir()):
            lrel = lesson_dir.relative_to(content_dir)
            if not SLUG_RE.match(lesson_dir.name):
                problems.append(f"{lrel}: folder name must look like '01-some-name'")
                continue
            missing = [f for f in LESSON_FILES if not (lesson_dir / f).exists()]
            extra = sorted(
                p.name
                for p in lesson_dir.iterdir()
                if p.name not in LESSON_FILES and p.name != "__pycache__"
            )
            if missing:
                problems.append(f"{lrel}: missing file(s): {', '.join(missing)}")
                continue
            if extra:
                problems.append(f"{lrel}: unexpected file(s): {', '.join(extra)}")
            try:
                meta, body = split_frontmatter(_read(lesson_dir / "lesson.md"))
            except ValueError as exc:
                problems.append(f"{lrel}/lesson.md: {exc}")
                continue
            lessons.append(
                Lesson(
                    id=f"{module.slug}/{lesson_dir.name}",
                    dir=lesson_dir,
                    module=module,
                    meta=meta,
                    body=body,
                    starter=_read(lesson_dir / "starter.py"),
                    solution=_read(lesson_dir / "solution.py"),
                    tests=_read(lesson_dir / "test_exercise.py"),
                )
            )

    problems.extend(validate(lessons))
    return lessons, problems


def validate(lessons: list[Lesson]) -> list[str]:
    problems: list[str] = []
    order = {lesson.id: i for i, lesson in enumerate(lessons)}

    for lesson in lessons:
        where = lesson.id
        m = lesson.meta

        title = m.get("title")
        if not isinstance(title, str) or not title.strip():
            problems.append(f"{where}: 'title' must be a non-empty string")

        minutes = m.get("minutes")
        if not isinstance(minutes, int) or isinstance(minutes, bool) or not 1 <= minutes <= 60:
            problems.append(f"{where}: 'minutes' must be a whole number from 1 to 60")

        prereqs = m.get("prereqs")
        if not isinstance(prereqs, list):
            problems.append(f"{where}: 'prereqs' must be a list (use [] for none)")
        else:
            for pre in prereqs:
                if pre not in order:
                    problems.append(f"{where}: prerequisite {pre!r} does not exist")
                elif order[pre] >= order[lesson.id]:
                    problems.append(f"{where}: prerequisite {pre!r} must come earlier in the course")

        concepts = m.get("concepts")
        if (
            not isinstance(concepts, list)
            or not concepts
            or not all(isinstance(c, str) and c.strip() for c in concepts)
        ):
            problems.append(f"{where}: 'concepts' must be a non-empty list of strings")

        if not isinstance(m.get("local_only"), bool):
            problems.append(f"{where}: 'local_only' must be true or false")

        hints = m.get("hints")
        if (
            not isinstance(hints, list)
            or len(hints) != HINT_COUNT
            or not all(isinstance(h, str) and h.strip() for h in hints)
        ):
            problems.append(f"{where}: 'hints' must be a list of exactly {HINT_COUNT} non-empty strings")

        unknown = set(m) - {"title", "minutes", "prereqs", "concepts", "local_only", "hints"}
        if unknown:
            problems.append(f"{where}: unknown frontmatter key(s): {', '.join(sorted(unknown))}")

        for heading in REQUIRED_HEADINGS:
            if not re.search(rf"^{re.escape(heading)}\s*$", lesson.body, re.MULTILINE):
                problems.append(f"{where}: lesson.md is missing the '{heading}' section")

        for name, source in (
            ("starter.py", lesson.starter),
            ("solution.py", lesson.solution),
            ("test_exercise.py", lesson.tests),
        ):
            try:
                tree = ast.parse(source)
            except SyntaxError as exc:
                problems.append(f"{where}/{name}: syntax error on line {exc.lineno}: {exc.msg}")
                continue
            if name == "test_exercise.py":
                problems.extend(_check_tests(where, tree))

        if lesson.starter.strip() == lesson.solution.strip():
            problems.append(f"{where}: starter.py and solution.py are identical")

    return problems


def _check_tests(where: str, tree: ast.AST) -> list[str]:
    """Tests must give learners a helpful message on every assert."""
    problems = []
    tests = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    if not tests:
        problems.append(f"{where}/test_exercise.py: contains no test_* functions")
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert) and node.msg is None:
            problems.append(
                f"{where}/test_exercise.py line {node.lineno}: every assert needs a helpful message "
                "(assert condition, \"what the learner should do\")"
            )
    return problems


def expected_exercise_files(lessons: list[Lesson]) -> dict[Path, str]:
    """Map of path (relative to EXERCISES) -> expected file content for the local track."""
    files: dict[Path, str] = {}
    for lesson in lessons:
        base = Path(lesson.module.slug) / lesson.dir.name
        files[base / "exercise.py"] = lesson.starter
        files[base / "test_exercise.py"] = lesson.tests
        files[base / "LESSON.md"] = render_lesson_markdown(lesson)
    return files


def render_lesson_markdown(lesson: Lesson) -> str:
    """Plain-Markdown version of a lesson for people working in the repo."""
    m = lesson.meta
    parts = [
        f"# {m['title']}\n",
        f"*{lesson.module.title} · about {m['minutes']} minutes*\n",
        lesson.body.strip() + "\n",
        "## How to check your work\n",
        "Edit `exercise.py` in this folder, then run this from the repository root:\n",
        f"```\npytest exercises/{lesson.id}\n```\n",
        "## Stuck? Hints\n",
        "Try each hint in order, one at a time.\n",
    ]
    for i, hint in enumerate(m["hints"], 1):
        parts.append(f"<details><summary>Hint {i}</summary>\n\n{hint}\n\n</details>\n")
    return "\n".join(parts)


# Files in exercises/ that people maintain by hand and the generator must not touch.
HAND_MAINTAINED = {Path("conftest.py"), Path("README.md")}
