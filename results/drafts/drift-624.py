# results/drafts/drift-624.py [DB] - a carryall run's carried designs measured again, against their pool readings: a drift
# check between runs (Iteration 624; results/drafts/gain-designs-624.md). DB: seed 89's db.jsonl (default: its pack under
# /tmp/process); the pool before seed 89, as confirm.py's. As the build user, from the repository's root.
import json, statistics, sys, os
DB = sys.argv[1] if len(sys.argv) > 1 else '/tmp/process/forth-vm-evolution-seed89-eca15d532f-fury-20261108-020020/pack/db.jsonl'
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']
import evolve as E, hv, stopping, confirm
L = stopping.LEDGER; method, runs = stopping.series(L)
runs = [r for r in runs if r['seed'] < 89] + confirm.confirmations(L, 89) + confirm.portables(L, 89)
pool = confirm.pool_files(runs)
P = {}
src = {}
for f in pool:
    d = hv.load(f, E); P.update(d)
    for i in d: src[i] = os.path.basename(f)
R = hv.load(DB, E)
both = [i for i in R if i in P and R[i].get('status') == 'ok' and P[i].get('speed') and R[i].get('speed')]
def q(xs):
    xs = sorted(xs); n = len(xs)
    return 'median %.4f, quartiles %.4f-%.4f (n %d)' % (statistics.median(xs), xs[n // 4], xs[3 * n // 4], n)
for k in ('speed', 'speed32'):
    xs = [R[i][k] / P[i][k] for i in both if R[i].get(k) and P[i].get(k)]
    print(k, 'seed 89 / pool:', q(xs))
    fast = [R[i][k] / P[i][k] for i in both if R[i].get(k) and P[i].get(k) and P[i][k] < 0.2]
    if fast: print('  the fast end (pool reading under 0.2):', q(fast))
by = {}
for i in both:
    if R[i].get('speed32') and P[i].get('speed32'): by.setdefault(src[i], []).append(R[i]['speed32'] / P[i]['speed32'])
for s, xs in sorted(by.items()): print('  32-bit by source', s.replace('evolve-amd-ryzen-7-pro-8840hs-', ''), q(xs))
