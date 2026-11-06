total = 0
count = 0

while True:
    number = int(input("Number: "))
    if number == 0:
        break
    if number < 0:
        continue
    total += number
    count += 1

print(f"Sum: {total}")
print(f"Counted: {count}")
