# results/wip-regmachine/README.md, "Coverage" - how much of what a register stage could take in each set of operand
# sources covers. python3 THIS [N] - N plain-CV8 designs of seed 58's front (default 8), spread by size; each built
# with the profiler and the converter's names (as price-418.py), its workloads' pairs and triples read, every
# taken-in pattern - moves and literals straight before the operation that consumes them - classed by what its
# operands need, the sets cumulative:
#   A  a literal operand (LIT8, or wider)              C  + the return stack (R@, R>)
#   B  + the top kept (a DUP before)                   D  + the loop index (I, J)
#   E  + the second item (OVER) and the order (SWAP)   rest - >R, ROT, DROP, two-cell moves, deeper runs
import collections, json, os, shutil, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8; sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
MOVE = {'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '-ROT', 'NIP', 'TUCK', '>R', 'R>', 'R@', '2DUP', '2DROP', '2SWAP', '2OVER', 'I', 'J', 'UNLOOP'}
CONTROL = {'EXIT', 'BRANCH', '?BRANCH', '0BRANCH', '(LOOP)', '(+LOOP)', '(DO)', '(?DO)', 'EXECUTE', 'DOVAR', 'DODOES', 'DOCON'}
F = [json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"')]
F = [r for r in F if not E.express(E.canon(r['genome'])).get('tag2')]
F.sort(key=lambda r: r.get('total') or 0); pick = F[::max(1, len(F) // N)][:N]
def need(pre):
    """The set a run of prefix names needs, or 'rest'."""
    s = 'A'
    for p in pre:
        if p.startswith('LIT'): continue
        if p == 'DUP' and pre.index(p) == 0: s = max(s, 'B')
        elif p in ('R@', 'R>'): s = max(s, 'C')
        elif p in ('I', 'J'): s = max(s, 'D')
        elif p in ('OVER', 'SWAP'): s = max(s, 'E')
        else: return 'rest'
    return s
WORKS = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann']
tot = collections.defaultdict(lambda: collections.Counter()); consumers = collections.Counter()
print('| design | total | ' + ' | '.join(WORKS) + ' |'); print('|---|---|' + '---|' * len(WORKS))
for r in pick:
    g = E.canon(r['genome']); d = os.path.join(E.EV, 'rmcov'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    E.PROFILING[0] = True; cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; os.environ.pop('CALLMAP', None)
    conv = {}
    for l in open(cm):
        f = l.split()
        if f and f[0] == 'O' and len(f) >= 5: conv.setdefault(int(f[3]), (f[2], f[4]))
    nm = lambda op: 'call' if op >= 128 else conv.get(op, ('?', 'op%d' % op))[1]
    def kind(op):
        if op >= 128: return 'C'
        k, n = conv.get(op, ('?', '?'))
        if k in ('LIT', 'LITX') or n.startswith('LIT'): return 'L'
        if k in ('LP', 'BR', 'CALL') or n in CONTROL or n.endswith('BRANCH'): return 'C'
        parts = [p for p in n.replace(';', ' ').replace('|', ' ').split() if p]
        if parts and all(p in MOVE for p in parts): return 'M'
        if n == '?': return '?'
        return 'C' if any(p in CONTROL for p in parts) else 'W'
    pw = E.private_work(d); cells = []
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        by, pr, tr = collections.Counter(), collections.Counter(), collections.Counter()
        for line in open(pf):
            f = line.split()
            if not f: continue
            if f[0] == 'T' and len(f) == 5 and f[1].isdigit(): tr[(int(f[1]), int(f[2]), int(f[3]))] += int(f[4]); continue
            if not f[0].isdigit(): continue
            a, b, k = int(f[0]), int(f[1]), int(f[2])
            if a == 0x7D or 128 <= b <= 255: continue
            by[b] += k; pr[(a, b)] += k
        D = sum(by.values()) or 1; c = collections.Counter()
        for (a, b), k in pr.items():
            if kind(a) in ('M', 'L') and kind(b) == 'W': c[need([nm(a)])] += k; consumers[nm(b)] += k
        for (a, b, x), k in tr.items():
            if kind(a) in ('M', 'L') and kind(b) in ('M', 'L') and kind(x) == 'W': c[need([nm(a), nm(b)])] += k
        cum, acc = [], 0
        for s in 'ABCDE': acc += c[s]; cum.append(100 * acc / D)
        tot[w].update({s: 100 * c[s] / D for s in c})
        cells.append('%.0f/%.0f/%.0f/%.0f/%.0f (%.0f)' % tuple(cum + [100 * (acc + c['rest']) / D]))
    print('| %s | %s | %s |' % (r['id'], r.get('total'), ' | '.join(cells)), flush=True)
print('\nCells: the share of all dispatches taken in, cumulative over the sets A/B/C/D/E (all of it, rest included).')
t = sum(consumers.values()) or 1
print('The operations that take them in, the largest: ' + '; '.join('`%s` %.0f%%' % (o, 100 * k / t) for o, k in consumers.most_common(14)))
