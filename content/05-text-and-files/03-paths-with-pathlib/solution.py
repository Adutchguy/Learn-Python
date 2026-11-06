from pathlib import Path


def notes_path(folder, name):
    return Path(folder) / f"{name}.txt"


def list_text_files(folder):
    return sorted(path.name for path in Path(folder).glob("*.txt"))


def copy_text(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(Path(source).read_text())
