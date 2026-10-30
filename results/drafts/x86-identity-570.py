#!/usr/bin/env python3
"""results/drafts/x86-identity-570.py ROOT - the after-seed-83 batch changes nothing on x86 (Iteration 570): s6 and a spread
of seed 82's front - per (enc, JIT, clang) class its two fastest and its slowest - built by ROOT's evolve.py at 8- and
4-byte cells, a line each with the sha1s of engine and image. Run it in master and in the batch's scratch tree and diff
the two outputs: Iteration 570, 28 builds, identical."""
import hashlib, json, os, sys
ROOT = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
recs = [json.loads(l) for l in open(os.path.join(ROOT, 'results', 'evolve-amd-ryzen-7-pro-8840hs-seed82.md')) if l.startswith('{"bin"')]
recs.sort(key=lambda r: r.get('speed') or 9)
cat = {}
for r in recs:
    e = E.express(E.canon(r['genome'])); k = (r['genome'].get('enc'), bool(e.get('jit')), bool(e.get('compiler')))
    cat.setdefault(k, []).append(r)
pick = [('s6', E.HUMAN['s6-cv8b'])] + [(r['id'], r['genome']) for k in sorted(cat, key=str) for r in (cat[k][:2] + cat[k][-1:])]
E.setup(); E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
h = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
for wname, ctx in (('8', None), ('4', E.WIDTH4)):
    for i, g in pick:
        d = os.path.join(E.EV, 'ident-%s-%s' % (wname, i))
        try:
            if ctx:
                with E.at_width(ctx): eng, img = E.build(E.canon(g), d)
            else: eng, img = E.build(E.canon(g), d)
            print(wname, i, h(eng), h(img), os.path.getsize(eng), flush=True)
        except Exception as ex: print(wname, i, 'FAILED', str(ex)[:60], flush=True)
print('categories', {str(k): len(v) for k, v in cat.items()})
