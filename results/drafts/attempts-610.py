#!/usr/bin/env python3
"""results/drafts/attempts-610.py DB [STEP] - seed 87's two attempts side by side (Iteration 610).

The laptop crashed 10.5 hours into seed 87 (generation 136); the restart's replay forked at generation 3 (lab/evolve/
evolve.py's resume, fixed at 610), so the database holds two searches from the same seed and carried designs: attempt A
(the crashed one, generations 1-136) and attempt B (the resumed one, 1-262 - its generations 1-2 replayed A's records,
its own records from generation 3). Each attempt's hypervolume (lab/evolve/hv.py - the stopping rule's fixed box, the
true front) every STEP generations, beside the portable pool's 0.288890 (lab/evolve/portable.py): how much a longer run
adds, and how far two runs of one seed differ at the same generation.

A: the records written before B's first line. B's first line: the first record whose generation falls by more than 50
below the one before it, and the re-measures written just before it (gated designs of A's last generation, measured
again in B's first batch - A's designs, not B's). B: the carried designs, A's generations 1-2 (replayed), and B's own
records.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EV = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'lab', 'evolve')
sys.path.insert(0, EV)
db = sys.argv[1]; step = int(sys.argv[2]) if len(sys.argv) > 2 else 20
sys.argv = ['x']; import evolve as E
import hv

lines = []
for l in open(db, errors='replace'):
    if l.startswith('{'):
        try: lines.append(json.loads(l))
        except ValueError: pass
b = next(k for k in range(1, len(lines)) if (lines[k].get('gen') or 0) < (lines[k - 1].get('gen') or 0) - 50)
while 'speed1' in lines[b - 1]: b -= 1                          # B's first batch re-measured A's gated designs first
first = {}
for k, r in enumerate(lines): first.setdefault(r['id'], k)
RA, RB = {}, {}
for k, r in enumerate(lines):
    a_design = first[r['id']] < b
    if k < b: RA[r['id']] = r                                    # A as it stood at the crash
    if (a_design and (r.get('gen') or 0) <= 2 and k < b) or not a_design: RB[r['id']] = r
ga = max((r.get('gen') or 0) for r in RA.values()); gb = max((r.get('gen') or 0) for r in RB.values())
print('records: A %d (generations 0-%d), B %d (0-%d); B starts at line %d of %d' % (len(RA), ga, len(RB), gb, b, len(lines)))
print('| generation | A hypervolume | B hypervolume |')
print('|---|---|---|')
for g in list(range(step, max(ga, gb) + 1, step)) + [ga, gb]:
    va = hv.measure(db, E, gen=g, R=RA)['hv'] if g <= ga else None
    vb = hv.measure(db, E, gen=g, R=RB)['hv'] if g <= gb else None
    print('| %d | %s | %s |' % (g, '%.6f' % va if va is not None else '-', '%.6f' % vb if vb is not None else '-'), flush=True)
F = dict(fastest='speed', smallest='total', memory='rss', fastest32='speed32')
for n, R in (('A', RA), ('B', RB)):
    al = [r for r in R.values() if r.get('status') == 'ok' and all(r.get(f) for f in F.values())]
    print('%s at its end: %s' % (n, ', '.join('%s %s' % (k, ('%.4f' % min(r[f] for r in al)) if k.startswith('fastest') else min(r[f] for r in al)) for k, f in F.items())))
