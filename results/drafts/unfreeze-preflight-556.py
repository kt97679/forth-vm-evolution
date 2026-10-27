# results/drafts/unfreeze-preflight-556.py - every lifted freeze checked before seed 77 (Iteration 556): run as the build user
# in a built tree with the freezes lifted (EVOLVE_CELL=4 EVOLVE_CC="gcc -m32 -fno-pie -no-pie" for 32 bits); reads seed 76's pack db.
import json, glob, os, random, shutil, sys, time
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E, hv
E.setup()
db = glob.glob('/tmp/process/forth-vm-evolution-seed76-*/pack/db.jsonl')[0]; R = {}
for l in open(db, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'):
            r['total'] = E.ov(r, 'total') if r.get('status') == 'ok' and (r.get('total') or r.get('size')) else r.get('total'); R[r['id']] = r
front = [R[i] for i in hv.true_front(R, E)]
J = lambda r: E.jit_on(E.canon(r['genome']))
jit = sorted([r for r in front if J(r)], key=lambda r: r['total']); nojit = sorted([r for r in front if not J(r)], key=lambda r: r['total'])
bases = [('the fastest', min(front, key=lambda r: r['speed'])), ('the smallest', min(front, key=lambda r: r['total'])),
         ('a JIT design, mid', jit[len(jit) // 2]), ('a non-JIT design, mid', nojit[len(nojit) // 2])]
GENES = ['alignhot', 'msc', 'scale', 'sharedcall', 'bytehdr', 'doesfar', 'thinhdr', 'varcall', 'bss', 'lean']
W = list(E.WORK_SEL) + [w for w in ('sieve', 'parse') if w not in E.WORK_SEL]
S6 = {}
for w in W: E.run_metric(*E.REF, w); S6[w] = E.OUT_LAST[0]
def check(g):
    d = os.path.join(E.EV, 'preflight'); shutil.rmtree(d, ignore_errors=True)
    try: eng, img = E.build(g, d)
    except Exception as x: return 'BUILD FAILED: %s' % str(x)[:70]
    pw = E.private_work(d); bad = []
    for w in W:
        try:
            E.run_metric(eng, img, pw, w)
            if E.OUT_LAST[0] != S6[w]: bad.append(w + ' WRONG')
        except Exception as x: bad.append(w + ' DIED')
    shutil.rmtree(d, ignore_errors=True)
    return 'right on all %d' % len(W) if not bad else ', '.join(bad)
print('cell %s; workloads: %s' % (os.environ.get('EVOLVE_CELL', '8'), ' '.join(W)), flush=True)
for bn, b in bases:
    print('## %s: %s (speed %.3f, %d bytes, JIT %s)' % (bn, b['id'], b['speed'], b['total'], J(b)), flush=True)
    for k in GENES:
        vals = E.GENE_VALUES[k][0] if k in E.GENE_VALUES and len(E.GENE_VALUES[k][0]) > 2 else [0, 1]
        for v in vals:
            if v == b['genome'].get(k): continue
            g = E.canon(dict(b['genome'], **{k: v}))
            if g.get(k) != v: print('  %s=%s: not kept by canon (%s=%s here)' % (k, v, k, g.get(k)), flush=True); continue
            t0 = time.time(); print('  %s=%s: %s (%.0fs)' % (k, v, check(g), time.time() - t0), flush=True)
print('## eight random designs from the unfrozen space', flush=True)
rnd = random.Random(556)
for n in range(8):
    g = E.random_genome(rnd); on = [k for k in GENES if g.get(k) != {'bytehdr': 1, 'doesfar': 1, 'thinhdr': 1, 'varcall': 1, 'bss': 1, 'lean': 1}.get(k, 0)]
    print('  random %d (%s; JIT %s; unfrozen values: %s): %s' % (n, g.get('enc'), E.jit_on(g), ' '.join('%s=%s' % (k, g.get(k)) for k in on) or 'none', check(g)), flush=True)
print('preflight done', flush=True)
