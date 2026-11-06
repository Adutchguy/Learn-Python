goal = int(input("Savings goal in dollars: "))
deposit = int(input("Dollars saved each week: "))

saved = 0
weeks = 0
while saved < goal:
    saved += deposit
    weeks += 1

print(f"Weeks needed: {weeks}")
