"""The ``python -m learn`` command line.

    python -m learn                 what to do next
    python -m learn check [LESSON]  run the checks for a lesson (default: the next one)
    python -m learn hint [LESSON]   reveal the next hint, one at a time
    python -m learn status          your progress, module by module
    python -m learn list            every lesson, with the finished ones ticked

``LESSON`` can be a number from ``list``, a full id, or a word from the id (``variables``).
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

from .course import Lesson, find_root, load_course, resolve
from .progress import FILE_NAME, Progress


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _next_lesson(course: list[Lesson], progress: Progress) -> Lesson | None:
    for lesson in course:
        if lesson.id not in progress.completed:
            return lesson
    return None


def _describe(lesson: Lesson, course: list[Lesson], root: Path) -> None:
    number = course.index(lesson) + 1
    print(f"Lesson {number} of {len(course)}: {lesson.title}")
    print(f"{lesson.module} - about {lesson.minutes} minutes")
    print()
    print(f"  1. Read:   {_relative(lesson.lesson_file, root)}")
    print(f"  2. Edit:   {_relative(lesson.exercise_file, root)}")
    print("  3. Check:  python -m learn check")
    print("  Stuck?     python -m learn hint")


def _pick(args, course, progress) -> Lesson | None:
    """The lesson named on the command line, or the next unfinished one."""
    if getattr(args, "lesson", None):
        return resolve(course, args.lesson)
    return _next_lesson(course, progress)


def cmd_next(args, root, course, progress) -> int:
    lesson = _next_lesson(course, progress)
    if lesson is None:
        print(f"You have finished all {len(course)} lessons. Well done!")
        return 0
    _describe(lesson, course, root)
    return 0


def cmd_check(args, root, course, progress) -> int:
    lesson = _pick(args, course, progress)
    if lesson is None:
        print(f"Nothing left to check: you have finished all {len(course)} lessons.")
        return 0
    if importlib.util.find_spec("pytest") is None:
        print("pytest is not installed, and it runs the checks. Install it with:\n\n  pip install -r requirements.txt")
        return 2
    number = course.index(lesson) + 1
    print(f"Checking lesson {number} of {len(course)}: {lesson.title}\n")
    sys.stdout.flush()
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", _relative(lesson.folder, root)], cwd=root)
    print()
    if result.returncode == 0:
        newly = lesson.id not in progress.completed
        progress.completed.add(lesson.id)
        progress.save()
        print(f"PASSED. {'Lesson complete!' if newly else 'Already complete; still passing.'}")
        upcoming = _next_lesson(course, progress)
        if upcoming is None:
            print(f"That was the last one: all {len(course)} lessons are finished. Congratulations!")
        elif newly:
            print(f"Up next: {upcoming.title}  (python -m learn)")
        return 0
    if result.returncode == 1:
        print("Not quite yet. Read the failure messages above: each says what was expected.")
        print("Stuck? Reveal one hint with: python -m learn hint")
        return 1
    print(f"pytest could not run the checks (exit code {result.returncode}). Look at the messages above;")
    print("a syntax error in exercise.py is the most common reason.")
    return 2


def cmd_hint(args, root, course, progress) -> int:
    lesson = _pick(args, course, progress)
    if lesson is None:
        print("You have finished every lesson, so there is nothing to get hints for.")
        return 0
    if not lesson.hints:
        print(f"This lesson has no hints. Reread {_relative(lesson.lesson_file, root)}.")
        return 0
    seen = progress.hints_seen.get(lesson.id, 0)
    if seen >= len(lesson.hints):
        print(f"You have seen all {len(lesson.hints)} hints for '{lesson.title}'.")
        print(f"Reread {_relative(lesson.lesson_file, root)} and compare your code with the examples in it.")
        return 0
    print(f"Hint {seen + 1} of {len(lesson.hints)} for '{lesson.title}':\n")
    print(lesson.hints[seen])
    progress.hints_seen[lesson.id] = seen + 1
    progress.save()
    if seen + 1 < len(lesson.hints):
        print("\nStill stuck? Run the same command again for the next hint.")
    return 0


def cmd_status(args, root, course, progress) -> int:
    modules: dict[str, list[Lesson]] = {}
    for lesson in course:
        modules.setdefault(lesson.id.split("/")[0], []).append(lesson)
    for slug, lessons in modules.items():
        done = sum(1 for lesson in lessons if lesson.id in progress.completed)
        name = lessons[0].module or slug
        mark = "done" if done == len(lessons) else ""
        print(f"{name:<32} {done:>2}/{len(lessons):<2} {mark}".rstrip())
    finished = sum(1 for lesson in course if lesson.id in progress.completed)
    percent = round(100 * finished / len(course)) if course else 0
    print(f"\nOverall: {finished} of {len(course)} lessons ({percent}%)")
    remaining = sum(lesson.minutes for lesson in course if lesson.id not in progress.completed)
    if remaining:
        print(f"Roughly {remaining // 60} h {remaining % 60} min of lessons left.")
    return 0


def cmd_list(args, root, course, progress) -> int:
    upcoming = _next_lesson(course, progress)
    current_module = None
    for number, lesson in enumerate(course, 1):
        module_slug = lesson.id.split("/")[0]
        if module_slug != current_module:
            current_module = module_slug
            print(f"\n{lesson.module or module_slug}")
        tick = "x" if lesson.id in progress.completed else " "
        arrow = ">" if lesson is upcoming else " "
        print(f" {arrow}[{tick}] {number:>3}  {lesson.title}")
    print("\n[x] finished   > next up")
    return 0


COMMANDS = {"next": cmd_next, "check": cmd_check, "hint": cmd_hint, "status": cmd_status, "list": cmd_list}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m learn", description="Your guide through the Learn-Python exercises.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("next", help="show what to do next (the default)")
    for name, text in (("check", "run the checks for a lesson"), ("hint", "reveal the next hint for a lesson")):
        p = sub.add_parser(name, help=text)
        p.add_argument("lesson", nargs="?", help="a number from 'list', a lesson id, or a word from its name (default: the next lesson)")
    sub.add_parser("status", help="your progress, module by module")
    sub.add_parser("list", help="every lesson, with the finished ones ticked")
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    root = find_root()
    course = load_course(root)
    if not course:
        print(f"No lessons found in {root / 'exercises'}. Run this from a clone of the repository.")
        return 2
    progress = Progress(root / FILE_NAME)
    command = args.command or "next"
    try:
        return COMMANDS[command](args, root, course, progress)
    except LookupError as exc:
        print(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
