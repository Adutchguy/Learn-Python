# Fill in the five functions. Leave main() and the last two lines alone.

def parse_expense(line):
    """'food 12.50' -> ('food', 12.5). Raises ValueError with the messages in the lesson."""
    # TODO 1: split the line, check there are exactly two parts, convert the amount, check it is positive.
    ...


def load_expenses(path):
    """Return a list of (category, amount) tuples. A missing file gives []. Skip bad lines."""
    # TODO 2
    ...


def save_expense(path, category, amount):
    """Append 'category,amount' as a new line at the end of the file."""
    # TODO 3
    ...


def totals_by_category(expenses):
    """[('food', 10.0), ('food', 2.5)] -> {'food': 12.5}. Round each total to 2 decimals."""
    # TODO 4
    ...


def format_report(totals):
    """Build the report text described in the lesson."""
    # TODO 5
    ...


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
