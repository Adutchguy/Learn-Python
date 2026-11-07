---
title: "Project: Build a Tiny JSON API"
minutes: 40
prereqs: ["13-web-and-apis/03-calling-a-web-service"]
concepts: ["project", "http.server", "BaseHTTPRequestHandler", "REST", "routes", "status codes", "JSON API"]
local_only: true
hints:
  - "Use a closure: make_handler() creates notes = {} and a counter, then defines class Handler(BaseHTTPRequestHandler) inside it (so its methods can use them) and returns Handler. Add a helper method send_json(self, status, data) that does send_response, the Content-Type and Content-Length headers, end_headers, then writes json.dumps(data).encode(). Override log_message to do nothing."
  - "do_GET: split self.path. \"/notes\" returns a list of {\"id\", \"text\"} sorted by id. \"/notes/<id>\" returns that note, or 404 {\"error\": \"not found\"}. do_DELETE for \"/notes/<id>\" removes it and answers 204 with no body (send_response(204); end_headers()), or 404 if it does not exist."
  - "do_POST: read the body first, whatever the path: length = int(self.headers.get(\"Content-Length\", 0)); raw = self.rfile.read(length). Then for \"/notes\" parse with json.loads inside try/except ValueError. If it is not a JSON object with a non-empty text string, answer 400 {\"error\": ...}. Otherwise store the note under the next id and answer 201 with the new note."
---

## Why this matters

You have used web services. Now you will **build one**. With just the standard library you can write a real HTTP server that speaks JSON, the same shape as the APIs behind most apps. You will practise routing (which path means what), status codes (`201`, `204`, `400`, `404`) and careful input checking.

This project runs on your own computer: the checks start your server and talk to it.

## The idea

You are building a **notes service**:

| Request | What it does | Response |
|---|---|---|
| `GET /notes` | list all notes | `200` and a JSON list of `{"id": 1, "text": "..."}` ordered by id |
| `POST /notes` with `{"text": "buy milk"}` | create a note | `201` and the new note `{"id": 1, "text": "buy milk"}` |
| `GET /notes/1` | read one note | `200` and the note, or `404` |
| `DELETE /notes/1` | delete a note | `204` (no body), or `404` |
| anything else | | `404` and `{"error": "not found"}` |

A bad `POST` (not valid JSON, not an object, or no non-empty `"text"`) gets `400` and `{"error": "..."}`.

The standard library gives you the server:

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):                      # called for every GET request
        body = b'{"hello": "world"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

Inside a handler, `self.path` is the request path, `self.headers` the request headers, and `self.rfile` the incoming body (read exactly `Content-Length` bytes). Methods `do_GET`, `do_POST` and `do_DELETE` handle those verbs.

Make the handler share state (the notes) by building the class inside a function that owns the notes: a **closure**.

## Try it

Run the little server above, then visit `http://127.0.0.1:8000/` in your browser or call it with `urllib`. Stop it with Ctrl+C.

## Your turn

Write one function, `make_handler()`, that creates an empty set of notes and returns a `BaseHTTPRequestHandler` subclass implementing the table above. The first note has id `1`, the next `2`, and so on; ids are never reused after a delete. The checks create a `ThreadingHTTPServer` with your handler and talk to it with `urllib`.

## Recap

- `BaseHTTPRequestHandler` plus `do_GET` / `do_POST` / `do_DELETE` is a complete (if basic) web server.
- Choose status codes on purpose: `201` created, `204` no content, `400` bad input, `404` not found.
- Never trust input: parse it carefully and answer clearly when it is wrong.
- A closure lets the handler share state without globals.

## Going further

Add `PUT /notes/<id>` to edit a note, save the notes to a JSON file so they survive a restart, or try the same service with a framework such as Flask or FastAPI to see what they add. This hand-written version shows what they do for you.
