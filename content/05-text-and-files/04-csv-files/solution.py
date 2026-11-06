import csv


def load_students(path):
    students = []
    with open(path, newline="") as file:
        for row in csv.DictReader(file):
            students.append((row["name"], int(row["score"])))
    return students


def class_average(path):
    scores = [score for _, score in load_students(path)]
    return sum(scores) / len(scores)


def save_passed(source, destination, minimum):
    with open(destination, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "score"])
        writer.writeheader()
        for name, score in load_students(source):
            if score >= minimum:
                writer.writerow({"name": name, "score": score})
