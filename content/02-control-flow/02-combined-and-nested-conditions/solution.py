age = int(input("Age: "))
day = input("Day (mon, tue, wed, thu, fri, sat or sun): ")

if age < 5:
    price = 0
elif age <= 12:
    price = 8
elif age <= 64:
    price = 15
else:
    price = 10

if day in ("sat", "sun") and price > 0:
    price = price + 2

print(f"Ticket: ${price}")
