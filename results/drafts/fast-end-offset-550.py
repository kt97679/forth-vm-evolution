#!/usr/bin/env python3
"""results/drafts/fast-end-offset-550.py DB REMEASURE - where the fast end's offset comes from (Iteration 550): the
front measured again after the run (remeasure.json: 6 rounds, one design at a time) against the same designs' readings
in the run (db.jsonl: 3 rounds, four workers; a gated design's speed the geometric mean of two readings) - by in-run
rank, JIT or not, per workload; and the gate's two in-run readings against each other, the noise and luck the run's
own records hold."""
import json, math, os, statistics as st, sys
dbp, rmp = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lab/evolve')); import evolve as E
R = {}
for l in open(dbp, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): R[r['id']] = r
M = json.load(open(rmp))
W = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']
q = lambda xs, f: sorted(xs)[min(len(xs) - 1, int(f * len(xs)))]
def desc(xs): return 'median %.3f (quartiles %.3f-%.3f, %d)' % (st.median(xs), q(xs, .25), q(xs, .75), len(xs)) if xs else '-'
ids = sorted((i for i in M if i in R and R[i].get('speed')), key=lambda i: R[i]['speed'])
rat = {i: M[i]['speed'] / R[i]['speed'] for i in ids}
print('re-measured / in-run, the %d designs measured again (the front\'s fastest, by in-run speed):' % len(ids))
for a, b in ((0, 10), (10, 30), (30, 60), (60, len(ids))):
    g = ids[a:b]
    if g: print('  in-run ranks %3d-%3d (%.3f-%.3f): %s' % (a + 1, a + len(g), R[g[0]]['speed'], R[g[-1]]['speed'], desc([rat[i] for i in g])))
jit = {i: bool(E.jit_on(E.canon(R[i]['genome']))) for i in ids}
for name, g in (('JIT', [i for i in ids if jit[i]]), ('no JIT', [i for i in ids if not jit[i]])): print('  %-6s %s' % (name, desc([rat[i] for i in g])))
print('per workload, re-measured / in-run (design / s6 on each):')
for w in W + ['sieve', 'parse']:
    x = [M[i]['t'][w] / R[i]['t'][w] for i in ids if w in M[i].get('t', {}) and (R[i].get('t') or {}).get(w)]
    xj = [M[i]['t'][w] / R[i]['t'][w] for i in ids if jit[i] and w in M[i].get('t', {}) and (R[i].get('t') or {}).get(w)]
    print('  %-9s %s; JIT %s' % (w, desc(x), ('%.3f' % st.median(xj)) if xj else '-'))
g2 = [r for r in R.values() if r.get('speed1') and r.get('speed2') and r.get('status') == 'ok']
d = [r['speed2'] / r['speed1'] for r in g2]
sd = st.pstdev([math.log(x) for x in d]) if len(d) > 1 else 0
print('the gate\'s two in-run readings - second / first, every gated design: %s; one reading\'s noise about %.1f%%' % (desc(d), 100 * sd / math.sqrt(2)))
g3 = [i for i in ids if R[i].get('speed1') and R[i].get('speed2')]
print('  of the re-measured: %d gated - second / first %s; re-measured / in-run %s' % (len(g3), desc([R[i]['speed2'] / R[i]['speed1'] for i in g3]), desc([rat[i] for i in g3])))
print('  re-measured / the second in-run reading alone: %s' % desc([M[i]['speed'] / R[i]['speed2'] for i in g3]))
