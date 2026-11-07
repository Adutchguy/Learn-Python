---
title: "Project: A File Organiser"
minutes: 35
prereqs: ["12-automation/04-timing-retries-and-schedules"]
concepts: ["project", "pathlib", "shutil.move", "argparse", "dry run", "automation", "collision handling"]
local_only: false
hints:
  - "category_for: look at Path(filename).suffix.lower() and return \"Images\" for .jpg .jpeg .png .gif, \"Documents\" for .pdf .txt .md .docx, \"Archives\" for .zip .tar .gz, and \"Other\" for everything else. A dict of suffix -> category keeps this tidy."
  - "unique_destination: if path does not exist, return it. Otherwise try path.with_name(f\"{path.stem} ({n}){path.suffix}\") for n = 1, 2, 3... until one does not exist. plan_moves: for each file directly in the folder (sorted by name) return (source, folder / category_for(name) / name)."
  - "organise: moves = plan_moves(folder). Unless dry_run, for each move create the category folder with mkdir(exist_ok=True), find a free destination with unique_destination, and shutil.move(source, destination). Return the list of \"name -> Category\" strings (even for a dry run). main: argparse with folder and --dry-run; print each line, then a summary line, and return 0."
---

## Why this matters

Everyone's Downloads folder is a mess. In this project you build a small command-line tool that sorts a folder's files into `Images`, `Documents`, `Archives` and `Other`. It uses everything from this track: arguments, folders and files, and safe habits like a **dry run** and never overwriting.

## The idea

The design is a few small functions, each easy to test:

1. `category_for(filename)`: which category does a file belong to?
2. `unique_destination(path)`: if `photo.jpg` already exists there, use `photo (1).jpg`, then `photo (2).jpg`.
3. `plan_moves(folder)`: work out **what would move where**, without moving anything.
4. `organise(folder, dry_run)`: carry out the plan (or only report it).
5. `main(argv)`: the command line: `organiser.py FOLDER [--dry-run]`.

Separating *planning* from *doing* is what makes a dry run easy and safe: the same plan is either executed or just printed.

```python
from pathlib import Path
import shutil

source = Path("Downloads/cat.JPG")
target = Path("Downloads/Images/cat.JPG")
target.parent.mkdir(exist_ok=True)
shutil.move(source, target)
```

## Try it

In a scratch folder, create `a.jpg`, `b.pdf` and `c.xyz`. Write just `category_for` first and print the category of each name.

## Your turn

Write these five functions:

- `category_for(filename)`: `"Images"` (`.jpg`, `.jpeg`, `.png`, `.gif`), `"Documents"` (`.pdf`, `.txt`, `.md`, `.docx`), `"Archives"` (`.zip`, `.tar`, `.gz`) or `"Other"`. Ignore upper or lower case in the extension.
- `unique_destination(path)`: `path` itself if nothing exists there, otherwise the first free name of the form `name (1).ext`, `name (2).ext`, ...
- `plan_moves(folder)`: a list of `(source, destination)` pairs of `Path`s for the files **directly** in the folder, sorted by file name. The destination is `folder / category / name`. Do not touch folders.
- `organise(folder, dry_run=False)`: carry out the plan, creating category folders as needed and never overwriting (use `unique_destination`). Return a list of strings like `"cat.jpg -> Images"` in plan order. With `dry_run=True`, return the same list but change nothing.
- `main(argv=None)`: arguments `folder` and `--dry-run`. Print each line from `organise`, then a last line `N file(s) moved` (or `N file(s) would be moved` for a dry run). Return `0`.

## Recap

- Plan first, then act: it makes dry runs, testing and undo-thinking easy.
- `pathlib` + `shutil` do the file work; `argparse` makes the script reusable.
- Never overwrite silently; find a free name instead.

## Going further

Add a `--undo` that reads a log of moves and reverses them, or organise by the file's modified date (`path.stat().st_mtime`). Run your tool with a real `cron` job once you trust it.
