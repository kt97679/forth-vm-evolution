#!/usr/bin/env python3
"""heldout.py RESULTS.md - does the front's speed hold on the held-out workload?
(Iteration 305)

The report's front table carries each design's selection speed and its speed on the
held-out workload (sieve; parse too where a report has it) - columns found by their
header's name, never by position (the first try at this read "re-measured", the
selection speed measured again, and called it held out). Prints the Spearman rank
correlation between the two, where the selection's fastest designs rank on the
held-out one, the spread of held-out over selection speed, and the designs worst
on the held-out workload relative to their selection speed - the ones the selection
flatters. Both speeds are against s6 on the same machine and commit.
Iteration 390 (the review, results/review-methodology-386.md, 2d): a whole front spanning JIT and not ranks
well on anything, so the Spearman over its fastest third and tenth too - where selection chooses - and the
regret: how much slower held out the selection's fastest is than the held-out fastest.
"""
import sys
if len(sys.argv) != 2: sys.exit(__doc__)
L = open(sys.argv[1]).read().split('\n')
h = next((i for i, l in enumerate(L) if l.startswith('| design | speed |')), None)
if h is None: sys.exit('heldout: no front table (| design | speed | ...) in %s' % sys.argv[1])
cols = [c.strip() for c in L[h].strip().strip('|').split('|')]
si = cols.index('speed'); held = [(i, c) for i, c in enumerate(cols) if 'held out' in c]
if not held: sys.exit('heldout: no held-out column in %s' % sys.argv[1])
rows = []
for l in L[h + 2:]:
    if not l.startswith('| '): break
    c = [x.strip() for x in l.strip().strip('|').split('|')]
    rows.append(c)
def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o): r[i] = k
    return r
for hi, name in held:
    d = [(c[0], float(c[si]), float(c[hi])) for c in rows if c[hi] not in ('', '-')]
    n = len(d); a, b = ranks([x[1] for x in d]), ranks([x[2] for x in d])
    rho = 1 - 6.0 * sum((x - y) ** 2 for x, y in zip(a, b)) / (n * (n * n - 1))
    top = sorted(range(n), key=lambda i: d[i][1])[:10]
    q = sorted((d[i][2] / d[i][1], d[i][0]) for i in range(n))
    print('%s: %d designs; Spearman with the selection speed %.3f' % (name, n, rho))
    def rho_of(idx):
        m = len(idx); aa, bb = ranks([d[i][1] for i in idx]), ranks([d[i][2] for i in idx])
        return 1 - 6.0 * sum((x - y) ** 2 for x, y in zip(aa, bb)) / (m * (m * m - 1)) if m > 2 else float('nan')
    order = sorted(range(n), key=lambda i: d[i][1]); k3, k10 = n // 3, max(3, n // 10)
    print('  at the top, where selection chooses: the fastest third (%d) %.3f, the fastest tenth (%d) %.3f' % (k3, rho_of(order[:k3]), k10, rho_of(order[:k10])))
    pick, best = order[0], min(range(n), key=lambda i: d[i][2])
    print('  regret: the selection\'s fastest, %s, %.3f held out; the held-out fastest, %s, %.3f - the pick %+.1f%%'
          % (d[pick][0], d[pick][2], d[best][0], d[best][2], 100 * (d[pick][2] / d[best][2] - 1)))
    print('  the 10 fastest by selection, their rank on it: %s' % ' '.join(str(b[i] + 1) for i in top))
    print('  held-out / selection speed: min %.2f, median %.2f, max %.2f' % (q[0][0], q[n // 2][0], q[-1][0]))
    print('  flattered most by the selection: %s' % ', '.join('%s %.2f' % (i, r) for r, i in q[-5:][::-1]))
