---
title: "Working with JSON APIs"
minutes: 24
prereqs: ["13-web-and-apis/01-how-http-works"]
concepts: ["API", "JSON", "nested data", "safe lookup", "pagination", "error handling", "dependency injection"]
local_only: false
hints:
  - "extract_names: data = json.loads(response_text); the people are in data[\"results\"], and each one has a \"name\". A list comprehension does it: [item[\"name\"] for item in data[\"results\"]]."
  - "safe_get: start with current = data. For each key: if current is a dict and the key is in it, step into it (current = current[key]); otherwise return default. After all keys return current. A value of None in the middle should also give the default."
  - "all_pages: page = 1; loop while page is not None: response = fetch_page(page); items.extend(response[\"items\"]); page = response[\"next_page\"]. Stop with an error after max_pages to avoid looping forever. describe_error: json.loads can fail, so wrap it in try/except ValueError and fall back to the plain text."
---

## Why this matters

An **API** (application programming interface) is a way for programs to ask other programs for data. Most web APIs answer in **JSON**: weather forecasts, maps, payments, and the data behind your favourite apps. Working with them well means three skills: reading nested data safely, collecting results spread over many pages, and handling errors without crashing.

You do not need a live server to practise these skills. The functions below work on the *text* an API returns, and take the page-fetching function as a parameter so they can be checked instantly. The next lesson makes real calls.

## The idea

**Parse and dig.** An API response is text. `json.loads` turns it into dicts and lists, and then you dig in:

```python
import json

text = '{"results": [{"name": "Ada", "stats": {"wins": 3}}, {"name": "Bo", "stats": null}]}'
data = json.loads(text)
data["results"][0]["name"]           # 'Ada'
data["results"][1]["stats"]["wins"]  # TypeError: stats is None!
```

Real data has holes: missing keys and `null` values. **Defensive lookups** avoid crashes:

```python
data["results"][0].get("stats", {}).get("wins", 0)    # .get with a default
```

**Pagination.** APIs rarely send everything at once. They send a *page* and tell you where the next one is:

```python
{"items": [1, 2, 3], "next_page": 2}      # ... and the last page has "next_page": null
```

To collect everything you loop until there is no next page. Add a **safety limit** so a buggy server cannot keep you looping for ever.

**Errors.** A response has a status code and a body. For a 4xx or 5xx the body often explains what went wrong, usually as JSON like `{"message": "Rate limit exceeded"}`, but not always: it might be plain text or HTML. So parse carefully and fall back gracefully.

**Passing the fetching function in.** Instead of writing `requests.get(...)` inside your code, accept a function `fetch_page(page_number)` as a parameter. In real use you pass a function that calls the network; in checks you pass a tiny fake. Your logic works the same, and the checks run in microseconds.

## Try it

Parse the JSON text above. Print the first name. Then use `.get("stats", {})` safely on the second person, whose stats are `null`.

(Hint: `.get("stats", {})` returns the default only when the key is *missing*. If the value is `None`, use `or {}` as well.)

## Your turn

Write four functions:

- `extract_names(response_text)`: the names from `{"results": [{"name": ...}, ...]}`, as a list.
- `safe_get(data, *keys, default=None)`: follow the keys one after another into nested dicts. If any key is missing, or any step along the way is not a dict (for example `None`), return `default`.
- `all_pages(fetch_page, max_pages=100)`: call `fetch_page(1)`, then the page given by each response's `"next_page"`, until it is `None`. Return all the `"items"` in one list. If more than `max_pages` pages would be needed, raise `RuntimeError`.
- `describe_error(status, body)`: a short message for the user: `"OK"` for 2xx; for 4xx, `"Request problem (<status>): <message>"` using the `"message"` from a JSON body, or the body text itself when it is not JSON; for 5xx, `"Server problem (<status>): try again later"`.

## Recap

- `json.loads` gives dicts and lists; dig in defensively with `.get` or a helper like `safe_get`.
- Pagination means looping until there is no next page, with a limit as a safety net.
- Error bodies are not always JSON; parse them in `try/except`.
- Taking the fetch function as a parameter makes network code easy to test.

## Common mistakes

- **Assuming every key exists.** One missing field crashes the whole run.
- **`.get("x", {})` when the value is `null`.** The key exists, so you get `None`, not `{}`.
- **Looping on `next_page` without a limit.**
