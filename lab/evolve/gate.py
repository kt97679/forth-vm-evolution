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
    before it is built - a list's members put first, ahead of the design's own,
    so they take its opcode slots (Iteration 290) - a new gene's check across the fronts (Iteration 270;
    Iteration 268 checked factor=3 on seed 46's front with a script in /tmp). A
    design that does not express the forced value is counted apart, not built.

    --db FILE (any number): genomes from a run's database too, for designs no
    results file holds yet (Iteration 288: seed 48's pack had not come back, its
    front in seed 49's database as carried records).

Until Iteration 256 this lived in /tmp, rewritten each time.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; force = {}; dbs = []
while '--db' in args:
    i = args.index('--db'); dbs.append(args[i + 1]); del args[i:i + 2]
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
DBG = {}
for db in dbs:
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'id' in r and 'genome' in r: DBG.setdefault(r['id'], r['genome'])
for did in ids:
    d = os.path.join(E.EV, 'gate')
    try:
        g = E.recorded_genome(did) or DBG.get(did)
        if g is None: raise RuntimeError('no recorded genome')
        g = dict(E.canon(g))
        for k, v in force.items():          # Iteration 290: a list's members go first, then the design's own - so they
            g[k] = v + [x for x in (g.get(k) or []) if x not in v] if isinstance(v, list) else v   # take the slots (ops10_in)
        e_ = E.express(g)
        if any((not set(v) <= set(e_.get(k) or [])) if isinstance(v, list) else e_.get(k) != v for k, v in force.items()): apart += 1; continue
        eng, img = E.build(E.canon(g), d); E.alive(eng, img, E.private_work(d))
    except Exception as e:
        bad += 1; print('DIED', did, str(e)[:120], flush=True)
print('alive: %d of %d (the run\'s front %d, the joint front %d, %d in both)%s' % (
    len(ids) - apart - bad, len(ids) - apart, len(run), len(joint), len(run) + len(joint) - len(ids),
    ('; with %s, %d not expressing it' % (' '.join('%s=%s' % kv for kv in force.items()), apart)) if force else ''), flush=True)
sys.exit(1 if bad or len(ids) == apart else 0)
