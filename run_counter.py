from collections import Counter, defaultdict

COVERAGE_RANGE = 16
INPUT_FILE = "input.txt"
ENCODING = "latin-1"
ALPHABET = "abcdefghiklmnoprstuvwy"

def load_filtered(path, encoding, alphabet):
    with open(path, "r", encoding=encoding) as f:
        text = f.read().lower()
    return [c for c in text if c in alphabet]

def build_unigram_followers(filtered):
    followers = defaultdict(Counter)
    for a, b in zip(filtered, filtered[1:]):
        followers[a][b] += 1
    return followers

def build_bigram_followers(filtered):
    followers = defaultdict(Counter)
    for a, b, c, d in zip(filtered, filtered[1:], filtered[2:], filtered[3:]):
        followers[(a, b)][(c, d)] += 1
    return followers

def coverage_at_n(followers, total, n):
    return sum(
        sum(v for _, v in followers[ctx].most_common(n))
        for ctx in followers
    ) / total if total else 0

def print_comparison(unigram_followers, bigram_followers, coverage_range):
    u_total = sum(sum(c.values()) for c in unigram_followers.values())
    b_total = sum(sum(c.values()) for c in bigram_followers.values())
    print(f"{'slots':>6}  {'1-to-1 cov':>10}  {'letters/slot':>12}  {'2-to-2 cov':>10}  {'letters/slot':>12}")
    for n in range(1, coverage_range + 1):
        u_cov = coverage_at_n(unigram_followers, u_total, n)
        b_cov = coverage_at_n(bigram_followers, b_total, n)
        u_lps = u_cov / n
        b_lps = (b_cov * 2) / n
        print(f"{n:>6}  {u_cov:>10.1%}  {u_lps:>12.4f}  {b_cov*2:>10.1%}  {b_lps:>12.4f}")

filtered = load_filtered(INPUT_FILE, ENCODING, ALPHABET)
unigram_followers = build_unigram_followers(filtered)
bigram_followers = build_bigram_followers(filtered)
print_comparison(unigram_followers, bigram_followers, COVERAGE_RANGE)
