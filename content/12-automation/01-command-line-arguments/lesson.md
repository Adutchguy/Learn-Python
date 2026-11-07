---
title: "Command-Line Programs with argparse"
minutes: 22
prereqs: ["05-text-and-files/02-reading-and-writing-files"]
concepts: ["argparse", "sys.argv", "positional argument", "option", "flag", "type=int", "default", "exit code", "SystemExit"]
local_only: false
hints:
  - "build_parser: parser = argparse.ArgumentParser(description=...). parser.add_argument(\"path\") adds the required positional argument. parser.add_argument(\"-n\", \"--limit\", type=int, default=5) adds an option, and parser.add_argument(\"-v\", \"--verbose\", action=\"store_true\") adds a flag that is False unless given. Return the parser."
  - "main: args = build_parser().parse_args(argv). args.path, args.limit and args.verbose hold the values. Open the file with open(args.path) inside try/except FileNotFoundError; on an error print to sys.stderr (print(..., file=sys.stderr)) and return 1."
  - "To show the first limit lines: lines = file.read().splitlines()[:args.limit], then print each one. When verbose is on, first print a line saying which file you are reading. Return 0 when everything worked."
---

## Why this matters

The most useful scripts are the ones you can point at different inputs without editing the code: `tidy.py ~/Downloads`, `backup.py --dry-run`. Programs like that take **command-line arguments**. Python's `argparse` module reads them, checks them, converts types and writes the `--help` text for you.

## The idea

```python
import argparse

parser = argparse.ArgumentParser(description="Show the first lines of a file.")
parser.add_argument("path")                                   # required, by position
parser.add_argument("-n", "--limit", type=int, default=5)     # optional value
parser.add_argument("-v", "--verbose", action="store_true")   # flag: False unless given

args = parser.parse_args()
print(args.path, args.limit, args.verbose)
```

Run as `python head.py notes.txt -n 3 --verbose` and you get `notes.txt 3 True`. Things argparse does for you:

- `--help` prints a usage message built from your arguments.
- A missing argument, or `-n abc` where a number is required, prints a clear error and **exits** with status 2.
- `type=int` converts the text to a number; `default=` fills in what was not given.

`parse_args()` reads `sys.argv`, the list of words typed after `python`. For testing, pass a list instead: `parser.parse_args(["notes.txt", "-n", "3"])`. That is how this lesson's checks run your code, without a real terminal.

**Exit codes.** A program tells the shell whether it worked through its exit status: `0` means success, anything else means failure. Put your logic in a `main(argv=None)` function that returns the code, and finish the script with:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

Print error messages to **standard error** (`print("oops", file=sys.stderr)`), so they stay out of the normal output when someone redirects it.

## Try it

Make a parser with one positional argument and one `--times` option with `type=int`. Call `parse_args(["hi", "--times", "3"])` and print the result.

## Your turn

Build a tiny version of the Unix `head` command.

- `build_parser()`: returns an `ArgumentParser` with a positional `path`, an option `-n` / `--limit` (a whole number, default 5) and a flag `-v` / `--verbose`.
- `main(argv=None)`: parse `argv`, print the first `limit` lines of the file, and return `0`. If the file does not exist, print a message to standard error and return `1`. With `--verbose`, first print a line starting with `Reading ` and the path.

## Recap

- `add_argument("name")` is required and positional; `add_argument("-n", "--name", ...)` is an option; `action="store_true"` makes a flag.
- `type=` converts, `default=` fills in, and `--help` is free.
- Pass a list to `parse_args` to test without a terminal.
- Return an exit code from `main`: 0 for success, non-zero for failure; errors go to stderr.

## Common mistakes

- **Reading `sys.argv` by hand** and rebuilding what argparse already does.
- **Forgetting `type=int`,** so the value is the text `"5"` and `lines[:"5"]` fails.
- **Printing errors to normal output,** which mixes them into the results other programs read.
