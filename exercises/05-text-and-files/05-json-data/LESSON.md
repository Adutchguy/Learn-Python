# JSON: Saving Structured Data

*Text and Files · about 15 minutes*

## Why this matters

Lists and dicts are great while your program runs, but how do you save one to a file or send it over the internet? **JSON** is the standard text format for exactly that. Web APIs, settings files and many apps speak it, and it maps almost directly onto Python's dicts, lists, strings, numbers, `True`/`False` and `None`.

## The idea

```python
import json

settings = {"name": "Ada", "scores": [90, 85], "admin": True, "nickname": None}

text = json.dumps(settings)               # Python object -> JSON text (a string)
back = json.loads(text)                   # JSON text -> Python object
print(back == settings)                   # True
```

The `s` stands for "string". The versions without `s` work directly with files:

```python
with open("settings.json", "w") as file:
    json.dump(settings, file, indent=2)   # indent makes it readable

with open("settings.json") as file:
    loaded = json.load(file)
```

JSON uses `true`, `false` and `null` where Python has `True`, `False` and `None`, and the module converts them for you. Keys must be text (a dict key `1` becomes `"1"`), and only basic types are allowed: you cannot save a set, a function or your own objects directly.

`sort_keys=True` makes the output order predictable, which is handy for comparisons.

## Try it

`json.dumps` a dict that contains a list and a `None`. Then `json.loads` it back and print its type. What happens when you try to dump a `set`?

## Your turn

Write three functions (they receive file paths, so the checks can use temporary files):

- `to_json(data)`: the JSON text for `data`, indented by 2 spaces with keys sorted.
- `save_json(path, data)`: write `data` to the file as JSON (indent 2).
- `load_json(path, default)`: read and return the data from the file, or return `default` if the file does not exist.

## Recap

- `json.dumps` / `json.loads` convert to and from text; `json.dump` / `json.load` work with files.
- Only basic types survive: dicts (text keys), lists, text, numbers, booleans and `None`.
- Use `indent=` for people to read and `sort_keys=True` for stable output.

## Common mistakes

- **Mixing up `dump` and `dumps`:** one takes a file, the other returns a string.
- **Expecting tuples or sets back.** Tuples become lists; sets cannot be saved.
- **Loading a missing or empty file**, which is an error: check `exists()` or handle the problem.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/05-text-and-files/05-json-data
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

to_json: json.dumps(data, indent=2, sort_keys=True) gives the pretty, predictable text.

</details>

<details><summary>Hint 2</summary>

save_json: open the path with "w" in a with block and call json.dump(data, file, indent=2). load_json: json.load(file).

</details>

<details><summary>Hint 3</summary>

load_json should return default when the file is missing. Check Path(path).exists() first and return default if it is False.

</details>
