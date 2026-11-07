"""The ``python -m learn`` command line.

    python -m learn                 what to do next
    python -m learn check [LESSON]  run the checks for a lesson (default: the next one)
    python -m learn hint [LESSON]   reveal the next hint, one at a time
    python -m learn status          your progress, module by module
    python -m learn list            every lesson, with the finished ones ticked
    python -m learn tracks          the optional tracks (data analysis, automation, web and APIs)
    python -m learn next TRACK      what to do next in one optional track

``LESSON`` can be a number from ``list``, a full id, or a word from the id (``variables``).
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

from .course import Lesson, core_lessons, find_root, load_course, resolve, resolve_track, tracks
from .progress import FILE_NAME, Progress


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _next_lesson(course: list[Lesson], progress: Progress, track: str | None = None) -> Lesson | None:
    """The first unfinished lesson on the main path, or in the given optional track."""
    pool = tracks(course)[track] if track else core_lessons(course)
    for lesson in pool:
        if lesson.id not in progress.completed:
            return lesson
    return None


def _tracks_hint(course: list[Lesson]) -> str:
    names = [name.split("-", 1)[1] for name in tracks(course)]
    if not names:
        return ""
    return "Optional tracks you can try next: " + ", ".join(names) + "  (python -m learn tracks)"


def _describe(lesson: Lesson, course: list[Lesson], root: Path) -> None:
    if lesson.optional:
        pool = tracks(course)[lesson.id.split("/")[0]]
        print(f"Track lesson {pool.index(lesson) + 1} of {len(pool)}: {lesson.title}")
        print(f"Optional track: {lesson.module} - about {lesson.minutes} minutes")
    else:
        core = core_lessons(course)
        print(f"Lesson {core.index(lesson) + 1} of {len(core)}: {lesson.title}")
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
    track = resolve_track(course, args.track) if getattr(args, "track", None) else None
    lesson = _next_lesson(course, progress, track)
    if lesson is None:
        if track:
            print(f"You have finished every lesson in the {track.split('-', 1)[1]} track. Well done!")
        else:
            print(f"You have finished all {len(core_lessons(course))} core lessons. Well done!")
            hint = _tracks_hint(course)
            if hint:
                print(hint)
        return 0
    _describe(lesson, course, root)
    return 0


def cmd_check(args, root, course, progress) -> int:
    lesson = _pick(args, course, progress)
    if lesson is None:
        print(f"Nothing left to check: you have finished all {len(core_lessons(course))} core lessons.")
        hint = _tracks_hint(course)
        if hint:
            print(hint)
        return 0
    if importlib.util.find_spec("pytest") is None:
        print("pytest is not installed, and it runs the checks. Install it with:\n\n  pip install -r requirements.txt")
        return 2
    if lesson.optional:
        print(f"Checking optional-track lesson: {lesson.title}\n")
    else:
        core = core_lessons(course)
        print(f"Checking lesson {core.index(lesson) + 1} of {len(core)}: {lesson.title}\n")
    sys.stdout.flush()
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", _relative(lesson.folder, root)], cwd=root)
    print()
    if result.returncode == 0:
        newly = lesson.id not in progress.completed
        progress.completed.add(lesson.id)
        progress.save()
        print(f"PASSED. {'Lesson complete!' if newly else 'Already complete; still passing.'}")
        if lesson.optional:
            track = lesson.id.split("/")[0]
            upcoming = _next_lesson(course, progress, track)
            if upcoming is None:
                print(f"That was the last lesson in the {lesson.module} track. Congratulations!")
            elif newly:
                print(f"Up next in this track: {upcoming.title}  (python -m learn next {track.split('-', 1)[1]})")
            return 0
        upcoming = _next_lesson(course, progress)
        if upcoming is None:
            print(f"That was the last one: all {len(core_lessons(course))} core lessons are finished. Congratulations!")
            hint = _tracks_hint(course)
            if hint:
                print(hint)
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
        print("You have finished every core lesson, so there is nothing to get hints for.")
        print("Name a lesson to get hints for an optional one, for example: python -m learn hint numpy")
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


def _print_modules(lessons: list[Lesson], progress: Progress) -> None:
    modules: dict[str, list[Lesson]] = {}
    for lesson in lessons:
        modules.setdefault(lesson.id.split("/")[0], []).append(lesson)
    for slug, group in modules.items():
        done = sum(1 for lesson in group if lesson.id in progress.completed)
        name = group[0].module or slug
        mark = "done" if done == len(group) else ""
        print(f"{name:<32} {done:>2}/{len(group):<2} {mark}".rstrip())


def cmd_status(args, root, course, progress) -> int:
    core = core_lessons(course)
    _print_modules(core, progress)
    finished = sum(1 for lesson in core if lesson.id in progress.completed)
    percent = round(100 * finished / len(core)) if core else 0
    print(f"\nCore path: {finished} of {len(core)} lessons ({percent}%)")
    remaining = sum(lesson.minutes for lesson in core if lesson.id not in progress.completed)
    if remaining:
        print(f"Roughly {remaining // 60} h {remaining % 60} min of lessons left.")
    extra = [lesson for lesson in course if lesson.optional]
    if extra:
        print("\nOptional tracks")
        _print_modules(extra, progress)
    return 0


def cmd_tracks(args, root, course, progress) -> int:
    found = tracks(course)
    if not found:
        print("This copy of the course has no optional tracks.")
        return 0
    print("Optional tracks (try them any time after the core path, or after Module 6 or 8):\n")
    for slug, group in found.items():
        done = sum(1 for lesson in group if lesson.id in progress.completed)
        name = slug.split("-", 1)[1]
        print(f"  {group[0].module:<24} {done}/{len(group)} done   start: python -m learn next {name}")
    print("\nSome lessons need extra packages: pip install -r requirements-tracks.txt")
    return 0


def cmd_list(args, root, course, progress) -> int:
    upcoming = _next_lesson(course, progress)
    current_module = None
    for number, lesson in enumerate(course, 1):
        module_slug = lesson.id.split("/")[0]
        if module_slug != current_module:
            current_module = module_slug
            label = lesson.module or module_slug
            print(f"\n{'Optional track: ' if lesson.optional else ''}{label}")
        tick = "x" if lesson.id in progress.completed else " "
        arrow = ">" if lesson is upcoming else " "
        print(f" {arrow}[{tick}] {number:>3}  {lesson.title}")
    print("\n[x] finished   > next up   (optional tracks are listed after the core path)")
    return 0


COMMANDS = {
    "next": cmd_next,
    "check": cmd_check,
    "hint": cmd_hint,
    "status": cmd_status,
    "list": cmd_list,
    "tracks": cmd_tracks,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m learn", description="Your guide through the Learn-Python exercises.")
    sub = parser.add_subparsers(dest="command")
    nxt = sub.add_parser("next", help="show what to do next (the default)")
    nxt.add_argument("track", nargs="?", help="an optional track to continue instead of the core path (see 'tracks')")
    for name, text in (("check", "run the checks for a lesson"), ("hint", "reveal the next hint for a lesson")):
        p = sub.add_parser(name, help=text)
        p.add_argument("lesson", nargs="?", help="a number from 'list', a lesson id, or a word from its name (default: the next lesson)")
    sub.add_parser("status", help="your progress, module by module")
    sub.add_parser("list", help="every lesson, with the finished ones ticked")
    sub.add_parser("tracks", help="the optional tracks and your progress in each")
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
