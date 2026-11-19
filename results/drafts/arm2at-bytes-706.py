#!/usr/bin/env python3
"""results/drafts/arm2at-bytes-706.py TREE LIST N OUT - the 2@/2! patch's x86 check (Iteration 706): N designs of LIST that
express 2@ (format 10) spread over tos 0/1, GCC/clang and the JIT, each built by TREE's evolve.py at the width of
EVOLVE_CELL (8 unless set; 4 with EVOLVE_CC='gcc -m32 -fno-pie -no-pie' as arm-cross-check.py builds the 32-bit x86
engines); OUT: a line a design - id, its genes that matter, the engine's and the image's sha256. Run once on master and
once on the patched tree, then diff the two OUTs: every line the same - the patch changes no x86 byte. As the build user."""
import hashlib, json, os, sys

tree, lst, n, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab', 'evolve'))
import evolve as E
recs = [json.loads(l) for l in open(lst) if l.startswith('{"')]
pick, seen = [], {}
for r in recs:
    x = E.express(E.canon(dict(r['genome'])))
    if '2@' not in (x.get('ops10') or []): continue
    k = (bool(x.get('tos')), x.get('compiler'), bool(x.get('jit')))
    if seen.get(k, 0) < max(1, n // 8): seen[k] = seen.get(k, 0) + 1; pick.append((r['id'], r['genome'], k))
sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:16]
with open(out, 'w') as o:
    for i, g, k in pick[:n]:
        d = os.path.join(E.EV, 'a2b-' + i)
        try:
            eng, img = E.build(E.canon(dict(g)), d)
            line = '%s tos=%d cc=%s jit=%d engine %s image %s' % (i, k[0], k[1], k[2], sha(eng), sha(img))
        except Exception as e:
            line = '%s tos=%d cc=%s jit=%d FAILED %s' % (i, k[0], k[1], k[2], str(e)[:60])
        o.write(line + '\n'); print(line, flush=True)
