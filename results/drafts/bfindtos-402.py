# Iteration 402 (results/bfind32-fault-399.md): python3 THIS TREE, its stages built with the patch.
# Iteration 402: bfind on a TOS design (s6) built at 8- and 4-byte cells - alive, and its engine not the same without bfind.
import contextlib, os, shutil, sys
tree = sys.argv[1]; os.chdir(tree); sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
S6 = dict(E.HUMAN['s6-cv8b'])
for name, genes in [('THREAD-FIND, CV8', {'kfast': 1, 'tfind': 1}), ('(FIND), TAG2', {'tag2': 1, 'kfast': 1, 'kinput': 1, 'klookup': 1})]:
    for width in (8, 4):
        out = {}
        try:
            for tag, bf in (('b1', 1), ('b0', 0), ('b0again', 0)):
                g = dict(S6, **genes); g['bfind'] = bf
                if width == 4: g['jit'] = 0
                g = E.canon(g); d = os.path.join(E.EV, 'bft-' + tag); shutil.rmtree(d, ignore_errors=True)
                with (E.at_width(E.WIDTH4) if width == 4 else contextlib.nullcontext()):
                    eng, img = E.build(g, d)
                    if bf: E.alive(eng, img, E.private_work(d))
                out[tag] = open(eng, 'rb').read(); tos = g.get('tos'); ex = E.express(g).get('bfind') if bf else None
                if tag == 'b1': exb = ex
            res = 'alive; engine differs without bfind: %s; bfind 0 built twice identical: %s' % (out['b1'] != out['b0'], out['b0'] == out['b0again'])
        except Exception as e: res = 'FAILED: ' + str(e)[:200]
        print('%-18s %d-byte cells, tos=%s, bfind expressed=%s: %s' % (name, width, tos, exb if out else '?', res), flush=True)
for t in ('b1', 'b0', 'b0again'): shutil.rmtree(os.path.join(E.EV, 'bft-' + t), ignore_errors=True)
