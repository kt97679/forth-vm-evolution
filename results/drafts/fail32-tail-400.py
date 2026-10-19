# Iteration 400 (results/fail32-400.md): seed 58's tail designs and engines-check's tail variants built at 4-byte cells as
# eval32 does, each failure with its tool's first error lines. python3 THIS TREE DB IDS.
import json, os, shutil, sys
tree, db, ids = sys.argv[1], sys.argv[2], sys.argv[3].split(','); os.chdir(tree)
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
G = {}
for l in open(db):
    if any(i in l for i in ids):
        r = json.loads(l)
        if r['id'] in ids: G['seed58 ' + r['id']] = r['genome']
S6 = dict(E.HUMAN['s6-cv8b'])
for name, genes in [('tail', dict(tail=1)), ('tail+lto', dict(tail=1, lto=1)), ('clang tail', dict(tail=1, compiler=1)),
                    ('clang tailpn', dict(tail=1, compiler=1, tailpn=1))]: G[name] = dict(S6, **genes)
E.TWO_WIDTHS[0] = True; E.setup_widths()
orig = E.sh
def sh(cmd, *a, **k):
    r = orig(cmd, *a, **k)
    if getattr(r, 'returncode', 0) and cmd and 'objdump' not in str(cmd[0]):
        err = r.stderr if isinstance(r.stderr, str) else (r.stderr or b'').decode('utf-8', 'replace')
        sh.last = [l for l in err.splitlines() if 'error' in l.lower()][:2]
    return r
sh.last = []; E.sh = sh
for name, g in G.items():
    g32 = dict(g, jit=0)
    if (g32.get('scale') or 0) > 2: g32['scale'] = 2
    g32 = E.canon(g32); ex = E.express(g32); d = os.path.join(E.EV, 'tv'); shutil.rmtree(d, ignore_errors=True); sh.last = []
    try:
        with E.at_width(E.WIDTH4):
            eng, img = E.build(g32, d); E.alive(eng, img, E.private_work(d), far=not E.hand_made(g32)); res = 'ALIVE'
    except Exception as e: res = 'FAILED: %s %s' % (str(e)[:150], ' | '.join(sh.last)[:400])
    print('%-20s tail=%s tailpn=%s compiler=%s: %s' % (name, ex.get('tail'), ex.get('tailpn'), ex.get('compiler'), res), flush=True)
shutil.rmtree(os.path.join(E.EV, 'tv'), ignore_errors=True)
