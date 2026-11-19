#!/usr/bin/env python3
"""results/drafts/epistasis-707.py DB [--min N] - gene interactions in a run's alive designs (Iteration 707; the ideation
survey's "stranger": the search's own 80,000 records as an idea source). For each pair of genes whose expressed value is
off/on (0 / not 0) on enough alive designs, the four cells' mean log speed (64-bit) and mean log size (binary + image +
the five programs' code); the interaction (on,on) - (on,off) - (off,on) + (off,off) - zero when the two act
independently. Confounded: the cells' other genes differ, the search sampled them unevenly, in-run speeds are noisy - so
a hypothesis list, not a measure; a pair to test is then built both ways (newgenes.py's pairs, by hand). Each cell needs
--min designs (default 300). Reads only; python3 -I -B."""
import collections, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
db = sys.argv[1]; mn = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 300
sys.argv = ['x']; sys.path.insert(0, os.path.join(HERE, '..', '..', 'lab', 'evolve'))
import evolve as E
R = []
for l in open(db, errors='replace'):
    if '"status": "ok"' not in l: continue
    r = json.loads(l)
    if not (r.get('speed') and r.get('total')): continue
    x = E.express(E.canon(r['genome']))
    R.append(({k: (1 if v not in (0, None, [], False) else 0) for k, v in x.items() if not isinstance(v, (list, dict)) or True},
              math.log(r['speed']), math.log(r['total'])))
genes = sorted({k for x, _, _ in R for k in x})
share = {g: sum(1 for x, _, _ in R if x.get(g) == 1) / len(R) for g in genes}
G = [g for g in genes if 0.05 < share[g] < 0.95]
print('%d alive designs; %d genes on in 5-95 %% of them: %s' % (len(R), len(G), ' '.join(G)))
out = []
for i, a in enumerate(G):
    for b in G[i + 1:]:
        c = collections.defaultdict(list)
        for x, s, t in R:
            if a in x and b in x: c[(x[a], x[b])].append((s, t))
        if any(len(c[k]) < mn for k in ((0, 0), (0, 1), (1, 0), (1, 1))): continue
        m = {k: (sum(v[0] for v in c[k]) / len(c[k]), sum(v[1] for v in c[k]) / len(c[k])) for k in c}
        ins = m[(1, 1)][0] - m[(1, 0)][0] - m[(0, 1)][0] + m[(0, 0)][0]
        int_ = m[(1, 1)][1] - m[(1, 0)][1] - m[(0, 1)][1] + m[(0, 0)][1]
        out.append((a, b, ins, int_, min(len(c[k]) for k in c)))
print('%d pairs with every cell at %d or more' % (len(out), mn))

# Quartets (the clean form, as newgenes.py's pairs for one gene): designs the same in every expressed gene but a and b,
# in all four on/off cells - the interaction within each quartet, then the median over quartets. Size is exact there.
import statistics
X = []
for l in open(db, errors='replace'):
    if '"status": "ok"' not in l: continue
    r = json.loads(l)
    if not (r.get('speed') and r.get('total')): continue
    X.append((E.express(E.canon(r['genome'])), math.log(r['speed']), r['total'], r.get('speed32')))
top = sorted(G, key=lambda g: -min(share[g], 1 - share[g]))[:28]
q = []
for i, a in enumerate(top):
    for b in top[i + 1:]:
        cells = collections.defaultdict(dict)
        for x, s_, t, s32 in X:
            if a not in x or b not in x: continue
            k = json.dumps({g: v for g, v in x.items() if g not in (a, b)}, sort_keys=True, default=str)
            cells[k][(int(x[a] not in (0, None, [], False)), int(x[b] not in (0, None, [], False)))] = (s_, t)
        full = [c for c in cells.values() if len(c) == 4]
        if len(full) < 5: continue
        isp = [c[(1, 1)][0] - c[(1, 0)][0] - c[(0, 1)][0] + c[(0, 0)][0] for c in full]
        isz = [c[(1, 1)][1] - c[(1, 0)][1] - c[(0, 1)][1] + c[(0, 0)][1] for c in full]
        q.append((a, b, len(full), statistics.median(isp), statistics.median(isz), min(isz), max(isz)))
print('\nquartets - the same design but for a and b, all four cells - %d pairs with 5 or more:' % len(q))
print('| gene a | gene b | quartets | speed interaction, median (%%) | size interaction, median (bytes) | its range |\n|---|---|---:|---:|---:|---|')
for a, b, n, s_, t, lo, hi in sorted(q, key=lambda o: -abs(o[4]) - abs(o[3]) * 1000)[:16]:
    print('| %s | %s | %d | %+.1f | %+d | %+d to %+d |' % (a, b, n, 100 * s_, t, lo, hi))
for name, j in (('speed', 2), ('size', 3)):
    print('\nthe strongest interactions on %s (x100 of the log: about %% - below 0 the pair together better than its parts):' % name)
    print('| gene a | gene b | interaction, speed | interaction, size | smallest cell |\n|---|---|---:|---:|---:|')
    for a, b, s, t, n in sorted(out, key=lambda o: -abs(o[j]))[:10]:
        print('| %s | %s | %+.1f | %+.1f | %d |' % (a, b, 100 * s, 100 * t, n))
