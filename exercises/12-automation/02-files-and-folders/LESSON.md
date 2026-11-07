# Working with Files and Folders in Bulk

*Optional track: Automation and Scripting · about 24 minutes*

## Why this matters

Renaming 200 photos, sorting a messy Downloads folder, finding the biggest files eating your disk: jobs like these take minutes in Python and hours by hand. You already know `pathlib` for single paths. This lesson adds **looping over folders** and the **`shutil`** module for copying and moving.

## The idea

```python
from pathlib import Path
import shutil

folder = Path("photos")

for item in folder.iterdir():          # everything directly inside the folder
    if item.is_file():
        print(item.name, item.suffix, item.stat().st_size)   # name, ".jpg", bytes

folder.rglob("*.jpg")                  # every .jpg in the folder AND its subfolders
folder.glob("*.jpg")                   # only directly inside the folder
```

Useful facts about a path: `.name` (`"cat.jpg"`), `.stem` (`"cat"`), `.suffix` (`".jpg"`), `.parent`, `.is_file()`, `.is_dir()`, `.exists()`, and `.stat().st_size` (size in bytes). Compare suffixes with `.lower()`, because `PHOTO.JPG` and `photo.jpg` are the same kind of file.

**Copying and moving** (the `shutil` module):

```python
folder.mkdir(parents=True, exist_ok=True)      # create it (and parents) if needed
shutil.copy2("a.txt", "backup/a.txt")          # copy, keeping the timestamps
shutil.move("a.txt", "archive/a.txt")          # move (also renames)
shutil.rmtree("old_folder")                    # delete a whole folder: careful!
```

Safety habits for scripts that change files:

- Do a **dry run** first (print what would happen) before really moving anything.
- Never overwrite silently; check `exists()`.
- Test on a copy of your data, or in a temporary folder, as the checks here do.

`iterdir()` gives paths in no particular order, so `sorted(...)` the results when order matters.

## Try it

In a scratch folder, create a few files with different extensions. Loop over the folder with `iterdir()` and print each file's name and size.

## Your turn

The checks give your functions a temporary folder. Write:

- `files_by_extension(folder)`: a dict of lowercase extension (like `".txt"`, or `""` for none) to the sorted list of file names directly in the folder. Ignore subfolders.
- `big_files(folder, min_bytes)`: the sorted relative paths (like `"sub/big.bin"`) of every file in the folder **and its subfolders** that is at least `min_bytes` big.
- `total_size(folder)`: the total size in bytes of all files in the folder and its subfolders.
- `copy_matching(src, dst, extension)`: create `dst` if needed and copy the files directly inside `src` with that extension (compared in lowercase) into it. Return the sorted list of copied file names.

## Recap

- `iterdir()` lists a folder; `glob` / `rglob` match patterns (`rglob` also searches subfolders).
- `suffix`, `name`, `stem` and `stat().st_size` describe a file.
- `shutil.copy2`, `move` and `rmtree` copy, move and delete; `mkdir(parents=True, exist_ok=True)` creates folders safely.
- Dry-run first, never overwrite silently, and test in a temporary folder.

## Common mistakes

- **Treating folders like files.** `iterdir()` returns both; check `is_file()`.
- **Case-sensitive extensions:** `.JPG` does not equal `.jpg` until you lower-case it.
- **Running a destructive script on real data first.** Print the plan, then act.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/12-automation/02-files-and-folders
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

files_by_extension: loop over Path(folder).iterdir(), skip anything that is not a file (item.is_file()), and group by item.suffix.lower() in a dict of lists. Use "" as the key when there is no suffix. Sort each list at the end.

</details>

<details><summary>Hint 2</summary>

big_files: for path in Path(folder).rglob("*") visits every file in every subfolder. path.stat().st_size is the size in bytes. path.relative_to(folder).as_posix() gives a tidy name like "sub/big.bin". total_size: add up st_size for the files only.

</details>

<details><summary>Hint 3</summary>

copy_matching: Path(dst).mkdir(parents=True, exist_ok=True), then for every file in src (iterdir) whose suffix matches, shutil.copy2(path, Path(dst) / path.name). Return the sorted list of copied names.

</details>
