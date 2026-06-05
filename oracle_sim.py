from collections import defaultdict

OMIT = frozenset('qx')
SENTINEL = '^'

def build_alphabet(text):
    seen = set(text)
    seen.discard('')
    return sorted(seen)

def normalize(raw, omit=OMIT):
    out = []
    for ch in raw:
        if ch in (' ', '\n'):
            out.append(' ')
        elif ch.isalpha():
            low = ch.lower()
            if low not in omit:
                out.append(low)
    return out

def build_ngram_counts(stream, max_order):
    counts = {}
    for order in range(1, max_order + 1):
        counts[order] = defaultdict(lambda: defaultdict(int))
    for i in range(len(stream) - 1):
        nxt = stream[i + 1]
        for order in range(1, max_order + 1):
            start = i - order + 1
            if start < 0:
                continue
            ctx = tuple(stream[start:i + 1])
            counts[order][ctx][nxt] += 1
    return counts

def build_global_freq(stream, alphabet):
    freq = defaultdict(int)
    for ch in stream:
        if ch in alphabet:
            freq[ch] += 1
    total = sum(freq.values()) or 1
    return sorted(alphabet, key=lambda c: -freq[c] / total)

def make_oracle(counts, global_order, max_order):
    def reorder(context):
        for order in range(min(max_order, len(context)), 0, -1):
            ctx_key = tuple(context[-order:])
            if ctx_key in counts[order]:
                followers = counts[order][ctx_key]
                ranked = sorted(followers.keys(), key=lambda c: -followers[c])
                ranked_set = set(ranked)
                tail = [c for c in global_order if c not in ranked_set]
                return ranked + tail
        return global_order
    return reorder

def simulate(stream, alphabet, reorder_fn, max_order):
    total_cost = 0
    total_chars = 0
    padding = [SENTINEL] * max_order
    padded = padding + stream
    for i in range(max_order, len(padded)):
        ch = padded[i]
        if ch not in alphabet:
            continue
        context = padded[i - max_order:i]
        ordering = reorder_fn(context)
        try:
            pos = ordering.index(ch)
        except ValueError:
            pos = len(ordering)
        total_cost += pos
        total_chars += 1
    avg = total_cost / total_chars if total_chars else 0
    return total_cost, total_chars, avg

def static_reorder(global_order):
    def reorder(context):
        return global_order
    return reorder

def main():
    with open('input.txt', encoding='utf-8') as f:
        raw = f.read()
    stream = normalize(raw)
    alphabet = set(stream)
    alphabet.discard(SENTINEL)
    alphabet = sorted(alphabet)
    global_order = build_global_freq(stream, alphabet)
    print(f"Alphabet size: {len(alphabet)}")
    print(f"Stream length: {len(stream)}")
    print(f"Global frequency order: {''.join(global_order)}")
    print()
    padded_stream = [SENTINEL] * 4 + stream
    max_order = 4
    counts = build_ngram_counts(padded_stream, max_order)
    static_fn = static_reorder(global_order)
    _, _, static_avg = simulate(stream, set(alphabet), static_fn, max_order)
    print(f"Static alphabet baseline: {static_avg:.4f} avg rotations/char")
    for order in range(1, max_order + 1):
        oracle_fn = make_oracle(counts, global_order, order)
        _, _, oracle_avg = simulate(stream, set(alphabet), oracle_fn, order)
        reduction = 100 * (1 - oracle_avg / static_avg)
        print(f"Oracle (max order={order}):         {oracle_avg:.4f} avg rotations/char  ({reduction:.1f}% reduction)")

main()
