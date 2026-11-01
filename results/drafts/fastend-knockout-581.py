#!/usr/bin/env python3
"""results/drafts/fastend-knockout-581.py GENE ID... - one gene switched in seed 84's fast designs, counted (Iteration 581):
for each ID (its genome from the results files), the design with GENE at 1 and at 0, user-space instructions on corpus,
apps and kernel against s6's (results/drafts/fastend-icount-579.s6.json; valgrind cachegrind as fastend-icount-579.py).
Iteration 581 ran it for jitimg (4df5b46d00 332d4a8da1 8ef0975d7c d701cad70b) and guard (4df5b46d00 332d4a8da1
b27ca531b3) - results/drafts/fastend-icount-579.md."""
import glob, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
gene, ids = sys.argv[1], sys.argv[2:]
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
E.setup()
gen = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md'))) + sorted(glob.glob(os.path.join(ROOT, 'results', 'candidates-*.md'))):
    for l in open(f, errors='replace'):
        if l.startswith('{"'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id') and 'genome' in r: gen.setdefault(r['id'], r['genome'])
s6 = json.load(open(os.path.join(ROOT, 'results', 'drafts', 'fastend-icount-579.s6.json')))
def ic(eng, img, pw, w):
    r = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', '--smc-check=all', eng, img],
                       input=E.program(w), cwd=pw, capture_output=True, timeout=1800)
    return int(re.search(rb'I\s+refs:\s+([\d,]+)', r.stderr).group(1).replace(b',', b''))
for i in ids:
    for v in (1, 0):
        d = os.path.join(E.EV, 'knockout-%s-%s-%d' % (gene, i, v))
        eng, img = E.build(E.canon(dict(gen[i], **{gene: v})), d); pw = E.private_work(d)
        print(i, gene, v, ' '.join('%s %.4f' % (w, ic(eng, img, pw, w) / s6[w]) for w in ('corpus', 'apps', 'kernel')), flush=True)
