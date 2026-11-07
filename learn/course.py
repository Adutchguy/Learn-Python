"""Discover the lessons in ``exercises/`` and read their details from ``LESSON.md``.

The CLI deliberately depends only on the standard library (plus pytest, which runs the checks),
so a learner never needs anything beyond ``pip install -r requirements.txt``.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

NUMBERED = re.compile(r"^\d{2}-")
HEADER_LINE = re.compile(r"^\*(?P<module>.+?)\s+\S\s+about (?P<minutes>\d+) minutes?\*\s*$")
TRACK_PREFIX = "Optional track: "
HINT = re.compile(r"<details><summary>Hint \d+</summary>\n\n(.*?)\n\n</details>", re.DOTALL)


@dataclass(frozen=True)
class Lesson:
    id: str  # "04-functions/01-defining-functions"
    module: str  # "Functions"
    title: str
    minutes: int
    folder: Path
    hints: tuple[str, ...]
    optional: bool = False  # belongs to an optional track, not the core path

    @property
    def lesson_file(self) -> Path:
        return self.folder / "LESSON.md"

    @property
    def exercise_file(self) -> Path:
        return self.folder / "exercise.py"


def find_root() -> Path:
    """The repository root (override with LEARN_ROOT, which the tests use)."""
    override = os.environ.get("LEARN_ROOT")
    return Path(override) if override else Path(__file__).resolve().parent.parent


def _read_lesson(folder: Path, lesson_id: str) -> Lesson:
    text = (folder / "LESSON.md").read_text(encoding="utf-8")
    lines = [line for line in text.replace("\r\n", "\n").split("\n")]
    title = lines[0].lstrip("# ").strip() if lines else lesson_id
    module, minutes = "", 0
    for line in lines[1:6]:
        match = HEADER_LINE.match(line)
        if match:
            module, minutes = match.group("module"), int(match.group("minutes"))
            break
    hints = tuple(h.strip() for h in HINT.findall(text.replace("\r\n", "\n")))
    optional = module.startswith(TRACK_PREFIX)
    if optional:
        module = module[len(TRACK_PREFIX) :]
    return Lesson(lesson_id, module, title, minutes, folder, hints, optional)


def load_course(root: Path | None = None) -> list[Lesson]:
    """Every lesson in course order."""
    root = root or find_root()
    exercises = root / "exercises"
    lessons: list[Lesson] = []
    if not exercises.is_dir():
        return lessons
    for module_dir in sorted(p for p in exercises.iterdir() if p.is_dir() and NUMBERED.match(p.name)):
        for lesson_dir in sorted(p for p in module_dir.iterdir() if p.is_dir() and NUMBERED.match(p.name)):
            if (lesson_dir / "LESSON.md").is_file() and (lesson_dir / "exercise.py").is_file():
                lessons.append(_read_lesson(lesson_dir, f"{module_dir.name}/{lesson_dir.name}"))
    return lessons


def resolve(course: list[Lesson], query: str) -> Lesson:
    """Find a lesson from its id, its number in the course, or a word from its id.

    Raises LookupError with a message fit to show a learner.
    """
    query = query.strip().lower().replace("\\", "/").rstrip("/")
    if query.startswith("exercises/"):
        query = query[len("exercises/") :]
    for lesson in course:
        if lesson.id == query:
            return lesson
    if query.isdigit():
        number = int(query)
        if 1 <= number <= len(course):
            return course[number - 1]
        raise LookupError(f"There is no lesson number {number}. The course has {len(course)} lessons (see: python -m learn list).")
    matches = [lesson for lesson in course if query in lesson.id]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise LookupError(f"No lesson matches {query!r}. See all lessons with: python -m learn list")
    shown = "\n".join(f"  {m.id}" for m in matches[:8])
    more = f"\n  ... and {len(matches) - 8} more" if len(matches) > 8 else ""
    raise LookupError(f"{query!r} matches several lessons; be more specific:\n{shown}{more}")


def core_lessons(course: list[Lesson]) -> list[Lesson]:
    """The lessons on the main path (everything except the optional tracks)."""
    return [lesson for lesson in course if not lesson.optional]


def tracks(course: list[Lesson]) -> dict[str, list[Lesson]]:
    """Optional tracks by module folder name, in course order."""
    found: dict[str, list[Lesson]] = {}
    for lesson in course:
        if lesson.optional:
            found.setdefault(lesson.id.split("/")[0], []).append(lesson)
    return found


def resolve_track(course: list[Lesson], query: str) -> str:
    """Find an optional track from its folder name or a word from it ('data', 'web', 'automation').

    Raises LookupError with a message fit to show a learner.
    """
    names = list(tracks(course))
    query = query.strip().lower()
    if query in names:
        return query
    matches = [name for name in names if query and query in name]
    if len(matches) == 1:
        return matches[0]
    if not names:
        raise LookupError("This copy of the course has no optional tracks.")
    options = ", ".join(n.split("-", 1)[1] for n in names)
    if not matches:
        raise LookupError(f"No track matches {query!r}. The tracks are: {options}")
    raise LookupError(f"{query!r} matches several tracks ({options}); be more specific.")
