#!/usr/bin/env python3
"""lab/evolve/gene-narrow.py DB ID WORKLOAD GENE=VALUE... - which genes a design's wrong output needs (Iteration 564: seed
78's cv8 kernel deaths, six lifted values together). The design ID of DB, built here and run on WORKLOAD against s6, as
it is; with each GENE set to its VALUE (a suspect value put back to a known one), one at a time - a gene whose putting
back makes it right is necessary; then all of them put back (it should compute right), and each suspect value alone
returned - one that alone makes it wrong is sufficient. As the build user, in a built tree; a build a line.
"""
import json, os, shutil, sys
a = sys.argv[1:]
if len(a) < 4: sys.exit(__doc__)
db, ID, W, sets = a[0], a[1], a[2], dict(x.split('=', 1) for x in a[3:])
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
r = next(json.loads(l) for l in open(db) if l.startswith('{') and '"%s"' % ID in l and json.loads(l).get('id') == ID)
g0 = dict(r['genome']); val = lambda v: int(v) if v.lstrip('-').isdigit() else v
known = {k: val(v) for k, v in sets.items()}; suspect = {k: g0.get(k) for k in known}
E.setup(); E.run_metric(*E.REF, W); ref = E.OUT_LAST[0]
def run(g, what):
    d = os.path.join(E.EV, 'gene-narrow'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(g), d); E.run_metric(eng, img, E.private_work(d), W)
        ok = E.OUT_LAST[0] == ref; out = 'right' if ok else 'WRONG'
    except Exception as x:
        ok, out = False, 'DIES: %s' % str(x)[:70]
    shutil.rmtree(d, ignore_errors=True); print('| %s | %s |' % (what, out), flush=True); return ok
print('%s (%s) on %s - the suspects: %s\n\n| the genome | here |\n|---|---|' % (ID, r.get('status'), W, ', '.join('%s=%s' % kv for kv in suspect.items())))
base = run(g0, 'as it is')
nec = [k for k in known if run(dict(g0, **{k: known[k]}), '%s put back to %s' % (k, known[k]))]
allb = dict(g0, **known); clean = run(allb, 'all %d put back' % len(known))
suf = [k for k in known if not run(dict(allb, **{k: suspect[k]}), 'all put back but %s=%s' % (k, suspect[k]))] if clean else []
print('\ngene-narrow: as it is %s; necessary (put back, it is right): %s; all put back %s; sufficient alone: %s'
      % ('wrong' if not base else 'RIGHT - nothing to narrow', ', '.join(nec) or 'none alone', 'right' if clean else 'STILL WRONG - another cause', ', '.join(suf) or 'none alone'))
