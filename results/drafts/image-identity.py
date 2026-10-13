#!/usr/bin/env python3
"""image-identity.py ROOT ID,ID,... - each design built in the tree at ROOT: its id, its
image's sha1 and size (JSON, the last line). Run it in two trees - master and a
scratch tree holding a converter change - and compare the two: a change whose gene
is off must leave every image and id byte for byte as it was (Iteration 267: 14 of
14 front designs of different kinds, for the gene factor). Kept in Iteration 272:
it produced a recorded figure, and lived in /tmp.
"""
import glob, hashlib, json, os, shutil, sys
ROOT, ids = sys.argv[1], sys.argv[2].split(',')
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
E.setup(); recs = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(f, errors='replace'):
        if l.startswith('{"bin"'): r = json.loads(l); recs[r['id']] = r
out = {}
for i in ids:
    g = E.canon(recs[i]['genome']); d = os.path.join(E.EV, 'ident-' + i); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); out[i] = [E.gid(g), hashlib.sha1(open(img, 'rb').read()).hexdigest()[:16], os.path.getsize(img)]
    shutil.rmtree(d, ignore_errors=True)
print(json.dumps(out))
