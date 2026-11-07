---
title: "How the Web Talks: URLs, Requests and Status Codes"
minutes: 20
prereqs: ["05-text-and-files/05-json-data"]
concepts: ["HTTP", "URL", "urllib.parse", "query string", "status code", "HTTPStatus", "headers"]
local_only: false
hints:
  - "parse_url: parts = urlsplit(url). The pieces are parts.scheme, parts.hostname and parts.path. parse_qs(parts.query) gives a dict of LISTS, so take the first value of each: {key: values[0] for key, values in ...items()}."
  - "build_url: urlencode(params) turns a dict into \"q=py+thon&page=2\". Join it on: f\"{base}{path}?{query}\". If params is empty, return just base + path with no question mark."
  - "status_kind: compare ranges with // 100 (code // 100 == 2 means success). status_phrase: HTTPStatus(code).phrase raises ValueError for an unknown code, so catch it. parse_headers: split the raw text with splitlines(), then line.partition(\":\") gives (name, colon, value); store name.strip().lower() and value.strip()."
---

## Why this matters

Every time you open a web page, check the weather in an app or ask a voice assistant a question, programs are talking to each other over **HTTP**. To use or build web services you need to know the vocabulary: URLs, requests, responses, status codes and headers. Python's standard library handles all the plumbing, so you can focus on the ideas.

## The idea

A **URL** has parts:

```text
https://api.example.com:8080/search/books?q=python&page=2
└─┬──┘   └──────┬──────┘└─┬─┘└────┬─────┘└──────┬───────┘
scheme        host     port   path          query string
```

```python
from urllib.parse import urlsplit, parse_qs, urlencode

parts = urlsplit("https://api.example.com/search/books?q=python&page=2")
parts.scheme        # 'https'
parts.hostname      # 'api.example.com'
parts.path          # '/search/books'
parse_qs(parts.query)       # {'q': ['python'], 'page': ['2']}   (values are LISTS)

urlencode({"q": "py thon", "page": 2})     # 'q=py+thon&page=2'  (spaces and symbols made safe)
```

Never join query strings by hand: `urlencode` correctly escapes spaces, `&`, `#` and non-English characters.

**A conversation** has two halves. The client sends a **request**: a method (`GET` to read, `POST` to create, `PUT`/`PATCH` to change, `DELETE` to remove), a path, **headers** and sometimes a body. The server sends a **response**: a **status code**, headers and usually a body (often JSON).

**Status codes** tell you what happened, by their first digit:

| Range | Meaning | Examples |
|---|---|---|
| 2xx | success | 200 OK, 201 Created, 204 No Content |
| 3xx | redirect | 301 Moved Permanently, 304 Not Modified |
| 4xx | the **client** made a mistake | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | the **server** has a problem | 500 Internal Server Error, 503 Service Unavailable |

```python
from http import HTTPStatus
HTTPStatus(404).phrase      # 'Not Found'
```

**Headers** are `Name: value` lines, such as `Content-Type: application/json`. Names are not case-sensitive, so programs usually lower-case them.

## Try it

Use `urlsplit` on a URL with a query string and print each part. Build a URL with `urlencode` using a value that contains a space and an `&`.

## Your turn

Write five functions:

- `parse_url(url)`: a dict with `"scheme"`, `"host"`, `"path"` and `"query"` (a dict of each query key to its **first** value, as text).
- `build_url(base, path, params)`: `base + path`, followed by `?` and the encoded `params` when there are any.
- `status_kind(code)`: `"informational"` (1xx), `"success"` (2xx), `"redirect"` (3xx), `"client error"` (4xx), `"server error"` (5xx), or `"unknown"`.
- `status_phrase(code)`: the standard phrase (`"Not Found"` for 404), or `"Unknown"` for a code that does not exist.
- `parse_headers(raw)`: turn header text (lines of `Name: value`) into a dict with lower-case names and stripped values.

## Recap

- A URL is scheme, host, path and query; use `urlsplit`, `parse_qs` and `urlencode` instead of string tricks.
- Methods say what to do (GET, POST, PUT, DELETE); status codes say what happened; headers carry details.
- 2xx success, 3xx redirect, 4xx you did something wrong, 5xx the server failed.

## Common mistakes

- **Building query strings by hand** and breaking on spaces and `&`.
- **Forgetting that `parse_qs` returns lists.**
- **Treating every non-200 as an error.** 201, 204 and redirects are normal outcomes.
