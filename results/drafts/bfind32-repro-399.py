# Iteration 399 (results/bfind32-fault-399.md): python3 THIS TREE TAG, as the user that builds, in a tree whose stages
# are built. Run on master's engine (before) and with bf_walk's three declarations uint64_t (after); the 4-byte
# check of the variants alone (before2) was this with the seed-59 ids removed and 'tos': 0 in each variant.
# Open item 0f: seed 59's designs (and the bfind variants on s6) built as eval32 builds them - a 32-bit x86
# engine at 4-byte cells, the JIT off - alive or not; on a corpus death, the first line that differs.
import json, os, shutil, sys
tree, tag = sys.argv[1], sys.argv[2]; os.chdir(tree)
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve'))
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
recs = {}
for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed59.md'):
    if l.startswith('{"bin"'):
        r = json.loads(l); recs[r['id']] = r['genome']
S6 = dict(E.HUMAN['s6-cv8b'])
cases = [('seed59 ' + i, recs[i]) for i in ('708757c03f', '686ae7cd5f', '505aec3d29')]
cases += [(n, dict(S6, **gs)) for n, gs in [
    ('bfind: THREAD-FIND, CV8', {'kfast': 1, 'tfind': 1, 'bfind': 1}),
    ('bfind: (FIND), CV8', {'kfast': 1, 'kinput': 1, 'klookup': 1, 'bfind': 1}),
    ('bfind: THREAD-FIND, TAG2', {'tag2': 1, 'kfast': 1, 'tfind': 1, 'bfind': 1}),
    ('bfind: (FIND), TAG2', {'tag2': 1, 'kfast': 1, 'kinput': 1, 'klookup': 1, 'bfind': 1})]]
for name, g in cases:
    g32 = dict(g, jit=0)
    if (g32.get('scale') or 0) > 2: g32['scale'] = 2
    g32 = E.canon(g32); ex = E.express(g32)
    d = os.path.join(E.EV, 'f0f'); shutil.rmtree(d, ignore_errors=True)
    try:
        with E.at_width(E.WIDTH4):
            eng, img = E.build(g32, d); pw = E.private_work(d)
            try:
                E.alive(eng, img, pw, far=not E.hand_made(g32)); res = 'ALIVE'
            except RuntimeError as e:
                res = 'DIED ' + str(e)
                if 'corpus' in str(e):
                    r = E.sh([eng, img], cwd=pw, inp=open(E.CORPUS, 'rb').read(), timeout=120, cpu=5)
                    a = r.stdout.split(b'\n'); b = E.REF_CORPUS.split(b'\n')
                    k = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
                    res += ' | line %d of %d: got %r want %r' % (k, len(b), a[k][:100] if k < len(a) else b'<end>', b[k][:100] if k < len(b) else b'<end>')
    except Exception as e:
        res = 'BUILD-FAIL ' + str(e)[:150]
    print('%s %-24s bfind=%s tos=%s: %s' % (tag, name, ex.get('bfind'), g32.get('tos'), res), flush=True)
shutil.rmtree(os.path.join(E.EV, 'f0f'), ignore_errors=True)
