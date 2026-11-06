import math
import statistics


def circle_area(radius):
    return round(math.pi * radius ** 2, 2)


def pages_needed(items, per_page):
    return math.ceil(items / per_page)


def summarize(numbers):
    return {"mean": round(statistics.mean(numbers), 2), "median": statistics.median(numbers)}


def main():
    print("Area:", circle_area(2))


if __name__ == "__main__":
    main()
