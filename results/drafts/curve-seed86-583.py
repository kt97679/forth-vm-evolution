#!/usr/bin/env python3
"""results/drafts/curve-seed86-583.py DB - a run's improvement over its generations (Iteration 583): the true front's
fixed-box hypervolume of every record up to generation g (hv.measure, the box hv-bounds.json), and the four extremes
from every alive design up to g (stopping.py's curve arithmetic). DB: a seed pack's db.jsonl. Run from the repository root.
Seed 86 (the second confirmation run, carryall): hv 0.37071 at generation 0 (the founders re-timed), 0.36933 at 91; the
fastest 0.1330, the least memory 104 KB and the fastest at 32 bits 0.1645 all at generation 0; the smallest 13,973 ->
13,939 (gens 30, 60) - seven hours of evolution from the pooled front added nothing past the bars."""
import sys
db = sys.argv[1]
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E, hv
R = hv.load(db, E)
F = dict(fastest='speed', smallest='total', memory='rss', fast32='speed32')
A = [r for r in R.values() if r.get('status') == 'ok' and all(r.get(f) for f in F.values())]
gens = max((r.get('gen') or 0) for r in A)
print('records', len(R), '- alive with all four', len(A), '- generations 0-%d' % gens)
for g in sorted({0, 10, 20, 30, 45, 60, 75, gens}):
    m = hv.measure(db, E, gen=g, R=R); B = [r for r in A if (r.get('gen') or 0) <= g]
    x = {k: min(r[f] for r in B) for k, f in F.items()}
    print('gen %3d: hv %.5f  fastest %.4f  smallest %d  memory %d  fastest32 %.4f' % (g, m['hv'], x['fastest'], x['smallest'], x['memory'], x['fast32']))
