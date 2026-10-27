#!/usr/bin/env python3
"""results/drafts/fast-end-offset-554.py PACK - the fast end's offset tested on a run's own re-measure (Iteration 554).
Is it a cost every process pays outside user space - the lead from seed 75's clock test, the cycle ratio unmoved where
the time moved - or one only the JIT designs pay? remeasure.json's designs, re-measured alone at the run's end, against
their in-run numbers (db.jsonl), by the JIT (E.jit_on, as draft-results.py counts it) and by speed. A cost every process
pays - the same absolute time for a design and its paired s6 - moves a ratio r by c(1 - r): an absolute shift growing as
r falls, JIT or not. A cost only JIT code pays moves only the JIT designs; a uniform slowdown moves every ratio by k*r.
No new timing: the run's records. PACK: an unpacked seed pack (db.jsonl, remeasure.json)."""
import json, os, sys, statistics as st
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')
pack = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
R = {}
for l in open(os.path.join(pack, 'db.jsonl'), errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): R[r['id']] = r
M = json.load(open(os.path.join(pack, 'remeasure.json')))
WL = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']
D = []
for i, m in M.items():
    r = R.get(i)
    if not r or not r.get('speed') or not m.get('speed'): continue
    D.append(dict(id=i, r=r['speed'], m=m['speed'], j=bool(E.jit_on(E.canon(r['genome']))), t=r.get('t', {}), u=m.get('t', {})))
med = lambda xs: st.median(xs) if xs else float('nan')
print('%d designs re-measured, %d JIT; in-run speed %.3f-%.3f' % (len(D), sum(d['j'] for d in D), min(d['r'] for d in D), max(d['r'] for d in D)))
print('\nre-measured / in-run, by in-run speed (median, n):')
B = [(0, .2), (.2, .3), (.3, .5), (.5, 1.0), (1.0, 9)]
for lo, hi in B:
    row = []
    for j in (True, False):
        q = [d['m'] / d['r'] for d in D if lo <= d['r'] < hi and d['j'] == j]
        row.append('%s %.3f (%d)' % ('JIT' if j else 'non-JIT', med(q), len(q)) if q else '%s - (0)' % ('JIT' if j else 'non-JIT'))
    print('  %.1f-%.1f: %s' % (lo, hi, ';  '.join(row)))
def fit(X, y):            # least squares through the origin, one or two regressors
    if len(X[0]) == 1:
        a = sum(x[0] * v for x, v in zip(X, y)) / sum(x[0] ** 2 for x in X); c = (a,)
    else:
        s11 = sum(x[0] ** 2 for x in X); s22 = sum(x[1] ** 2 for x in X); s12 = sum(x[0] * x[1] for x in X)
        b1 = sum(x[0] * v for x, v in zip(X, y)); b2 = sum(x[1] * v for x, v in zip(X, y)); det = s11 * s22 - s12 ** 2
        c = ((b1 * s22 - b2 * s12) / det, (b2 * s11 - b1 * s12) / det)
    sse = sum((v - sum(ci * xi for ci, xi in zip(c, x))) ** 2 for x, v in zip(X, y)); return c, sse
y = [d['m'] - d['r'] for d in D]; s0 = sum(v * v for v in y)
print('\nthe shift re-measured - in-run, fitted (share of its sum of squares explained):')
for name, X in (('every process, c(1-r)', [(1 - d['r'],) for d in D]), ('JIT only, d', [(1.0 * d['j'],) for d in D]),
                ('uniform, k*r', [(d['r'],) for d in D]), ('both, c(1-r) + d*JIT', [(1 - d['r'], 1.0 * d['j']) for d in D])):
    c, sse = fit(X, y); print('  %-22s %s  explained %.0f%%' % (name, ', '.join('%+.4f' % v for v in c), 100 * (1 - sse / s0)))
G = [('JIT, under 0.2', lambda d: d['j'] and d['r'] < .2), ('JIT, 0.2-0.33', lambda d: d['j'] and .2 <= d['r'] < .33),
     ('non-JIT, 0.33-0.5', lambda d: not d['j'] and .33 <= d['r'] < .5), ('non-JIT, 0.5-1', lambda d: not d['j'] and .5 <= d['r'] < 1),
     ('non-JIT, 1 and over', lambda d: not d['j'] and d['r'] >= 1)]
S = {}                    # s6's own in-run time a workload, ns: raw / t over every design - one s6, so one number each
for w in WL + ['sieve', 'parse']:
    S[w] = med([R[d['id']]['raw'][w] / d['t'][w] for d in D if R[d['id']].get('raw', {}).get(w) and d['t'].get(w)])
print('\ns6 in the run, a workload: ' + ', '.join('%s %.1f ms' % (w, S[w] / 1e6) for w in S))
print('\nby workload, re-measured / in-run (median) - then the cost c(1-t) implies, d = (t\' - t) S / (1 - t), in us:')
print('  %-10s' % 'workload' + ''.join('%22s' % g for g, _ in G))
for w in WL + ['sieve', 'parse']:
    q = lambda f: med([d['u'][w] / d['t'][w] for d in D if f(d) and d['t'].get(w) and d['u'].get(w)])
    dl = lambda f: med([(d['u'][w] - d['t'][w]) * S[w] / (1 - d['t'][w]) / 1e3 for d in D if f(d) and d['t'].get(w) and d['u'].get(w) and abs(1 - d['t'][w]) > .2])
    print('  %-10s' % w + ''.join('%22s' % ('%.3f  %+6.0f us' % (q(f), dl(f))) for _, f in G) + ('   (held out)' if w in ('sieve', 'parse') else ''))
print('  %-10s' % 'designs' + ''.join('%22d' % sum(1 for d in D if f(d)) for _, f in G))
