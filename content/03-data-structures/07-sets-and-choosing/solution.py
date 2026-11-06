first = set(input("Guests at the first party: ").split())
second = set(input("Guests at the second party: ").split())


def show(group):
    return ", ".join(sorted(group)) or "nobody"


print("Both: " + show(first & second))
print("Only first: " + show(first - second))
print("Only second: " + show(second - first))
print("Everyone: " + show(first | second))
