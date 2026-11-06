item = input("Item: ")
price = float(input("Price: "))
quantity = int(input("Quantity: "))

print(f"{quantity} x {item} at ${price:.2f} = ${price * quantity:.2f}")
