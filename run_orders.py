from collections import Counter, defaultdict
from math import log2

INPUT_FILE = "input.txt"
ENCODING = "latin-1"

ALPHABET = "abcdefghiklmnoprstuvwy"
ESCAPE = "~"

CONFLATIONS = {
    "0": "o",
    "1": "l",
    "j": "i",
}

MAX_ORDER = 8
PACKET_BITS = 40

def normalize_text(text):
    out = []
    for c in text.lower():
        if c in CONFLATIONS:
            out.extend(CONFLATIONS[c])
        elif c in ALPHABET:
            out.append(c)
        elif c.isalpha() or c.isdigit():
            out.append(ESCAPE)
            out.append(c)
    return "".join(out)

def load_text(path, encoding):
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    h = 0.0
    for count in counter.values():
        p = count / total
        h -= p * log2(p)
    return h

def conditional_entropy(text, order):
    if len(text) <= order:
        return 0.0
    followers = defaultdict(Counter)
    for i in range(len(text) - order):
        ctx = text[i:i + order]
        nxt = text[i + order]
        followers[ctx][nxt] += 1
    total = sum(sum(v.values()) for v in followers.values())
    h = 0.0
    for ctx, counts in followers.items():
        ctx_total = sum(counts.values())
        weight = ctx_total / total
        h += weight * entropy(counts)
    return h

def bits_per_symbol_fixed(alphabet_size):
    return log2(alphabet_size)

def chars_per_packet(bits_per_symbol, packet_bits):
    if bits_per_symbol == 0:
        return 0.0
    return packet_bits / bits_per_symbol

def print_global_stats(text):
    counts = Counter(text)
    raw_entropy = entropy(counts)
    fixed_bits = bits_per_symbol_fixed(len(ALPHABET))
    print()
    print("GLOBAL")
    print(f"symbols:                {len(text)}")
    print(f"alphabet size:          {len(ALPHABET)}")
    print(f"fixed bits/symbol:      {fixed_bits:.3f}")
    print(f"measured entropy:       {raw_entropy:.3f}")
    print(f"fixed chars/40 bits:    {chars_per_packet(fixed_bits, PACKET_BITS):.2f}")
    print(f"entropy chars/40 bits:  {chars_per_packet(raw_entropy, PACKET_BITS):.2f}")

def print_context_stats(text):
    print()
    print(f"{'order':>5} {'bits/sym':>10} {'chars/40b':>12} {'compression':>12}")
    for order in range(MAX_ORDER + 1):
        if order == 0:
            h = entropy(Counter(text))
        else:
            h = conditional_entropy(text, order)
        chars40 = chars_per_packet(h, PACKET_BITS)
        ratio = 8 / h if h else 0.0
        print(f"{order:>5} {h:>10.3f} {chars40:>12.2f} {ratio:>12.2f}x")

raw = load_text(INPUT_FILE, ENCODING)
text = normalize_text(raw)

print_global_stats(text)
print_context_stats(text)
