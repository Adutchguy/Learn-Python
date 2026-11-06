line = input("Shopping list (words separated by spaces): ")
items = line.split()

items.append("apples")
if "eggs" in items:
    items.remove("eggs")

print(f"First: {items[0]}")
print(f"Last: {items[-1]}")
print(f"Items: {len(items)}")
