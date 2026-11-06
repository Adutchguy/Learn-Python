numbers = []
for text in input("Whole numbers separated by spaces: ").split():
    numbers.append(int(text))

evens = 0
for number in numbers:
    if number % 2 == 0:
        evens += 1

print(f"Total: {sum(numbers)}")
print(f"Largest: {max(numbers)}")
print(f"Evens: {evens}")
