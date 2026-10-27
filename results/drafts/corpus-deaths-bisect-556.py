# results/drafts/corpus-deaths-bisect-556.py - seed 76's two corpus deaths, one gene at a time (Iteration 556); as the build user
# in a built tree; reads seed 76's pack db.
import json, glob, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
db = glob.glob('/tmp/process/forth-vm-evolution-seed76-*/pack/db.jsonl')[0]; R = {}
for l in open(db, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id') in ('e80800407e', 'd11c9a6300', 'acf592137d'): R[r['id']] = r
E.run_metric(*E.REF, 'corpus'); s6 = E.OUT_LAST[0]
P, D, B = R['acf592137d']['genome'], R['d11c9a6300']['genome'], R['e80800407e']['genome']
V = [('acf592137d (the parent)', P), ('parent + factor=3', dict(P, factor=3)), ('parent + nocrossjump=1', dict(P, nocrossjump=1)),
     ('d11c9a6300 (both)', D), ('e80800407e', B), ('e80800407e, nocrossjump=0', dict(B, nocrossjump=0)),
     ('e80800407e, tracer=0', dict(B, tracer=0)), ('e80800407e, both 0', dict(B, nocrossjump=0, tracer=0))]
print('parent %s: factor %s nocrossjump %s tracer %s jit %s' % ('acf592137d', P.get('factor'), P.get('nocrossjump'), P.get('tracer'), P.get('jit')), flush=True)
for name, g in V:
    d = os.path.join(E.EV, 'bisect'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d); E.run_metric(eng, img, pw, 'corpus')
        print('%-28s %s' % (name, 'right' if E.OUT_LAST[0] == s6 else 'WRONG (%s)' % E.OUT_LAST[0][:8]), flush=True)
    except Exception as x: print('%-28s DIED: %s' % (name, str(x)[:80]), flush=True)
shutil.rmtree(os.path.join(E.EV, 'bisect'), ignore_errors=True); print('bisect done', flush=True)
