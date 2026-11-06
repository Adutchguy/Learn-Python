import re


def find_numbers(text):
    return [int(number) for number in re.findall(r"\d+", text)]


def find_hashtags(text):
    return re.findall(r"#(\w+)", text)


def parse_date(text):
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", text)
    if match is None:
        return None
    return tuple(int(part) for part in match.groups())
