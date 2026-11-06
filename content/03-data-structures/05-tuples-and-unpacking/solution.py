names = input("Names separated by spaces: ").split()
scores = [int(text) for text in input("Scores separated by spaces: ").split()]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

best_score, best_name = max(zip(scores, names))
print(f"Best: {best_name} ({best_score})")
