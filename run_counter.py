from collections import Counter, defaultdict

MOST_COMMON = 8
COVERAGE_RANGE = 16
INPUT_FILE = "input.txt"
ENCODING = "latin-1"
#ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = "abcdefghiklmnoprstuvwy"

def load_filtered(path, encoding, alphabet):
    with open(path, "r", encoding=encoding) as f:
        text = f.read().lower()
    return [c for c in text if c in alphabet]

def build_followers(filtered, alphabet):
    followers = defaultdict(Counter)
    for a, b in zip(filtered, filtered[1:]):
        followers[a][b] += 1
    return followers

def compute_coverage(followers, alphabet, total_bigrams, n):
    covered = sum(
        sum(v for _, v in followers[letter].most_common(n))
        for letter in alphabet
    )
    return covered / total_bigrams if total_bigrams else 0

def print_table(followers, alphabet, most_common):
    for letter in alphabet:
        common = {c for c, _ in followers[letter].most_common(most_common)}
        line = [f"{letter:>2} |"]
        for c in alphabet:
            line.append(f"{c:>2}" if c in common else "  ")
        print(" ".join(line))

def print_coverage(followers, alphabet, most_common, coverage_range):
    total_bigrams = sum(sum(c.values()) for c in followers.values())
    current = compute_coverage(followers, alphabet, total_bigrams, most_common)
    print(f"{'top-N':>6}  {'coverage':>8}")
    for n in range(1, coverage_range + 1):
        print(f"{n:>6}  {compute_coverage(followers, alphabet, total_bigrams, n):>7.1%}")

filtered = load_filtered(INPUT_FILE, ENCODING, ALPHABET)
followers = build_followers(filtered, ALPHABET)
print_table(followers, ALPHABET, MOST_COMMON)
print_coverage(followers, ALPHABET, MOST_COMMON, COVERAGE_RANGE)
