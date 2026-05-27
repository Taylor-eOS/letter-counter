from collections import Counter, defaultdict

alphabet = "abcdefghijklmnopqrstuvwxyz"
followers = defaultdict(Counter)
MOST_COMMON = 8

with open("input.txt", "r", encoding="latin-1") as f:
    text = f.read().lower()
filtered = [c for c in text if c in alphabet]
for a, b in zip(filtered, filtered[1:]):
    followers[a][b] += 1
rows = []
for letter in alphabet:
    common = [c for c, _ in followers[letter].most_common(MOST_COMMON)]
    rows.append((letter, common))
for row_letter, common in rows:
    line = [f"{row_letter:>2} |"]
    for c in alphabet:
        line.append(f"{c:>2}" if c in common else "  ")
    print(" ".join(line))

