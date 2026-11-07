import json
import urllib.error
import urllib.request


def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url, data):
    payload = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def get_status(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def get_with_header(url, name, value):
    request = urllib.request.Request(url, headers={name: value})
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.read().decode("utf-8")
