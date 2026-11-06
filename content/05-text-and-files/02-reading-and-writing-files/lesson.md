---
title: "Reading and Writing Text Files"
minutes: 18
prereqs: ["05-text-and-files/01-string-methods"]
concepts: ["open", "with", "read", "write", "append", "readlines", "file mode", "newline"]
local_only: false
hints:
  - "save_lines: open the path with 'w' using a with block, then write every line followed by a newline character: file.write(line + \"\\n\")."
  - "load_lines: inside with open(path) as file:, loop for line in file: and collect line.rstrip(\"\\n\") into a list, then return the list. Return it after the with block."
  - "append_line: the mode 'a' adds to the end of an existing file instead of replacing it. Write line + \"\\n\"."
---

## Why this matters

Variables vanish when your program ends. **Files** are how programs remember: saved documents, logs, settings, data to analyse. Reading and writing text files takes only a few lines.

## The idea

```python
with open("notes.txt", "w") as file:   # "w" = write (creates or replaces the file)
    file.write("first line\n")
    file.write("second line\n")

with open("notes.txt") as file:        # default mode is "r" = read
    for line in file:
        print(line.rstrip("\n"))       # each line still ends with "\n"
```

- **`with open(...) as file:`** opens the file and **closes it automatically** when the block ends, even if something goes wrong. Always use it.
- Modes: `"r"` read (the default), `"w"` write (erases existing content), `"a"` append (adds to the end).
- `file.write(text)` writes exactly what you give it. It does **not** add a newline, so add `"\n"` yourself.
- `file.read()` returns the whole text; looping over `file` gives one line at a time (including its `"\n"`).

Reading a file that does not exist is a `FileNotFoundError`. (A later lesson shows how to handle errors gracefully.)

## Try it

Write three lines to a file, then read them back and print them with line numbers using `enumerate`. Open the file again in `"a"` mode and add a fourth line.

## Your turn

The checks give your functions a file path (so they never touch your own files). Write three functions:

- `save_lines(path, lines)`: write each string in `lines` on its own line, replacing any existing content.
- `load_lines(path)`: return the lines of the file as a list of strings **without** the trailing newline characters.
- `append_line(path, line)`: add one line to the end of the file, keeping what was there.

## Recap

- `with open(path, mode) as file:` opens a file and always closes it.
- `"r"` reads, `"w"` replaces, `"a"` appends; `write` needs explicit `"\n"`.
- Iterate over a file to get lines, and `rstrip("\n")` to remove the line ending.

## Common mistakes

- **Opening with `"w"` when you meant `"a"`**, which erases the file.
- **Forgetting `"\n"`**, so every line is joined into one.
- **Using the file after the `with` block**, when it is already closed (`ValueError: I/O operation on closed file`).
