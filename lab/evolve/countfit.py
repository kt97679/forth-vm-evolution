#!/usr/bin/env python3
"""lab/evolve/countfit.py FILE [FILE ...] [--folds K] [--self-test] - a model of a run's time from its counters (Iteration
711; results/drafts/frostbite-711.md). Architect Labs' Frostbite (architectlabs.com/blog/frostbite) searched its design
space with a fast model, Arcmodel, fitted to RTL: power and performance as a scalar function over a design's counters
(SRAM reads, operations, flits), the fit iterated until model and RTL agreed within 5 % - from a worst case near 250 %
to under 6 %, a median of 1.5 %. Here the counters are the PMU's (tools/cputime.c: instructions, cycles, branches
mispredicted, last-level misses) and the truth the CPU time; the question is the same - does a fit over counts that
do not depend on the moment (instructions, mispredictions, misses: one run's) predict the time the rounds measure,
closely enough to screen designs, or to tell a noisy reading from a real one?

FILE: records with "cnt" and "raw" (evolve.py's database or a results file - the design's runs), or loadtest.py's JSON
lines with "cnt" (the design's and s6's). Each (design, workload) a sample: time ns, and the counters. Two models, each
fitted per workload by least squares on the relative error (ns weighted 1/ns^2), K-fold by design (default 5): the
instructions alone, ns = a*instr + c; and the three, ns = a*instr + b*brmiss + l*llcmiss + c. Printed: per workload and
over all, the held-out folds' error |predicted - measured| / measured - median, 90th percentile, worst - and, per
design, the speed (the geometric mean over evolve.py's WORK_SEL of the design's time over s6's, both predicted where
s6's counters are in the file, else s6's measured median) predicted against measured: Spearman's rho and the median
error. Cycles are not a predictor (they are the time at a clock); they are reported, cycles / ns, as the clock seen.
No numpy: the normal equations of four unknowns, solved by elimination. As anyone, anywhere: reads only."""
import json, math, random, statistics, sys

WORK_SEL = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']
KEYS = ('instr', 'cycles', 'brmiss', 'llcmiss')

def samples(paths):
    """(design, side, workload) -> {ns, instr, cycles, brmiss, llcmiss}; side 'design' or 's6'."""
    S = {}
    for p in paths:
        for l in open(p, errors='replace'):
            l = l.strip()
            if not l.startswith('{'): continue
            try: r = json.loads(l)
            except ValueError: continue
            i, c = r.get('id'), r.get('cnt')
            if not i or not isinstance(c, dict): continue
            if 'design' in c or 's6' in c:                       # loadtest.py's line: sides, each workload a dict
                for side, ws in c.items():
                    for w, d in ws.items():
                        if d.get('instr', -1) > 0 and d.get('ns'): S[(i, side, w)] = dict(d)
            else:                                                # a record: workload -> [instr, cycles, brmiss, llcmiss]
                for w, v in c.items():
                    ns = (r.get('raw') or {}).get(w)
                    if ns and isinstance(v, list) and v and v[0] > 0: S[(i, 'design', w)] = dict(zip(KEYS, v), ns=ns)
    return S

def solve(A, b):
    n = len(b); M = [row[:] + [b[k]] for k, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-30: return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[k][n] / M[k][k] for k in range(n)]

def features(d, three):
    f = [d['instr']] + ([max(d.get('brmiss', 0), 0), max(d.get('llcmiss', 0), 0)] if three else [])
    return f + [1.0]

def fit(rows, three):
    """Least squares on relative error: minimise sum ((f.x - ns) / ns)^2."""
    k = len(features(rows[0], three)); A = [[0.0] * k for _ in range(k)]; b = [0.0] * k
    for d in rows:
        f = features(d, three); wt = 1.0 / d['ns'] ** 2
        for i in range(k):
            b[i] += wt * f[i] * d['ns']
            for j in range(k): A[i][j] += wt * f[i] * f[j]
    for i in range(k): A[i][i] += 1e-12 * (A[i][i] or 1.0)      # a counter all zeros must not make it singular
    return solve(A, b)

def predict(x, d, three):
    return sum(a * f for a, f in zip(x, features(d, three)))

def pct(v, q):
    v = sorted(v); return v[min(len(v) - 1, int(q * len(v)))] if v else float('nan')

def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o): r[i] = k
    return r

def spearman(a, b):
    n = len(a)
    if n < 3: return float('nan')
    ra, rb = rank(a), rank(b); return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))

