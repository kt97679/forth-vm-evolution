#!/usr/bin/env python3
"""lab/evolve/design-sizes.py OUT.json [OLD.json] - s6 and the ten designs of designs/ built as the search builds them
(evolve.build() from each record's genome: the translator's image), at both widths: the engine's bytes, the image's,
the four applications' code (app_size(), the size score's since 678) and the total. With OLD, a table of the change.
For a kernel or converter change measured before and after on every design and s6 (the plan's step 1, Iteration 681)."""
import json, os, sys, tempfile, shutil
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
OUT, OLD = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
sys.argv = sys.argv[:1]
import importlib.util
spec = importlib.util.spec_from_file_location('evolve', os.path.join(HERE_, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
import re
DESIGNS = re.findall(r"'([\w-]+)'", re.search(r'DESIGNS = \[([^\]]*)\]', open(os.path.join(HERE_, 'genapps.py')).read()).group(1))
E.TWO_WIDTHS[0] = True; E.setup_widths()
tmp = tempfile.mkdtemp(prefix='design-sizes-'); R = {}
try:
    for d in ['s6'] + DESIGNS:
        g = E.canon(E.HUMAN['s6-cv8b']) if d == 's6' else E.canon(json.load(open(os.path.join(ROOT, 'designs', d, 'record.json')))['genome'])
        dd = os.path.join(tmp, d); eng, img = E.build(g, dd); pw = E.private_work(dd); E.alive(eng, img, pw, far=d != 's6')
        a8 = E.app_size(eng, img, pw); r = {'8': dict(bin=E.bin_size(eng), image=os.path.getsize(img), app=sum(a8))}
        g32 = dict(g)
        if (g32.get('scale') or 0) > 2: g32['scale'] = 2
        g32 = E.canon(g32); dd = os.path.join(tmp, d + '-32')
        with E.at_width(E.WIDTH4):
            eng, img = E.build(g32, dd); pw = E.private_work(dd); E.alive(eng, img, pw, far=d != 's6')
            a4 = E.app_size(eng, img, pw); r['4'] = dict(bin=E.bin_size(eng), image=os.path.getsize(img), app=sum(a4))
        for w in ('8', '4'): r[w]['total'] = r[w]['bin'] + r[w]['image'] + r[w]['app']
        R[d] = r; print('design-sizes: %-16s 8: %s   4: %s' % (d, r['8'], r['4']), flush=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
json.dump(R, open(OUT, 'w'), indent=1)
if OLD:
    O = json.load(open(OLD))
    print('| design | engine 8 | image 8 | app 8 | total 8 | engine 4 | image 4 | app 4 | total 4 |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for d in R:
        print('| %s | %s |' % (d, ' | '.join('%+d' % (R[d][w][k] - O[d][w][k]) for w in ('8', '4') for k in ('bin', 'image', 'app', 'total'))))
print('design-sizes: wrote %s' % OUT)
