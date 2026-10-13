#!/usr/bin/env python3
"""gate.py RESULTS COMPARE - step 8 of processing a returned seed (Iteration 256).

Every design of the run's front (RESULTS: results/evolve-<machine>-seedN.md, the
records the pack's report.md carries) and of the joint front (COMPARE: the
comparison pack's compare-fronts.md, its "The front of all runs together" line)
built with this tree's code and run on the corpus. Earlier runs' genomes come
from their results files, as everywhere (E.recorded_genome).

    python3 lab/evolve/gate.py results/evolve-amd-ryzen-7-pro-8840hs-seed46.md \\
        /tmp/c46/pack/compare-fronts.md
    -> alive: 148 of 148 (the run's front 127, the joint front 72, 51 in both)

Until Iteration 256 this lived in /tmp, rewritten each time.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) != 3: sys.exit(__doc__)
results, compare = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.setup()
run = [json.loads(l)['id'] for l in open(results) if l.startswith('{"bin"')]
line = [l for l in open(compare).read().split('\n') if l.startswith('The front of all runs together')]
joint = re.findall(r'\b([0-9a-f]{10}) [0-9.]+ at', line[0]) if line else []
ids = list(dict.fromkeys(run + joint)); bad = 0
for did in ids:
    d = os.path.join(E.EV, 'gate')
    try:
        g = E.recorded_genome(did)
        if g is None: raise RuntimeError('no recorded genome')
        eng, img = E.build(E.canon(g), d); E.alive(eng, img, E.private_work(d))
    except Exception as e:
        bad += 1; print('DIED', did, str(e)[:120], flush=True)
print('alive: %d of %d (the run\'s front %d, the joint front %d, %d in both)' % (
    len(ids) - bad, len(ids), len(run), len(joint), len(run) + len(joint) - len(ids)), flush=True)
sys.exit(1 if bad else 0)
