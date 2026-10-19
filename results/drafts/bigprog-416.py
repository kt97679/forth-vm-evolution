# Iteration 416: big1.fth and big2.fth (gen.py) run on s6, seed 58's smallest (plain CV8), seed 60's fastest interpreted
# and fastest (tag 2, the JIT) - at 8-byte cells, and s6 at 4.
import contextlib, json, os, shutil, sys
tree = sys.argv[1]; os.chdir(tree); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
def rec(f, i): return next(json.loads(l)['genome'] for l in open(f) if l.startswith('{"') and '"%s"' % i in l)
R = 'results/evolve-amd-ryzen-7-pro-8840hs-seed%d.md'
cases = [('s6 (hand-made, plain CV8)', dict(E.HUMAN['s6-cv8b']), 8), ('58 09de03f091 (plain CV8)', rec(R % 58, '09de03f091'), 8),
         ('60 4ac602c8bd (tag 2)', rec(R % 60, '4ac602c8bd'), 8), ('60 5ee5c38165 (tag 2, JIT)', rec(R % 60, '5ee5c38165'), 8),
         ('s6 at 4-byte cells', dict(E.HUMAN['s6-cv8b']), 4)]
for name, g, w in cases:
    if w == 4: g = dict(g, jit=0)
    g = E.canon(g); d = os.path.join(E.EV, 'bp'); shutil.rmtree(d, ignore_errors=True); out = []
    try:
        with (E.at_width(E.WIDTH4) if w == 4 else contextlib.nullcontext()):
            eng, img = E.build(g, d); pw = E.private_work(d)
            for p in ('big1', 'big2'):
                r = E.sh([eng, img], cwd=pw, inp=open('/tmp/bp/%s.fth' % p, 'rb').read(), timeout=120, cpu=60)
                o = (r.stdout or b'').decode(errors='replace').replace('\r', '').strip().splitlines()
                sel = [x for x in o if any(c.isdigit() for c in x) or 'reach' in x or 'Undefined' in x][-2:]
                out.append('%s: %s' % (p, (' / '.join(sel) or (o[-1] if o else '(nothing)'))[:90]))
    except Exception as x: out.append('build: ' + str(x)[:100])
    print('%-28s tag2=%s | %s' % (name, g.get('tag2'), ' | '.join(out)), flush=True)
shutil.rmtree(os.path.join(E.EV, 'bp'), ignore_errors=True)
