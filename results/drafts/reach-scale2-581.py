#!/usr/bin/env python3
"""results/drafts/reach-scale2-581.py DB.jsonl - why only threads=2 reaches the scale-2 limit (Iteration 581;
results/drafts/reach-scale2-581.md): seed 85's first kernel deaths at scale 2, rebuilt with threads 0-3, then at threads 2
with both far forms, at scale 3 and at scale 1 - the kernel workload's image against the reference, and each image's size."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
E.setup()
D = []
for l in open(db):
    try: r = json.loads(l)
    except ValueError: continue
    if r.get('status') == 'died: kernel workload' and (r.get('genome') or {}).get('scale') == 2: D.append(r)
print(len(D), 'scale-2 kernel deaths')
def kernel(r, **ch):
    d = os.path.join(E.EV, 'reach2-%s-%s' % (r['id'], '-'.join('%s%s' % kv for kv in sorted(ch.items()))))
    eng, img = E.build(E.canon(dict(r['genome'], **ch)), d); pw = E.private_work(d); k = os.path.join(pw, 'kernel.img')
    if os.path.exists(k): os.remove(k)
    E.sh([eng, img], cwd=pw, inp=E.KERNEL_IN, timeout=240, cpu=10)
    ok = os.path.exists(k) and open(k, 'rb').read() == open(E.KREF, 'rb').read()
    print(r['id'], ch, 'image %d bytes' % os.path.getsize(img), 'kernel right' if ok else 'kernel WRONG', flush=True)
for r in D[:3]:
    for t in (0, 1, 2, 3): kernel(r, threads=t)
for r in D[:2]:
    for ch in (dict(varcall=1, doesfar=1), dict(scale=3), dict(scale=1)): kernel(r, threads=2, **ch)
