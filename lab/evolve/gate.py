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

    --set GENE=VALUE (any number of them): the gene forced on every design
    before it is built - a new gene's check across the fronts (Iteration 270;
    Iteration 268 checked factor=3 on seed 46's front with a script in /tmp). A
    design that does not express the forced value is counted apart, not built.

Until Iteration 256 this lived in /tmp, rewritten each time.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; force = {}
while '--set' in args:
    i = args.index('--set'); k, v = args[i + 1].split('=', 1); del args[i:i + 2]
    try: force[k] = json.loads(v)
    except ValueError: force[k] = v
if len(args) != 2: sys.exit(__doc__)
results, compare = args
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.setup()
run = [json.loads(l)['id'] for l in open(results) if l.startswith('{"bin"')]
line = [l for l in open(compare).read().split('\n') if l.startswith('The front of all runs together')]
joint = re.findall(r'\b([0-9a-f]{10}) [0-9.]+ at', line[0]) if line else []
ids = list(dict.fromkeys(run + joint)); bad = apart = 0
for did in ids:
    d = os.path.join(E.EV, 'gate')
    try:
        g = E.recorded_genome(did)
        if g is None: raise RuntimeError('no recorded genome')
        g = dict(E.canon(g), **force)
        if any(E.express(g).get(k) != v for k, v in force.items()): apart += 1; continue
        eng, img = E.build(E.canon(g), d); E.alive(eng, img, E.private_work(d))
    except Exception as e:
        bad += 1; print('DIED', did, str(e)[:120], flush=True)
print('alive: %d of %d (the run\'s front %d, the joint front %d, %d in both)%s' % (
    len(ids) - apart - bad, len(ids) - apart, len(run), len(joint), len(run) + len(joint) - len(ids),
    ('; with %s, %d not expressing it' % (' '.join('%s=%s' % kv for kv in force.items()), apart)) if force else ''), flush=True)
sys.exit(1 if bad or len(ids) == apart else 0)
