# Running Other Programs with subprocess

*Optional track: Automation and Scripting · about 22 minutes*

## Why this matters

Python can do a lot, but sometimes the right tool is another program: `git`, `ffmpeg`, a compiler, a shell command. The `subprocess` module starts another program from your code, waits for it, and gives you its output and its success or failure. That makes Python a great "glue" language for automation.

This lesson runs on your own computer, because browsers cannot start other programs.

## The idea

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "print('hi from a child')"],   # the command, as a LIST of words
    capture_output=True,                                   # collect stdout and stderr
    text=True,                                             # as text, not bytes
)
print(result.returncode)   # 0 means success
print(result.stdout)       # 'hi from a child\n'
print(result.stderr)       # '' (anything the program printed to standard error)
```

- **The command is a list**: the program first, then each argument as its own item. `sys.executable` is the path of the Python that is running your code, so it works on every computer.
- **`returncode`** is the exit status: `0` is success, anything else is failure. `check=True` turns a failure into a `CalledProcessError` exception.
- **`timeout=5`** raises `subprocess.TimeoutExpired` if the program takes longer than 5 seconds.
- A program that does not exist raises `FileNotFoundError`.

**Safety: avoid `shell=True`.** With a list and the default `shell=False`, each item is passed to the program untouched. If you build one string from user input and run it through a shell, a name like `x; rm -rf ~` can run extra commands. Keep input as separate list items and the problem cannot happen.

## Try it

Run `[sys.executable, "--version"]` with `capture_output=True, text=True` and print the stdout. Then run `[sys.executable, "-c", "raise SystemExit(3)"]` and print its `returncode`.

## Your turn

- `run(command)`: run the command (a list) and return `(returncode, stdout)`.
- `python_version()`: the text Python prints for `--version` (for example `"Python 3.12.1"`), stripped of surrounding whitespace.
- `run_or_none(command, timeout)`: return the program's stripped output, or `None` if it takes longer than `timeout` seconds or the program does not exist.
- `echo_safely(text)`: run a child Python program that prints the text it receives as an argument, and return what it printed (stripped). The text must be passed as a separate argument, never put into a command string.

## Recap

- `subprocess.run([...], capture_output=True, text=True)` runs a program and collects its output.
- `returncode` 0 means success; `check=True` raises on failure; `timeout=` guards against hangs.
- Pass arguments as a list and leave `shell=False`, so input can never become a command.

## Common mistakes

- **Passing one big string** instead of a list (it only works with `shell=True`, which is risky).
- **Ignoring the return code,** and carrying on after the program failed.
- **Running with no timeout** and hanging forever when the other program stalls.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/12-automation/03-running-other-programs
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

run: result = subprocess.run(command, capture_output=True, text=True). The command is a list such as [sys.executable, "-c", "print(1)"]. Return (result.returncode, result.stdout).

</details>

<details><summary>Hint 2</summary>

run_or_none: wrap subprocess.run(command, capture_output=True, text=True, timeout=timeout) in try/except. Catch subprocess.TimeoutExpired and FileNotFoundError and return None; otherwise return the stripped stdout. python_version: run [sys.executable, "--version"] and return the output text, stripped.

</details>

<details><summary>Hint 3</summary>

echo_safely: pass the text as its own list item: [sys.executable, "-c", "import sys; print(sys.argv[1])", text]. Because it is a separate argument (and shell=False is the default), characters like ; or $ in the text are just text, never commands.

</details>
