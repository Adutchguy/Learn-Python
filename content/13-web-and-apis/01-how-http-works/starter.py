from http import HTTPStatus
from urllib.parse import parse_qs, urlencode, urlsplit


# Write five functions:
#
# def parse_url(url): ...                  {"scheme", "host", "path", "query"}; query maps each key to its FIRST value
# def build_url(base, path, params): ...   base + path + "?" + encoded params (no "?" when params is empty)
# def status_kind(code): ...               "informational", "success", "redirect", "client error", "server error", "unknown"
# def status_phrase(code): ...             "Not Found" for 404, "Unknown" for a code that does not exist
# def parse_headers(raw): ...              "Name: value" lines -> {"name": "value"} with lower-case names
