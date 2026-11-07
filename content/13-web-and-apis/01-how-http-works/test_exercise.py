def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def test_parse_url_splits_the_parts():
    result = _fn("parse_url")("https://api.example.com/search/books?q=python&page=2")
    want = {"scheme": "https", "host": "api.example.com", "path": "/search/books", "query": {"q": "python", "page": "2"}}
    assert result == want, f"Expected {want} but got {result}."


def test_parse_url_without_a_query():
    result = _fn("parse_url")("http://localhost:8000/health")
    want = {"scheme": "http", "host": "localhost", "path": "/health", "query": {}}
    assert result == want, f"The host should not include the port, and a missing query is an empty dict. Expected {want} but got {result}."


def test_parse_url_decodes_the_query():
    result = _fn("parse_url")("https://x.org/s?q=py+thon%21")
    assert result["query"] == {"q": "py thon!"}, f"The + and %21 should be decoded to 'py thon!' but the query is {result['query']}."


def test_build_url_encodes_parameters():
    result = _fn("build_url")("https://api.example.com", "/search", {"q": "py thon", "page": 2})
    assert result == "https://api.example.com/search?q=py+thon&page=2", f"Expected 'https://api.example.com/search?q=py+thon&page=2' but got {result!r}."


def test_build_url_escapes_special_characters():
    result = _fn("build_url")("https://x.org", "/s", {"q": "a&b=c"})
    assert result == "https://x.org/s?q=a%26b%3Dc", f"The & and = inside a value must be escaped (use urlencode). Got {result!r}."


def test_build_url_without_parameters_has_no_question_mark():
    result = _fn("build_url")("https://x.org", "/status", {})
    assert result == "https://x.org/status", f"With no parameters there should be no '?' at all but got {result!r}."


def test_status_kind():
    kind = _fn("status_kind")
    cases = {100: "informational", 200: "success", 204: "success", 301: "redirect", 404: "client error", 418: "client error", 500: "server error", 503: "server error", 99: "unknown", 700: "unknown"}
    for code, expected in cases.items():
        assert kind(code) == expected, f"status_kind({code}) should be {expected!r} but returned {kind(code)!r}."


def test_status_phrase():
    phrase = _fn("status_phrase")
    assert phrase(200) == "OK", f"status_phrase(200) should be 'OK' but returned {phrase(200)!r}."
    assert phrase(404) == "Not Found", f"status_phrase(404) should be 'Not Found' but returned {phrase(404)!r}."
    assert phrase(503) == "Service Unavailable", f"status_phrase(503) should be 'Service Unavailable' but returned {phrase(503)!r}."
    assert phrase(799) == "Unknown", f"A code that does not exist should give 'Unknown' but gave {phrase(799)!r}. HTTPStatus raises ValueError for it."


def test_parse_headers():
    raw = "Content-Type: application/json\r\nContent-Length:  42 \r\nX-Note: has: colons"
    result = _fn("parse_headers")(raw)
    want = {"content-type": "application/json", "content-length": "42", "x-note": "has: colons"}
    assert result == want, f"Expected {want} but got {result}. Names are lower-cased, values stripped, and only the FIRST colon separates them."
