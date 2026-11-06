def parse_expense(line):
    parts = line.split()
    if len(parts) != 2:
        raise ValueError("expected CATEGORY AMOUNT, for example: food 12.50")
    try:
        amount = float(parts[1])
    except ValueError:
        raise ValueError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be positive")
    return parts[0].lower(), amount


def load_expenses(path):
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return []
    expenses = []
    for line in lines:
        category, _, amount = line.partition(",")
        try:
            expenses.append((category, float(amount)))
        except ValueError:
            continue
    return expenses


def save_expense(path, category, amount):
    with open(path, "a") as f:
        f.write(f"{category},{amount}\n")


def totals_by_category(expenses):
    totals = {}
    for category, amount in expenses:
        totals[category] = totals.get(category, 0) + amount
    return {category: round(total, 2) for category, total in totals.items()}


def format_report(totals):
    if not totals:
        return "No expenses yet."
    lines = []
    for category, amount in sorted(totals.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"{category:<10}{amount:>8.2f}")
    lines.append(f"{'total':<10}{sum(totals.values()):>8.2f}")
    return "\n".join(lines)


def main(path="expenses.csv"):
    print("Expense tracker. Commands: add CATEGORY AMOUNT, report, quit")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if line == "quit":
            break
        if line == "report":
            print(format_report(totals_by_category(load_expenses(path))))
        elif line.startswith("add "):
            try:
                category, amount = parse_expense(line[4:])
            except ValueError as err:
                print(f"Error: {err}")
            else:
                save_expense(path, category, amount)
                print(f"Added {amount:.2f} to {category}")
        else:
            print("Unknown command. Try: add food 12.50")


if __name__ == "__main__":
    main()
