def to_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def get_age(person):
    try:
        return int(person["age"])
    except KeyError:
        return "unknown"
    except (ValueError, TypeError):
        return "invalid"
