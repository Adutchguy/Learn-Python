names = input("Names separated by spaces: ").split()

print("Sorted: " + ", ".join(sorted(names, key=str.lower)))
print("By length: " + ", ".join(sorted(names, key=len)))
print("Reverse: " + ", ".join(sorted(names, key=str.lower, reverse=True)))
