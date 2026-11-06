numbers = [int(text) for text in input("Whole numbers separated by spaces: ").split()]
words = input("Words separated by spaces: ").split()

even_squares = [n * n for n in numbers if n % 2 == 0]
lengths = {word: len(word) for word in words}

print(f"Even squares: {even_squares}")
print(f"Lengths: {lengths}")
