#!/usr/bin/env python3
"""results/drafts/seed74-front-549.py DB REPORT - seed 74's fronts (Iteration 549): the true one from the records
(evolve.py's first_front, by dominates()), the results file's, and the old staircase's on the same records (7da6566's
first_front - prediction 527); the one-round audits (529); the operators' shares (526); the JIT genes (534); the
extremes."""
import json, os, re, subprocess, sys, types
dbp, rep = sys.argv[1], sys.argv[2]
EVD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lab/evolve')
sys.argv = ['x']; sys.path.insert(0, EVD); import evolve as E
O = types.ModuleType('old_evolve'); O.__file__ = os.path.join(EVD, 'evolve.py')
exec(compile(subprocess.run(['git', '-C', EVD, 'show', '7da6566:lab/evolve/evolve.py'], capture_output=True, text=True, check=True).stdout, 'old_evolve', 'exec'), O.__dict__)
R = {}
for l in open(dbp, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): R[r['id']] = r
ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss')]
E.TWO_WIDTHS[0] = O.TWO_WIDTHS[0] = sum(1 for i in ok if R[i].get('speed32')) * 2 > len(ok)
if E.TWO_WIDTHS[0]: ok = [i for i in ok if R[i].get('speed32')]
true = E.first_front(ok, R); old = O.first_front(ok, R); T, Od = set(true), set(old)
reported = set(m.group(1) for m in (re.match(r'\| ([0-9a-f]{10}) \|', l) for l in open(rep, errors='replace')) if m)
print('true front %d; the results file\'s %d (%d in both, %d only there); the old staircase %d (%d in the true front) - true / old %.2f'
      % (len(T), len(reported), len(T & reported), len(reported - T), len(Od), len(T & Od), len(T) / max(1, len(Od))))
xr = [R[i] for i in reported - T]
if xr: print('  only in the results file: %d - statuses %s, gated %s, with a 32-bit speed %d' % (len(xr), sorted(set(r.get('status') for r in xr)),
             sorted(set(r.get('gated') for r in xr)), sum(1 for r in xr if r.get('speed32'))))
sa = [i for i, r in R.items() if r.get('stopaudit')]
print('one round first: stopped %d; audited in full %d, of them alive %d, on the true front %d, on the results file\'s %d' % (
      sum(1 for r in R.values() if r.get('status') == 'stopped after one round'), len(sa), sum(1 for i in sa if R[i].get('status') == 'ok'), len(T & set(sa)), len(reported & set(sa))))
kids = [r for r in R.values() if (r.get('gen') or 0) > 0]
cls = lambda h: 'crossover' if h.startswith('crossover') else 'borrowed' if ' from ' in h else 'mutation'
top = max(k['gen'] for k in kids)
for name, grp in (('the run', kids), ('the last fifth', [r for r in kids if r['gen'] > 0.8 * top])):
    c = {}; [c.__setitem__(cls(r.get('how', '')), c.get(cls(r.get('how', '')), 0) + 1) for r in grp]
    print('children, %s: %d - %s' % (name, len(grp), ', '.join('%s %.1f%%' % (k, 100.0 * v / len(grp)) for k, v in sorted(c.items()))))
print('front entries per child: %d of %d children - %.3f%%' % (sum(1 for i in T if (R[i].get('gen') or 0) > 0), len(kids), 100.0 * sum(1 for i in T if (R[i].get('gen') or 0) > 0) / len(kids)))
f = min(true, key=lambda i: R[i]['speed']); s = min(true, key=lambda i: E.ov(R[i], 'total')); m = min(true, key=lambda i: R[i]['rss']); w = min(true, key=lambda i: R[i]['speed32'])
print('extremes: fastest %s %.4f; smallest %s %s bytes; least memory %s KB; fastest at 32 bits %s %.4f' % (f, R[f]['speed'], s, '{:,}'.format(E.ov(R[s], 'total')), R[m]['rss'], w, R[w]['speed32']))
ex = {i: E.express(E.canon(R[i]['genome'])) for i in true}; jit = [i for i in true if E.jit_on(E.canon(R[i]['genome']))]
k = max(1, len(true) // 10); fast = sorted(true, key=lambda i: R[i]['speed'])[:k]; fj = [i for i in fast if i in jit]
q = sorted(true, key=lambda i: E.qual(R[i]))[:k] if hasattr(E, 'qual') else []
print('JIT designs %d of %d; in the fastest tenth (%d) %d' % (len(jit), len(true), k, len(fj)))
for g in ('jitexec', 'jitfuse', 'jitmul', 'jitos', 'jitrp'):
    print('  %-8s %3d of the JIT designs, %2d of the fastest tenth\'s, %d of the best-Q tenth' % (g, sum(1 for i in jit if ex[i].get(g)), sum(1 for i in fj if ex[i].get(g)), sum(1 for i in q if ex[i].get(g))))
