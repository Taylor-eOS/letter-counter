from collections import defaultdict

SLOTS = 8
OMIT = frozenset('qx')

def build_table(transitions):
    table = {}
    for ctx, followers in transitions.items():
        total = sum(followers.values())
        ranked = sorted(followers.items(), key=lambda x: -x[1])
        top = ranked[:SLOTS]
        covered = sum(c for _, c in top)
        table[ctx] = {'top': top, 'covered': covered, 'total': total, 'escaped': total - covered}
    return table

def main():
    with open('input.txt', encoding='utf-8') as f:
        raw = f.read()
    normalized = []
    for ch in raw:
        if ch in (' ', '\n'):
            normalized.append(' ')
        elif ch.isalpha():
            low = ch.lower()
            if low not in OMIT:
                normalized.append(low)
    transitions = defaultdict(lambda: defaultdict(int))
    stream = ['^', '^'] + normalized
    for i in range(len(stream) - 2):
        ctx = stream[i] + stream[i + 1]
        nxt = stream[i + 2]
        transitions[ctx][nxt] += 1
    total_chars = len(normalized)
    total_spaces = sum(1 for c in normalized if c == ' ')
    table = build_table(transitions)
    total_covered = sum(v['covered'] for v in table.values())
    total_escaped = sum(v['escaped'] for v in table.values())
    total_transitions = total_covered + total_escaped
    print(f"Input characters (including spaces): {total_chars}")
    print(f"Spaces:                             {total_spaces}")
    print(f"Total transitions analyzed:         {total_transitions}")
    print(f"Slots per context:                  {SLOTS}")
    print(f"Overall covered:  {total_covered} ({100 * total_covered / total_transitions:.1f}%)")
    print(f"Overall escaped:  {total_escaped} ({100 * total_escaped / total_transitions:.1f}%)")
    worst = sorted((item for item in table.items() if item[1]['escaped'] > 0), key=lambda x: x[1]['escaped'] / x[1]['total'], reverse=True)
    print("Per-context breakdown (worst escape rate first):")
    print(f"  {'CTX':>6}  {'TOTAL':>7}  {'COVERED':>8}  {'ESCAPED':>8}  {'ESC%':>6}  TOP FOLLOWERS")
    print(f"  {'------':>6}  {'-------':>7}  {'--------':>8}  {'--------':>8}  {'------':>6}")
    for ctx, stats in worst:
        esc_pct = 100 * stats['escaped'] / stats['total']
        followers = ' '.join(f"{repr(ch)[1:-1]}:{c}" for ch, c in stats['top'][:6])
        print(f"  {ctx!r:>6}  {stats['total']:>7}  {stats['covered']:>8}  {stats['escaped']:>8}  {esc_pct:>5.1f}%  {followers}")
    print("Characters never appearing in any top follower list:")
    all_followers = set()
    for v in table.values():
        for ch, _ in v['top']:
            all_followers.add(ch)
    alphabet_seen = set(normalized)
    never_top = alphabet_seen - all_followers
    print(f"  {sorted(never_top)}")
    print("Global character frequencies:")
    freq = defaultdict(int)
    for ch in normalized:
        freq[ch] += 1
    for ch, count in sorted(freq.items(), key=lambda x: -x[1]):
        bar = '#' * (40 * count // max(freq.values()))
        label = '<sp>' if ch == ' ' else ch
        print(f"  {label}: {count:>7}  {bar}")

main()
