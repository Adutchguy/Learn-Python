from http import HTTPStatus
from urllib.parse import parse_qs, urlencode, urlsplit


def parse_url(url):
    parts = urlsplit(url)
    query = {key: values[0] for key, values in parse_qs(parts.query).items()}
    return {"scheme": parts.scheme, "host": parts.hostname, "path": parts.path, "query": query}


def build_url(base, path, params):
    url = base + path
    if params:
        url += "?" + urlencode(params)
    return url


def status_kind(code):
    kinds = {1: "informational", 2: "success", 3: "redirect", 4: "client error", 5: "server error"}
    return kinds.get(code // 100, "unknown")


def status_phrase(code):
    try:
        return HTTPStatus(code).phrase
    except ValueError:
        return "Unknown"


def parse_headers(raw):
    headers = {}
    for line in raw.splitlines():
        name, colon, value = line.partition(":")
        if colon:
            headers[name.strip().lower()] = value.strip()
    return headers
