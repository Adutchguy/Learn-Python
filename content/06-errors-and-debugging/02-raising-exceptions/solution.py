def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be a whole number")
    if not 0 <= age <= 150:
        raise ValueError("age must be between 0 and 150")
    return age


class OutOfStock(Exception):
    pass


def take(stock, item, quantity=1):
    have = stock.get(item, 0)
    if have < quantity:
        raise OutOfStock(f"only {have} {item} left, wanted {quantity}")
    stock[item] = have - quantity
    return stock[item]


def parse_percent(text):
    if not text.endswith("%"):
        raise ValueError(f"not a percentage: {text!r}")
    try:
        value = int(text[:-1])
    except ValueError:
        raise ValueError(f"not a percentage: {text!r}")
    if not 0 <= value <= 100:
        raise ValueError(f"percentage out of range: {value}")
    return value
