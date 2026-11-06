sentence = input("Type a sentence: ")

counts = {}
for word in sentence.lower().split():
    counts[word] = counts.get(word, 0) + 1

for word in sorted(counts):
    print(f"{word}: {counts[word]}")
print(f"Unique words: {len(counts)}")