def report(S, folds):
    designs = sorted({i for i, side, _ in S if side == 'design'})
    if len(designs) < folds: print('countfit: %d designs with counters - too few for %d folds' % (len(designs), folds)); return 1
    random.Random(711).shuffle(designs); fold = {i: k % folds for k, i in enumerate(designs)}
    works = sorted({w for _, _, w in S})
    clock = [d['cycles'] / d['ns'] for d in S.values() if d.get('cycles', -1) > 0]
    print('countfit: %d samples, %d designs, %d workloads; the clock seen (cycles / ns): median %.2f GHz' % (
        len(S), len(designs), len(works), statistics.median(clock) if clock else float('nan')))
    for three in (False, True):
        pred, errs = {}, {}
        for w in works:
            rows = [(i, side, d) for (i, side, w_), d in S.items() if w_ == w]
            for k in range(folds):
                train = [d for i, side, d in rows if side == 's6' or fold.get(i) != k]
                test = [(i, side, d) for i, side, d in rows if side == 'design' and fold.get(i) == k]
                if len(train) < 5 or not test: continue
                x = fit(train, three)
                if x is None: continue
                for i, side, d in test:
                    p = predict(x, d, three); pred[(i, w)] = p
                    errs.setdefault(w, []).append(abs(p - d['ns']) / d['ns'])
            s6 = [d for i, side, d in rows if side == 's6']
            if s6:
                x = fit([d for i, side, d in rows], three)
                if x: pred[('s6', w)] = statistics.median(predict(x, d, three) for d in s6)
        name = 'instructions, mispredictions, last-level misses' if three else 'instructions alone'
        allerr = [e for v in errs.values() for e in v]
        print('\n%s - held-out error by workload: median, 90th percentile, worst' % name)
        for w in works:
            if errs.get(w): print('  %-10s %5.1f %%  %5.1f %%  %5.1f %%  (%d)' % (w, 100 * statistics.median(errs[w]), 100 * pct(errs[w], 0.9), 100 * max(errs[w]), len(errs[w])))
        if allerr: print('  %-10s %5.1f %%  %5.1f %%  %5.1f %%  (%d)' % ('all', 100 * statistics.median(allerr), 100 * pct(allerr, 0.9), 100 * max(allerr), len(allerr)))
        ms, ps = [], []
        for i in designs:
            have = [w for w in WORK_SEL if (i, w) in pred and (i, 'design', w) in S]
            if len(have) < len(WORK_SEL): continue
            ref = lambda w, p: pred.get(('s6', w)) if p and ('s6', w) in pred else statistics.median(
                [d['ns'] for (j, side, w_), d in S.items() if side == 's6' and w_ == w] or [float('nan')])
            m = math.exp(sum(math.log(S[(i, 'design', w)]['ns'] / ref(w, False)) for w in have) / len(have))
            q = math.exp(sum(math.log(pred[(i, w)] / ref(w, True)) for w in have) / len(have))
            ms.append(m); ps.append(q)
        if ms and all(not math.isnan(v) for v in ms + ps):
            e = [abs(q - m) / m for m, q in zip(ms, ps)]
            print('  the speed (geometric mean over %s, to s6): %d designs, Spearman %.3f, error median %.1f %%, worst %.1f %%' % (
                ', '.join(WORK_SEL), len(ms), spearman(ms, ps), 100 * statistics.median(e), 100 * max(e)))
    return 0

def self_test():
    """A known model, its samples drawn with 2 % noise: the three-counter fit must find it, the instructions alone not."""
    rnd = random.Random(1); S = {}
    for n in range(60):
        for w in WORK_SEL + ['sieve']:
            instr = rnd.uniform(1e7, 5e8); br = instr * rnd.uniform(0.001, 0.03); llc = instr * rnd.uniform(0, 0.002)
            ns = (0.25 * instr + 15.0 * br + 60.0 * llc + 2e5) * rnd.gauss(1, 0.02)
            S[('d%02d' % n, 'design', w)] = dict(instr=instr, brmiss=br, llcmiss=llc, cycles=ns * 4.2, ns=ns)
            i6 = 3e8; ns6 = (0.25 * i6 + 15.0 * i6 * 0.02 + 60.0 * i6 * 0.001 + 2e5) * rnd.gauss(1, 0.02)   # its s6, measured beside it
            S[('d%02d' % n, 's6', w)] = dict(instr=i6, brmiss=i6 * 0.02, llcmiss=i6 * 0.001, cycles=ns6 * 4.2, ns=ns6)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): report(S, 5)
    out = buf.getvalue(); print(out)
    alone, three = out.split('instructions, mispredictions, last-level misses')
    med = lambda part: float(part.split('  all')[1].split('%')[0])
    ok = med(three) < 3.0 and med(alone) > med(three) and 'Spearman' in three and '4.20 GHz' in out
    print('countfit self-test: %s (median error %.1f %% three counters, %.1f %% instructions alone)' % ('PASS' if ok else 'FAIL', med(three), med(alone)))
    return 0 if ok else 1

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--self-test' in a: sys.exit(self_test())
    folds = 5
    if '--folds' in a: k = a.index('--folds'); folds = int(a[k + 1]); del a[k:k + 2]
    if not a: sys.exit(__doc__)
    sys.exit(report(samples(a), folds))
