def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import json
import os
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Talk to our own computer directly, even if a proxy is configured for the internet.
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, status, body, content_type="application/json"):
        raw = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/hello":
            self._send(200, json.dumps({"message": "hi", "numbers": [1, 2, 3]}))
        elif self.path == "/secret":
            token = self.headers.get("X-Token", "")
            self._send(200 if token == "abc123" else 401, f"token={token}", "text/plain")
        elif self.path == "/broken":
            self._send(500, json.dumps({"error": "boom"}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        kind = self.headers.get("Content-Type", "")
        self._send(201, json.dumps({"received": json.loads(body), "content_type": kind}))


@contextmanager
def _server():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_get_json_parses_the_reply():
    with _server() as base:
        result = _fn("get_json")(base + "/hello")
    assert result == {"message": "hi", "numbers": [1, 2, 3]}, f"get_json should return the parsed JSON but returned {result!r}."


def test_post_json_sends_a_json_body():
    with _server() as base:
        result = _fn("post_json")(base + "/echo", {"text": "buy milk", "done": False})
    assert result["received"] == {"text": "buy milk", "done": False}, f"The server should have received your data as JSON, but it received {result['received']!r}."


def test_post_json_sets_the_content_type():
    with _server() as base:
        result = _fn("post_json")(base + "/echo", {"a": 1})
    assert result["content_type"] == "application/json", (
        f"The Content-Type header should be 'application/json' but the server saw {result['content_type']!r}."
    )


def test_get_status_for_success_and_errors():
    with _server() as base:
        status = _fn("get_status")
        assert status(base + "/hello") == 200, "A successful request should give 200."
        assert status(base + "/missing") == 404, "A missing page should give 404, not an exception. Catch urllib.error.HTTPError and return error.code."
        assert status(base + "/broken") == 500, "A server error should give 500, not an exception."


def test_get_with_header_sends_the_header():
    with _server() as base:
        good = _fn("get_with_header")(base + "/secret", "X-Token", "abc123")
    assert good == "token=abc123", f"The server should have received the X-Token header and answered 'token=abc123', but the reply was {good!r}."
