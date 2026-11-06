TAX_RATE = 0.2


def add_tax(price):
    return round(price * (1 + TAX_RATE), 2)


def with_item(cart, item):
    return cart + [item]
