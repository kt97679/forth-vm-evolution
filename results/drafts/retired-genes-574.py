#!/usr/bin/env python3
"""results/drafts/retired-genes-574.py TREE [BASE] - seed 84's failure (Iteration 574): KeyError 'jithelp' in crossover().

Seed 71's genomes (run at b5e9cbd, Iteration 498) hold jithelp, jitre and nocase, which Iteration 516 deleted;
canon() back-filled LATE genes but kept dead keys, and crossover(a, b) reads b[k] for every key of a. This reads every
genome record in results/evolve-amd-ryzen-7-pro-8840hs-seed70..83.md (the fronts' records, real data) and, with TREE's
evolve.py: each seed's keys beside a current genome's (canon of hand-made s6); 20 seeded crossovers each way of every
genome against s6 and against a seed-83 genome; mutate() and borrow() both ways. With BASE (another tree, e.g. master
before the fix): every genome's id by TREE equal to its id by BASE - the fix moves no design. Exit 1 on any failure.
"""
import glob, importlib.util, json, os, random, re, sys, collections

def load(tree, name):
    d = os.path.join(tree, 'lab', 'evolve'); sys.argv = ['evolve.py']; cwd = os.getcwd(); os.chdir(d)
    spec = importlib.util.spec_from_file_location(name, os.path.join(d, 'evolve.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); os.chdir(cwd); return m

tree = sys.argv[1]; base = sys.argv[2] if len(sys.argv) > 2 else None
E = load(tree, 'ev_tree'); B = load(base, 'ev_base') if base else None
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = collections.OrderedDict()
for n in range(70, 84):
    f = os.path.join(root, 'results', 'evolve-amd-ryzen-7-pro-8840hs-seed%d.md' % n)
    gs = []
    for l in open(f, errors='replace'):
        if l.startswith('{') and '"genome"' in l:
            try: gs.append(json.loads(l)['genome'])
            except ValueError: pass
    G[n] = gs
ref = E.canon(E.require(dict(E.HUMAN['s6-cv8b']))); keys = set(ref)
late = E.canon(E.require(G[83][0]))
bad = 0
print('seed  genomes  keys beyond a current genome (raw)  after canon  crossover/mutate/borrow failures  ids moved')
for n, gs in G.items():
    extra = collections.Counter(k for g in gs for k in g if k not in keys)
    after = collections.Counter(k for g in gs for k in E.canon(E.require(g)) if k not in keys)
    miss = collections.Counter(k for g in gs for k in keys if k not in E.canon(E.require(g)))
    fail = moved = 0; first = None
    for g in gs:
        c = E.canon(E.require(g))
        for s in range(20):
            for a, b in ((c, ref), (ref, c), (c, late), (late, c)):
                try: E.crossover(a, b, random.Random(s))
                except KeyError as e: fail += 1; first = first or repr(e)
            try: E.mutate(c, random.Random(s)); E.borrow(c, ref, random.Random(s)); E.borrow(ref, c, random.Random(s))
            except KeyError as e: fail += 1; first = first or repr(e)
        if B and E.gid(E.require(g)) != B.gid(B.require(g)): moved += 1
    bad += fail + moved + sum(after.values()) + sum(miss.values())
    print('%4d  %7d  %-34s  %-11s  %-32s  %s' % (n, len(gs), ','.join(sorted(extra)) or '-', ','.join(sorted(after)) or '-',
          ('%d %s' % (fail, first)) if fail else '0', moved if B else 'n/a'))
# carry_pool() end to end - the path seed 84 took: databases of seeds 71 and 83's records, then one with a genome
# missing a gene canon() cannot supply and express() never reads (skippad: not LATE, dormant in cv8 - the class jithelp was), which the guard must stop (TREE with the guard; else n/a).
import tempfile
tmp = tempfile.mkdtemp(); dbs = []
for n in (71, 83):
    p = os.path.join(tmp, 'archived-%d' % n, 'build', 'evolve', 'db.jsonl'); os.makedirs(os.path.dirname(p))
    with open(p, 'w') as f:
        for i, g in enumerate(G[n]): f.write(json.dumps(dict(id='%02d%08x' % (n, i), status='ok', speed=1.0 + i, size=10000 - i, genome=g)) + '\n')
    dbs.append(p)
pool = E.carry_pool(dbs, named={})
left = sum(1 for g, _, _ in pool if set(g) != keys)
print('carry_pool, seeds 71 and 83: %d carried, %d off the current genes' % (len(pool), left)); bad += left
p = os.path.join(tmp, 'archived-99', 'build', 'evolve', 'db.jsonl'); os.makedirs(os.path.dirname(p))
g = dict(G[83][0]); g.pop('skippad')
with open(p, 'w') as f: f.write(json.dumps(dict(id='9900000000', status='ok', speed=0.5, size=5000, genome=g)) + '\n')
try: E.carry_pool([p], named={}); print('the guard (a cv8 genome without skippad): not stopped' + (' - FAIL' if 'genes not current' in open(os.path.join(tree, 'lab/evolve/evolve.py')).read() else ' (no guard in TREE)')); bad += 'genes not current' in open(os.path.join(tree, 'lab/evolve/evolve.py')).read()
except SystemExit as e: print('the guard (a cv8 genome without skippad): stopped - %s' % e)
print('PASS' if not bad else 'FAIL')
sys.exit(1 if bad else 0)
