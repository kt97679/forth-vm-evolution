#!/usr/bin/env python3
"""lab/evolve/lifted.py DB - the lifted freezes on a run's true front (Iteration 557). Each gene the owner unfroze at 556
(evolve.py's FROZEN until then): the share of the true front at each of its values (canon's, as a design is built), and
the enrichment of its non-frozen values - their share of the front over their share of every alive design. Then
prediction 556 scored: bytehdr, thinhdr, bss and lean at 1 on 95% or more of the front; alignhot, msc and sharedcall
each on under 10%; doesfar and varcall at 1 on every design. As the build user (it imports the evolver)."""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LIFTED = {'bytehdr': 1, 'doesfar': 1, 'thinhdr': 1, 'varcall': 1, 'bss': 1, 'lean': 1, 'msc': 0, 'scale': 0, 'sharedcall': 0, 'alignhot': 0}
if len(sys.argv) < 2: sys.exit(__doc__)
db = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E, hv
R = {}
for l in open(db, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'):
            r['total'] = E.ov(r, 'total') if r.get('status') == 'ok' and (r.get('total') or r.get('size')) else r.get('total'); R[r['id']] = r
F = hv.true_front(R, E)
A = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('speed32')]
X = {i: E.canon(R[i]['genome']) for i in set(F) | set(A)}
print('lifted.py: %s - the true front %d, alive %d' % (db, len(F), len(A)))
print('| gene | frozen at, until 556 | the front, at each value | enrichment of the other values |'); print('|---|---|---|---|')
share = {}
for k, f in LIFTED.items():
    cf = collections.Counter(X[i].get(k, f) for i in F); ca = collections.Counter(X[i].get(k, f) for i in A)
    share[k] = {v: c / len(F) for v, c in cf.items()}
    en = ', '.join('%s: %.2f' % (v, (cf[v] / len(F)) / (ca[v] / len(A))) for v in sorted(ca) if v != f and ca[v]) or '-'
    print('| %s | %s | %s | %s |' % (k, f, ', '.join('%s %.0f%%' % (v, 100 * cf[v] / len(F)) for v in sorted(cf)), en))
on = lambda k, v: share[k].get(v, 0.0)
c1 = all(on(k, 1) >= 0.95 for k in ('bytehdr', 'thinhdr', 'bss', 'lean'))
c2 = all(1 - on(k, 0) < 0.10 for k in ('alignhot', 'msc', 'sharedcall'))
c3 = all(on(k, 1) == 1.0 for k in ('doesfar', 'varcall'))
print('prediction 556 (the freezes were right): %s - bytehdr, thinhdr, bss, lean at 1 on 95%%+: %s; alignhot, msc, sharedcall each '
      'on under 10%%: %s; doesfar and varcall at 1 everywhere: %s' % ('HOLDS' if c1 and c2 and c3 else 'FAILS', *('yes' if c else 'no' for c in (c1, c2, c3))))
