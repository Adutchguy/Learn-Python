import json
import urllib.error
import urllib.request


# Write four functions:
#
# def get_json(url): ...                         GET; return the parsed JSON
# def post_json(url, data): ...                  POST data as JSON; return the parsed JSON reply
# def get_status(url): ...                       the status code, even for 404 / 500
# def get_with_header(url, name, value): ...     GET with an extra header; return the response text
