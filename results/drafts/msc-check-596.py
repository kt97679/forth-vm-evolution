#!/usr/bin/env python3
"""results/drafts/msc-check-596.py - the msc retirement checked without building (Iteration 596).
Run in a tree (its lab/evolve/evolve.py): every recorded design of the pooled runs (rtloop-check-595.py's pool - the
series' and the confirmation runs' results files, every record), the final pick's candidates, the shortlist, the final
set and the hand-made stages - by set, how many express msc on (express(canon(g)), the build's view: build() now
refuses them), how many carry msc=1 unexpressed (tos 0) and whether FROZEN's msc 0 changes any expression. express() and canon() are untouched by the patch, so
every id stands; the patch is right when no candidate, shortlist, final-set or hand-made design is among them."""
import json, os, sys
HERE = os.path.join(os.getcwd(), 'lab', 'evolve'); sys.path.insert(0, HERE)
sys.argv = ['x']
import evolve as E
import importlib.util, hv, stopping
s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(s); s.loader.exec_module(CF)
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 87]
SETS = {'pool': {}}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, 87)):
    for i, r in hv.load(f, E).items(): SETS['pool'].setdefault(i, r['genome'])
for n, f in (('candidates', 'results/candidates-final-seed86.md'), ('shortlist', 'results/shortlist-seed86.md'), ('final set', 'results/final-set-seed86.md')):
    SETS[n] = {}
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); SETS[n].setdefault(r['id'], r['genome'])
SETS['hand-made'] = dict(E.HUMAN)
bad = False
for n, G in SETS.items():
    on = sorted(i for i, g in G.items() if g.get('enc') == 'cv8' and E.express(E.canon(g)).get('msc'))
    req = [g for g in G.values() if g.get('enc') == 'cv8' and E.require(g).get('msc') != g.get('msc', 0)]
    moved = sum(1 for g in req if E.express(E.canon(E.require(g))) != E.express(E.canon(dict(E.require(g), msc=g['msc']))))
    print('%-10s %5d designs, %4d express msc on, %4d msc=1 in the genome, %d of them expressed differently by FROZEN\'s msc 0%s'
          % (n, len(G), len(on), len(req), moved, ' - ' + ' '.join(on[:8]) if on and n != 'pool' else ''))
    if (on or moved) and n != 'pool': bad = True
print('msc-check-596: %s' % ('FAIL - a design the final pick can choose expresses msc' if bad else 'PASS - msc on no candidate, shortlist, final-set or hand-made design'))
sys.exit(1 if bad else 0)
