def greet(name):
    print(f"Hello, {name}!")


def banner(text):
    border = "=" * (len(text) + 4)
    print(border)
    print(f"| {text} |")
    print(border)
