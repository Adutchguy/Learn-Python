class Cart:
    def __init__(self):
        self.items = {}

    def add(self, name, price, qty=1):
        if name in self.items:
            self.items[name][1] += qty
        else:
            self.items[name] = [price, qty]

    def remove(self, name):
        del self.items[name]

    def total(self):
        return round(sum(price * qty for price, qty in self.items.values()), 2)

    def count(self):
        return sum(qty for _, qty in self.items.values())

    def most_expensive(self):
        if not self.items:
            return None
        return max(self.items, key=lambda name: self.items[name][0])
