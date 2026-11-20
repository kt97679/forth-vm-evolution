"""results/drafts/heldout-711.py RESULTS - Frostbite's overfitting check on the screen's pool - the search set's speed against the held-out
workloads' (sieve, parse), per design, at 8-byte cells, ratios to s6 (1.0 = s6): how well the search set ranks the held-out pair, overall and
within the JIT designs and the interpreted, and where the search set's top 1, 5 and 20 % land on the held-out pair. Reads
only; python3 -I. results/drafts/frostbite-711.md."""
import json, math, statistics, sys
SEL = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']; HELD = ['sieve', 'parse']
R = [json.loads(l) for l in open(sys.argv[1]) if l.startswith('{"')]
R = [r for r in R if r.get('t') and all(w in r['t'] for w in SEL + HELD)]
gm = lambda xs: math.exp(sum(math.log(x) for x in xs) / len(xs))
rows = [(r['id'], gm([r['t'][w] for w in SEL]), gm([r['t'][w] for w in HELD]), r['t']['sieve'], r['t']['parse'],
         bool(r['genome'].get('jit') and r['genome'].get('tag2'))) for r in R]
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o): r[i] = k
    return r
def spearman(a, b):
    ra, rb = rank(a), rank(b); n = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))
print('%d designs' % len(rows))
for name, sub in (('all', rows), ('JIT', [x for x in rows if x[5]]), ('not JIT', [x for x in rows if not x[5]])):
    s, h = [x[1] for x in sub], [x[2] for x in sub]
    print('%-8s n=%4d  Spearman(search, held-out) %.3f  (search, sieve) %.3f  (search, parse) %.3f' % (
        name, len(sub), spearman(s, h), spearman(s, [x[3] for x in sub]), spearman(s, [x[4] for x in sub])))
    sub2 = sorted(sub, key=lambda x: x[1])
    for frac in (0.01, 0.05, 0.2):
        top = sub2[:max(1, int(len(sub2) * frac))]
        # the top by the search set: their median search ratio and held-out ratio, and where they rank on held-out
        hr = rank(h); idx = {x[0]: i for i, x in enumerate(sub)}
        pct = statistics.median(hr[idx[x[0]]] / len(sub) for x in top)
        print('   top %4.0f%% by search: search %.3f  held-out %.3f  (all: %.3f, %.3f) - their median held-out rank %.0f%%' % (
            100 * frac, statistics.median(x[1] for x in top), statistics.median(x[2] for x in top),
            statistics.median(s), statistics.median(h), 100 * pct))
