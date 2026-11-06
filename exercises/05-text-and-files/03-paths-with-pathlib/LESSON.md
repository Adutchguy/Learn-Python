# Paths and Folders with pathlib

*Text and Files · about 15 minutes*

## Why this matters

Programs need to find files and folders, build paths, check what exists, and list what is in a directory. Joining paths with plain strings (`"data" + "/" + "x.txt"`) breaks on Windows. The **`pathlib`** module gives paths that work everywhere and read nicely.

## The idea

```python
from pathlib import Path

folder = Path("notes")
file = folder / "todo.txt"        # the / operator joins path pieces
print(file)                       # notes/todo.txt  (notes\todo.txt on Windows)

file.name       # 'todo.txt'
file.stem       # 'todo'
file.suffix     # '.txt'
file.parent     # Path('notes')

folder.mkdir(exist_ok=True)       # create the folder (no error if it exists)
file.write_text("buy milk\n")     # write a whole file in one line
print(file.read_text())           # read a whole file in one line
print(file.exists())              # True

for item in folder.glob("*.txt"): # every match for a pattern
    print(item.name)
```

`Path.iterdir()` lists everything in a folder, and `glob("*.txt")` lists only the matches. Neither guarantees an order, so use `sorted(...)` when order matters. A `Path` works anywhere `open()` expects a filename.

## Try it

Make a folder, put three `.txt` files and one `.csv` file in it with `write_text`, and print the names of just the text files, sorted.

## Your turn

Write three functions. Each is given a folder or path (the checks use temporary ones):

- `notes_path(folder, name)`: the path of the file called `name` plus `.txt` inside `folder`. Return a `Path`.
- `list_text_files(folder)`: the **names** of the `.txt` files in the folder, sorted, as a list of strings.
- `copy_text(source, destination)`: copy the text from one file into another. The destination's folder may not exist yet: create it.

## Recap

- `Path("a") / "b.txt"` builds paths safely; `.name`, `.stem`, `.suffix`, `.parent` take them apart.
- `.exists()`, `.mkdir()`, `.read_text()`, `.write_text()` and `.glob()` cover most jobs.
- Sort listings when order matters.

## Common mistakes

- **Building paths by hand** with `"/"` or `"\\"` in strings.
- **Assuming listing order.** It differs between computers.
- **`mkdir` on an existing folder** raises `FileExistsError` unless you pass `exist_ok=True`.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/05-text-and-files/03-paths-with-pathlib
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

notes_path: Path(folder) / f"{name}.txt". The / operator joins path pieces correctly on every operating system.

</details>

<details><summary>Hint 2</summary>

list_text_files: use Path(folder).glob("*.txt") to find the matching files, take each one's .name, and return sorted(names).

</details>

<details><summary>Hint 3</summary>

copy_text: text = Path(source).read_text() and then Path(destination).write_text(text). Create the destination's folder first if it might not exist: destination.parent.mkdir(exist_ok=True).

</details>
