MAX_ITEMS = 10


def calculate_total(prices, tax_rate=0.1, discounts=None):
    """Return the total price after discounts and tax, rounded to cents."""
    if discounts is None:
        discounts = []
    subtotal = sum(prices) - sum(discounts)
    return round(subtotal * (1 + tax_rate), 2)


def is_valid_email(text):
    """Return True if the text looks like name@domain.tld."""
    name, _, domain = text.partition("@")
    return text.count("@") == 1 and "." in domain and name != ""


def read_number(text):
    """Return the text as an int, or None if it is not a whole number."""
    try:
        return int(text)
    except ValueError:
        return None
