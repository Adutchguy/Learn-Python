import json
from http.server import BaseHTTPRequestHandler


def make_handler():
    notes = {}
    counter = {"next_id": 1}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send_json(self, status, data):
            body = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def not_found(self):
            self.send_json(404, {"error": "not found"})

        def note_id(self):
            parts = self.path.strip("/").split("/")
            if len(parts) == 2 and parts[0] == "notes" and parts[1].isdigit():
                return int(parts[1])
            return None

        def do_GET(self):
            if self.path == "/notes":
                self.send_json(200, [{"id": i, "text": notes[i]} for i in sorted(notes)])
                return
            number = self.note_id()
            if number is not None and number in notes:
                self.send_json(200, {"id": number, "text": notes[number]})
            else:
                self.not_found()

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)  # always read the body, even if we then refuse it
            if self.path != "/notes":
                self.not_found()
                return
            try:
                data = json.loads(raw)
            except ValueError:
                self.send_json(400, {"error": "body must be valid JSON"})
                return
            text = data.get("text") if isinstance(data, dict) else None
            if not isinstance(text, str) or not text.strip():
                self.send_json(400, {"error": "a non-empty text is required"})
                return
            number = counter["next_id"]
            counter["next_id"] += 1
            notes[number] = text
            self.send_json(201, {"id": number, "text": text})

        def do_DELETE(self):
            number = self.note_id()
            if number is not None and number in notes:
                del notes[number]
                self.send_response(204)
                self.end_headers()
            else:
                self.not_found()

    return Handler
