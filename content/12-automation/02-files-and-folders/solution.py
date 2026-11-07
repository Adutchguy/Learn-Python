import shutil
from pathlib import Path


def files_by_extension(folder):
    groups = {}
    for item in Path(folder).iterdir():
        if item.is_file():
            groups.setdefault(item.suffix.lower(), []).append(item.name)
    return {ext: sorted(names) for ext, names in groups.items()}


def big_files(folder, min_bytes):
    folder = Path(folder)
    found = [
        path.relative_to(folder).as_posix()
        for path in folder.rglob("*")
        if path.is_file() and path.stat().st_size >= min_bytes
    ]
    return sorted(found)


def total_size(folder):
    return sum(path.stat().st_size for path in Path(folder).rglob("*") if path.is_file())


def copy_matching(src, dst, extension):
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    for path in Path(src).iterdir():
        if path.is_file() and path.suffix.lower() == extension.lower():
            shutil.copy2(path, dst / path.name)
            copied.append(path.name)
    return sorted(copied)
