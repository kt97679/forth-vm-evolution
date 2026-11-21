#!/usr/bin/env python3
"""results/drafts/guardsize-714.py LIST ID ... - the gene abortif's cost in the translator-built image (Iteration 714):
each ID's record from LIST built twice by evolve.build at 8-byte cells, abortif as it is (1) and 0, the images' bytes
compared - against the self-built image's, A with G-GUARD-ABORT -1 and 0 (results/selfhost-fusions-714.md), which the
cross compiler's guard must match site for site."""
import json, os, shutil, sys, tempfile
lst, ids = sys.argv[1], sys.argv[2:]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
E.setup()
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
for i in ids:
    out = []
    for ab in (1, 0):
        g = dict(C[i]['genome'], abortif=ab); d = tempfile.mkdtemp(prefix='gs-')
        eng, img = E.build(E.canon(g), d); out.append(os.path.getsize(img)); shutil.rmtree(d, ignore_errors=True)
    print('guardsize: %s - the translator\'s image %d B with abortif, %d without: the guards %+d B' % (i, out[0], out[1], out[0] - out[1]))
