#!/usr/bin/env python3
"""results/drafts/bred-gain-sensitivity-575.py DB --seed N - how firm is the stricter criterion's gain (confirm.py, 573)?
Iteration 575, seed 84: the pool and its bred front designs +1.2%, the bar 1%. In-run speeds at the fast end are
optimistic (review-checks curse: the fastest tenth re-measured / in-run, median 1.066), so this prints:
  1. the carried designs' speeds in this run against their own pool records (the pool's optimism, measured);
  2. the gain from the bred designs by thirds of speed, and without the ones faster than the pool's fastest;
  3. the gain with every bred design's two speeds multiplied by f - the f at which it falls under the bar.
Run from the repository root, as confirm.py is."""
import json, os, statistics, sys
sys.path.insert(0, 'lab/evolve')
import hv, stopping, confirm

a = sys.argv[1:]; db = a[0]; N = int(a[a.index('--seed') + 1])
sys.argv = ['x']; import evolve as E
b = json.load(open(hv.BOUNDS)); _, runs = stopping.series(stopping.LEDGER)
runs = [r for r in runs if r['seed'] < N] + confirm.confirmations(stopping.LEDGER, N)
P = {}
for f in confirm.pool_files(runs): P.update(hv.load(f, E))
PF, ph = confirm.front_hv(P, E, b)
R = hv.load(db, E); T = hv.true_front(R, E)
bred = [i for i in T if not str(R[i].get('how', '')).startswith(confirm.CARRIED)]

def hvwith(recs):
    U = dict(P); U.update(recs); return confirm.front_hv(U, E, b)[1]

# 1. the carried: the same design re-timed in this run against its pool record
both = [i for i, r in R.items() if str(r.get('how', '')).startswith(confirm.CARRIED) and r.get('status') == 'ok'
        and r.get('speed') and i in P and P[i].get('speed')]
fast = sorted(PF, key=lambda i: P[i]['speed'])[:max(1, len(PF) // 10)]
for nm, ids in (('every carried design in the pool', both), ("the pool front's fastest tenth", [i for i in fast if i in both])):
    q = [R[i]['speed'] / P[i]['speed'] for i in ids]
    if q: print('%s: %d re-timed here, this run / pool speed median %.3f, range %.3f-%.3f' % (nm, len(q), statistics.median(q), min(q), max(q)))

# 2. each bred design's exclusive share
hb = hvwith({i: R[i] for i in bred}); g = hb - ph
pf = min(P[i]['speed'] for i in PF)
print('\nthe pool %.5f, with the bred %.5f (%+.2f%%); the bar %.5f; the pool front\'s fastest %.4f' % (ph, hb, 100 * (hb / ph - 1), ph * 1.01, pf))
fa = [i for i in bred if R[i]['speed'] < pf]
hn = hvwith({i: R[i] for i in bred if i not in fa})
print('without the %d bred designs faster than the pool\'s fastest: %.5f (%+.2f%%)' % (len(fa), hn, 100 * (hn / ph - 1)))
q = sorted(bred, key=lambda i: R[i]['speed']); k = len(q) // 3
for nm, grp in (('the fastest third', q[:k]), ('the middle third', q[k:2 * k]), ('the slowest third', q[2 * k:])):
    h = hvwith({i: R[i] for i in grp})
    print('  %s alone (%d, speed %.4f-%.4f): %+.2f%%' % (nm, len(grp), R[grp[0]]['speed'], R[grp[-1]]['speed'], 100 * (h / ph - 1)))

# 3. the bred designs' speeds made slower by f
print('\nf (bred speeds x f)   the pool with the bred   gain')
cross = None
for f in (1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.066):
    h = hvwith({i: dict(R[i], speed=R[i]['speed'] * f, speed32=R[i]['speed32'] * f) for i in bred})
    print('  %.3f               %.5f                %+.2f%%%s' % (f, h, 100 * (h / ph - 1), '  under the bar' if h < ph * 1.01 else ''))
    if cross is None and h < ph * 1.01: cross = f
print('the gain falls under the bar at f = %s' % (cross or 'none tried'))
