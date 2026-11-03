#!/usr/bin/env python3
"""results/drafts/rtloop-check-595.py OUT.json [BEFORE.json] - the rtloop=2 retirement checked without building (Iteration 595).
Run in a tree (its lab/evolve/evolve.py): every recorded design of the pooled runs (build-hash-584.py's pool - the series'
and the confirmation runs' results files, every record, not only the true front), the final pick's candidates, the
shortlist, the final set and the hand-made stages -> OUT.json {id: [express(canon(g)) as JSON, headerless]}, where
headerless is whether the build passes the loop overlay's internal words to layout.py --headerless (rtloop=2 without
rtloopall - the one place rtloop=2 reached the build). With BEFORE.json (the same run on the tree before the patch):
every design compared - its expressed genes (its id and every gene build() reads through express) the same, and named
where not. The patch touches evolve.py alone, and rtloop reaches _build() only by rtloop_on() (its truth, which 2 -> 1
keeps) and the headerless line, so a design with the same expression and no headerless loop words builds the same bytes."""
import json, os, sys
HERE = os.path.join(os.getcwd(), 'lab', 'evolve'); sys.path.insert(0, HERE)
a = sys.argv[1:]; sys.argv = ['x']
import evolve as E
import importlib.util, hv, stopping
s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(s); s.loader.exec_module(CF)
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 87]
G = {}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, 87)):
    for i, r in hv.load(f, E).items(): G.setdefault(i, r['genome'])
for f in ('results/candidates-final-seed86.md', 'results/shortlist-seed86.md', 'results/final-set-seed86.md'):
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); G.setdefault(r['id'], r['genome'])
for k, g in E.HUMAN.items(): G[k] = g
out = {}
for i, g in sorted(G.items()):
    c = E.canon(g)
    if c['enc'] != 'cv8': out[i] = [json.dumps(E.express(c), sort_keys=True), False]; continue
    hl = bool(E.rtloop_on(c) and not E.rtloopall_on(c) and E.express(c).get('rtloop') == 2)
    out[i] = [json.dumps(E.express(c), sort_keys=True), hl]
json.dump(out, open(a[0], 'w'))
print('%d designs; rtloop expressed in %d; headerless loop words in %d' % (len(out),
      sum(1 for v in out.values() if '"rtloop": ' in v[0] and '"rtloop": 0' not in v[0]), sum(1 for v in out.values() if v[1])))
if len(a) > 1:
    B = json.load(open(a[1]))
    diff = [i for i in B if i in out and B[i][0] != out[i][0]]
    hlb = [i for i in B if B[i][1]]
    print('against %s: %d designs in both; expression changed in %d%s; headerless loop words before in %d%s' % (
        a[1], len(set(B) & set(out)), len(diff), (' - ' + ' '.join(diff[:12])) if diff else '',
        len(hlb), (' - ' + ' '.join(hlb[:12])) if hlb else ''))
    sys.exit(1 if [i for i in diff if i not in hlb] else 0)
