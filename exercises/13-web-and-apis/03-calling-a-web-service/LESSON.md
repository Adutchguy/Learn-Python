# Calling a Web Service with urllib

*Optional track: Web and APIs · about 24 minutes*

## Why this matters

Time to talk to a real server. Python's standard library can make web requests with no extra packages, using `urllib.request`. (Many people install the friendlier `requests` package later; everything you learn here carries over.) You will make **GET** and **POST** requests, send headers, and handle the errors that real networks produce.

This lesson runs on your own computer, because browsers cannot make arbitrary network connections from Python. The checks start a small web server on your own machine and talk to that, so no internet is needed.

## The idea

```python
import json
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:8000/hello", timeout=5) as response:
    print(response.status)                         # 200
    body = response.read().decode("utf-8")         # bytes -> text
    data = json.loads(body)
```

- **Always set a `timeout`.** Without one a stalled server can hang your program for ever.
- The body arrives as **bytes**; `.decode("utf-8")` makes text.
- `with` closes the connection for you.

**POST with a JSON body.** Build a `Request` object to say more than "GET this URL":

```python
payload = json.dumps({"text": "buy milk"}).encode("utf-8")      # text -> bytes
request = urllib.request.Request(
    "http://127.0.0.1:8000/notes",
    data=payload,                                    # giving data makes it a POST
    headers={"Content-Type": "application/json"},    # tell the server it is JSON
    method="POST",
)
with urllib.request.urlopen(request, timeout=5) as response:
    created = json.loads(response.read())
```

**Errors.** urllib raises an exception for 4xx and 5xx responses:

```python
import urllib.error

try:
    urllib.request.urlopen(url, timeout=5)
except urllib.error.HTTPError as error:       # the server answered with an error status
    print(error.code)                         # 404
except urllib.error.URLError as error:        # could not reach the server at all
    print("network problem:", error.reason)
```

`HTTPError` is a kind of `URLError`, so catch it first. You can also read the error body with `error.read()`.

**Be a good citizen:** respect an API's rate limits, never put secret keys in code you share, and use `https://` for anything real.

## Try it

Start a throwaway server in one terminal with `python -m http.server 8000`, then fetch `http://127.0.0.1:8000/` with `urlopen` in another and print the first 100 characters of the body. Ask for `/nope` and watch the `HTTPError`.

## Your turn

Write four functions. They are checked against a small server running on your own computer.

- `get_json(url)`: GET the URL and return the parsed JSON.
- `post_json(url, data)`: POST `data` as a JSON body (with the `Content-Type: application/json` header) and return the parsed JSON reply.
- `get_status(url)`: return the status code, **including** error statuses like 404 (do not let the exception escape).
- `get_with_header(url, name, value)`: GET the URL with that extra request header and return the response text.

## Recap

- `urlopen(url, timeout=...)` makes a GET; `Request(url, data=..., headers=..., method=...)` describes anything more.
- Bodies are bytes: `.encode()` going out, `.decode()` coming in; `json.dumps` / `json.loads` for JSON.
- `HTTPError` means the server replied with an error status (`.code`); `URLError` means it could not be reached.
- Always set a timeout.

## Common mistakes

- **No timeout,** so one unresponsive server freezes the script.
- **Forgetting `.encode()`** on a POST body: `data` must be bytes.
- **Catching `URLError` before `HTTPError`,** which hides the status code.

## How to check your work

Edit `exercise.py` in this folder, then run this from the repository root:

```
pytest exercises/13-web-and-apis/03-calling-a-web-service
```

## Stuck? Hints

Try each hint in order, one at a time.

<details><summary>Hint 1</summary>

get_json: with urllib.request.urlopen(url, timeout=5) as response: body = response.read().decode("utf-8"); return json.loads(body). response.status is the status code.

</details>

<details><summary>Hint 2</summary>

post_json: build the bytes with json.dumps(data).encode("utf-8"). request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST"). Then open it like get_json and parse the reply.

</details>

<details><summary>Hint 3</summary>

get_status: wrap urlopen in try/except urllib.error.HTTPError as error: for a 404 or 500, urllib raises HTTPError, and error.code holds the status. On success return response.status. get_with_header: Request(url, headers={name: value}) sends your own header; return the response text.

</details>
