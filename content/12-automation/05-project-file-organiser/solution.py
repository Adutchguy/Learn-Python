import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".pdf": "Documents",
    ".txt": "Documents",
    ".md": "Documents",
    ".docx": "Documents",
    ".zip": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
}


def category_for(filename):
    return CATEGORIES.get(Path(filename).suffix.lower(), "Other")


def unique_destination(path):
    path = Path(path)
    if not path.exists():
        return path
    number = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({number}){path.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


def plan_moves(folder):
    folder = Path(folder)
    files = sorted((p for p in folder.iterdir() if p.is_file()), key=lambda p: p.name)
    return [(p, folder / category_for(p.name) / p.name) for p in files]


def organise(folder, dry_run=False):
    lines = []
    for source, destination in plan_moves(folder):
        lines.append(f"{source.name} -> {destination.parent.name}")
        if dry_run:
            continue
        destination.parent.mkdir(exist_ok=True)
        shutil.move(source, unique_destination(destination))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sort the files in a folder into category folders.")
    parser.add_argument("folder")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    lines = organise(args.folder, dry_run=args.dry_run)
    for line in lines:
        print(line)
    verb = "would be moved" if args.dry_run else "moved"
    print(f"{len(lines)} file(s) {verb}")
    return 0
