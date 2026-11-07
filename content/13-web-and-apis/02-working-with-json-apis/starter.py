import json


# Write four functions:
#
# def extract_names(response_text): ...          names from {"results": [{"name": ...}, ...]}
# def safe_get(data, *keys, default=None): ...   follow keys into nested dicts; default if anything is missing
# def all_pages(fetch_page, max_pages=100): ...  collect "items" from every page; raise RuntimeError past max_pages
# def describe_error(status, body): ...          a short message for the user (see the lesson)
