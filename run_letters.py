from collections import defaultdict

SLOTS = 8
OMIT = frozenset('qx')

def build_table(bigrams):
    table = {}
    for ctx, followers in bigrams.items():
        total = sum(followers.values())
        ranked = sorted(followers.items(), key=lambda x: -x[1])
        top = ranked[:SLOTS]
        covered = sum(c for _, c in top)
        table[ctx] = {
            'top': top,
            'covered': covered,
            'total': total,
            'escaped': total - covered,
        }
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
    bigrams = defaultdict(lambda: defaultdict(int))
    word_start = defaultdict(int)
    for i in range(len(normalized) - 1):
        cur = normalized[i]
        nxt = normalized[i + 1]
        if nxt == ' ':
            continue
        if cur == ' ':
            word_start[nxt] += 1
        else:
            bigrams[cur][nxt] += 1
    total_chars = sum(1 for c in normalized if c != ' ')
    total_spaces = sum(1 for c in normalized if c == ' ')
    table = build_table(bigrams)
    ws_total = sum(word_start.values())
    ws_ranked = sorted(word_start.items(), key=lambda x: -x[1])
    ws_top = ws_ranked[:SLOTS]
    ws_covered = sum(c for _, c in ws_top)
    ws_escaped = ws_total - ws_covered
    total_covered = sum(v['covered'] for v in table.values()) + ws_covered
    total_escaped = sum(v['escaped'] for v in table.values()) + ws_escaped
    total_transitions = total_covered + total_escaped
    print(f"Input characters (letters only): {total_chars}")
    print(f"Space transitions (word starts):  {total_spaces}")
    print(f"Total transitions analyzed:       {total_transitions}")
    print(f"Slots per context:                {SLOTS}") 
    print(f"Overall covered:  {total_covered} ({100*total_covered/total_transitions:.1f}%)")
    print(f"Overall escaped:  {total_escaped} ({100*total_escaped/total_transitions:.1f}%)") 
    worst = sorted(table.items(), key=lambda x: x[1]['escaped'] / x[1]['total'] if x[1]['total'] > 0 else 0, reverse=True)
    print("Per-context breakdown (worst escape rate first):")
    print(f"  {'CTX':>4}  {'TOTAL':>7}  {'COVERED':>8}  {'ESCAPED':>8}  {'ESC%':>6}  TOP FOLLOWERS")
    print(f"  {'----':>4}  {'-------':>7}  {'--------':>8}  {'--------':>8}  {'------':>6}")
    ws_esc_pct = 100 * ws_escaped / ws_total if ws_total > 0 else 0
    ws_followers = ' '.join(f"{ch}:{c}" for ch, c in ws_top[:6])
    print(f"  {'SPC':>4}  {ws_total:>7}  {ws_covered:>8}  {ws_escaped:>8}  {ws_esc_pct:>5.1f}%  {ws_followers}")
    for ctx, stats in worst:
        esc_pct = 100 * stats['escaped'] / stats['total'] if stats['total'] > 0 else 0
        followers = ' '.join(f"{ch}:{c}" for ch, c in stats['top'][:6])
        print(f"  {ctx!r:>4}  {stats['total']:>7}  {stats['covered']:>8}  {stats['escaped']:>8}  {esc_pct:>5.1f}%  {followers}") 
    print("Characters never appearing as followers (always escaped or absent):")
    all_followers = set()
    for v in table.values():
        for ch, _ in v['top']:
            all_followers.add(ch)
    for ch, _ in ws_top:
        all_followers.add(ch)
    alphabet_seen = set(normalized) - {' '}
    never_top = alphabet_seen - all_followers
    print(f"  {sorted(never_top)}")
    print("Global letter frequencies (for reference):")
    freq = defaultdict(int)
    for ch in normalized:
        if ch != ' ':
            freq[ch] += 1
    for ch, count in sorted(freq.items(), key=lambda x: -x[1]):
        bar = '#' * (40 * count // max(freq.values()))
        print(f"  {ch}: {count:>7}  {bar}")

main()
