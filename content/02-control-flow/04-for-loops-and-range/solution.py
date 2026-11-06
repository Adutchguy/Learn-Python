n = int(input("How many square numbers? "))

total = 0
for number in range(1, n + 1):
    square = number * number
    print(square)
    total += square

print(f"Total: {total}")
