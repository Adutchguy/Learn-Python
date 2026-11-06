def save_lines(path, lines):
    with open(path, "w") as file:
        for line in lines:
            file.write(line + "\n")


def load_lines(path):
    lines = []
    with open(path) as file:
        for line in file:
            lines.append(line.rstrip("\n"))
    return lines


def append_line(path, line):
    with open(path, "a") as file:
        file.write(line + "\n")
