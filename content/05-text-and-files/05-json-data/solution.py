import json
from pathlib import Path


def to_json(data):
    return json.dumps(data, indent=2, sort_keys=True)


def save_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def load_json(path, default):
    if not Path(path).exists():
        return default
    with open(path) as file:
        return json.load(file)
