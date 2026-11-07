def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import json
import os
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager
from http.server import ThreadingHTTPServer

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"


@contextmanager
def _api():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _fn("make_handler")())
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def _call(base, method, path, body=None, raw=None):
    """Send a request; return (status, parsed JSON or None)."""
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    headers = {"Content-Type": "application/json"} if data is not None else {}
    request = urllib.request.Request(base + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            text = response.read().decode()
            return response.status, (json.loads(text) if text else None)
    except urllib.error.HTTPError as error:
        text = error.read().decode()
        return error.code, (json.loads(text) if text else None)


def test_starts_empty():
    with _api() as base:
        status, data = _call(base, "GET", "/notes")
    assert (status, data) == (200, []), f"GET /notes on a new service should give 200 and [] but gave {status} and {data!r}."


def test_create_a_note():
    with _api() as base:
        status, data = _call(base, "POST", "/notes", {"text": "buy milk"})
    assert status == 201, f"POST /notes should answer 201 (Created) but answered {status}."
    assert data == {"id": 1, "text": "buy milk"}, f"The reply should be the new note {{'id': 1, 'text': 'buy milk'}} but was {data!r}."


def test_list_and_read_notes():
    with _api() as base:
        _call(base, "POST", "/notes", {"text": "one"})
        _call(base, "POST", "/notes", {"text": "two"})
        status, listing = _call(base, "GET", "/notes")
        one = _call(base, "GET", "/notes/1")
        two = _call(base, "GET", "/notes/2")
    assert listing == [{"id": 1, "text": "one"}, {"id": 2, "text": "two"}], f"GET /notes should list both notes in id order but gave {listing!r}."
    assert one == (200, {"id": 1, "text": "one"}), f"GET /notes/1 should give (200, note 1) but gave {one!r}."
    assert two == (200, {"id": 2, "text": "two"}), f"GET /notes/2 should give (200, note 2) but gave {two!r}."


def test_unknown_note_is_404():
    with _api() as base:
        result = _call(base, "GET", "/notes/99")
    assert result == (404, {"error": "not found"}), f"A note that does not exist should give (404, {{'error': 'not found'}}) but gave {result!r}."


def test_delete_a_note_and_never_reuse_ids():
    with _api() as base:
        _call(base, "POST", "/notes", {"text": "one"})
        _call(base, "POST", "/notes", {"text": "two"})
        deleted = _call(base, "DELETE", "/notes/1")
        again = _call(base, "DELETE", "/notes/1")
        listing = _call(base, "GET", "/notes")
        third = _call(base, "POST", "/notes", {"text": "three"})
    assert deleted == (204, None), f"DELETE should answer 204 with no body but gave {deleted!r}."
    assert again[0] == 404, f"Deleting a note that is already gone should be 404 but was {again[0]}."
    assert listing == (200, [{"id": 2, "text": "two"}]), f"Only note 2 should remain but the list is {listing!r}."
    assert third[1] == {"id": 3, "text": "three"}, f"Ids must never be reused: the next note should have id 3 but is {third[1]!r}."


def test_bad_input_is_400():
    with _api() as base:
        not_json = _call(base, "POST", "/notes", raw=b"this is not json")
        not_object = _call(base, "POST", "/notes", body=[1, 2, 3])
        no_text = _call(base, "POST", "/notes", body={"title": "x"})
        blank = _call(base, "POST", "/notes", body={"text": "   "})
        wrong_type = _call(base, "POST", "/notes", body={"text": 42})
        listing = _call(base, "GET", "/notes")
    for name, result in (("invalid JSON", not_json), ("a JSON list", not_object), ("a missing text", no_text), ("a blank text", blank), ("a text that is not a string", wrong_type)):
        assert result[0] == 400, f"A POST with {name} should answer 400 but answered {result[0]}."
        assert isinstance(result[1], dict) and "error" in result[1], f"The 400 reply for {name} should be JSON with an 'error' message but was {result[1]!r}."
    assert listing == (200, []), "Rejected posts must not create notes."


def test_other_paths_are_404():
    with _api() as base:
        a = _call(base, "GET", "/")
        b = _call(base, "GET", "/notes/abc")
        c = _call(base, "POST", "/other", {"text": "x"})
    for result in (a, b, c):
        assert result == (404, {"error": "not found"}), f"Unknown paths should give (404, {{'error': 'not found'}}) but one gave {result!r}."
