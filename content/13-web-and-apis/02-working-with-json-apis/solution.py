import json


def extract_names(response_text):
    data = json.loads(response_text)
    return [item["name"] for item in data["results"]]


def safe_get(data, *keys, default=None):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def all_pages(fetch_page, max_pages=100):
    items = []
    page = 1
    fetched = 0
    while page is not None:
        if fetched >= max_pages:
            raise RuntimeError(f"More than {max_pages} pages; giving up.")
        response = fetch_page(page)
        fetched += 1
        items.extend(response["items"])
        page = response["next_page"]
    return items


def describe_error(status, body):
    if 200 <= status < 300:
        return "OK"
    if 400 <= status < 500:
        try:
            message = json.loads(body)["message"]
        except (ValueError, KeyError, TypeError):
            message = body
        return f"Request problem ({status}): {message}"
    return f"Server problem ({status}): try again later"
