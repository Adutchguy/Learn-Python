numbers = []
for text in input("Whole numbers separated by spaces: ").split():
    numbers.append(int(text))

print(f"First three: {numbers[:3]}")
print(f"Last two: {numbers[-2:]}")
print(f"Every other: {numbers[::2]}")
print(f"Reversed: {numbers[::-1]}")
