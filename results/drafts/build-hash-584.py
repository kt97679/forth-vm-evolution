#!/usr/bin/env python3
"""results/drafts/build-hash-584.py OUT.jsonl [--cell4] [--limit K] [--only ID,ID] - every design that matters, built by evolve.py's
own build() and hashed (Iteration 584): the pooled true front (retire-report-579.py's pool: the series' and the
confirmation runs' results files), the final pick's candidates (results/candidates-final-seed86.md) and the hand-made
stages. One JSON line a design: {"id", "cell", "engine", "image"} - sha256 of the engine as it ships and of the image -
or {"id", "cell", "died"}. --cell4: as eval32 builds it - setup_widths() first, at_width(WIDTH4), the scale above 2 read as 2. Each design builds in a
fixed directory (/tmp/build-hash/CELL/ID), so a path the compiler keeps is the same in both runs.
The test of a retirement patch (consolidation, the owner at 584: "if it will not lose good designs"): this run on master,
then on the patched tree; every design not using a retired value must hash the same - the same engine bytes and image
bytes, so the same design, measured or not. A design using a retired value is named, not compared."""
import hashlib, json, os, shutil, sys
a = sys.argv[1:]; out = a[0]; lim = None; only = None
if '--limit' in a: lim = int(a[a.index('--limit') + 1])
w4 = '--cell4' in a
if '--only' in a: only = set(a[a.index('--only') + 1].split(','))
HERE = os.path.join(os.getcwd(), 'lab', 'evolve'); sys.path.insert(0, HERE)
sys.argv = ['x']; import evolve as E
import importlib.util, hv, stopping
s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(s); s.loader.exec_module(CF)
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 87]
P = {}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, 87)): P.update(hv.load(f, E))
G = {i: P[i]['genome'] for i in hv.true_front(P, E)}
for l in open('results/candidates-final-seed86.md'):
    if l.startswith('{'): r = json.loads(l); G.setdefault(r['id'], r['genome'])
for k, g in E.HUMAN.items(): G[k] = g
ids = [i for i in sorted(G) if not only or i in only][:lim]
if w4: E.TWO_WIDTHS[0] = True; E.setup_widths()   # the 4-byte references at_width swaps in, as a run's start builds them
cell = '4' if w4 else '8'; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
n = 0
with open(out, 'w') as f:
    for i in ids:
        d = '/tmp/build-hash/%s/%s' % (cell, i); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        try:
            g = dict(G[i])
            if w4:
                if (g.get('scale') or 0) > 2: g['scale'] = 2
                with E.at_width(E.WIDTH4): eng, img = E.build(E.canon(g), d)
            else: eng, img = E.build(E.canon(g), d)
            rec = {'id': i, 'cell': cell, 'engine': sha(eng), 'image': sha(img)}
        except Exception as x: rec = {'id': i, 'cell': cell, 'died': str(x)[:160]}
        f.write(json.dumps(rec) + '\n'); f.flush(); n += 1
        shutil.rmtree(d, ignore_errors=True)
print('%d designs hashed at %s-byte cells -> %s' % (n, cell, out))
