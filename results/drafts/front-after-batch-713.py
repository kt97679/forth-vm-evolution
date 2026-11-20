#!/usr/bin/env python3
"""results/drafts/front-after-batch-713.py LIST_BEFORE SIZES POOLSIZES... - did the after-seed-96 batch's uneven savings
(482-2,224 bytes an engine, by compiler and genes) move a design off chain A's list onto the JIT-free front? (Iteration
713; the owner: "ensure we are not losing good designs"; the knee's 1 % rule the open case.) LIST_BEFORE: chain A's list
with its in-run records (`git show 3a04c66:results/followup-seed96-roles.md`); SIZES: results/drafts/sizes-713.json
(chain A's designs at master); POOLSIZES: sizes-713.py's JSON over pool designs off the list, their records read from
the seeds 92-96 results files. The front: no other design as fast or faster at both widths (in-run - the screen's own
measure), as small or smaller (master's total) and as lean or leaner, one better; over the designs with a size at master
up to MAX (env, 27,400 B: the knee holder's 27,334 and a little - every list design up to there has one). Prints the pool
designs on it and, for each, the list's nearest by size."""
import glob, json, os, sys
lb, szf, pools = sys.argv[1], sys.argv[2], sys.argv[3:]
MAX = int(os.environ.get('MAX', '27400'))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
L = {r['id']: r for r in (json.loads(l) for l in open(lb) if l.startswith('{"'))}
SZ = json.load(open(szf)); PS = {}
for p in pools: PS.update(json.load(open(p)))
R = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'evolve-amd-ryzen-7-pro-8840hs-seed9[2-6].md'))):
    for l in open(f):
        if l.startswith('{"') and '"genome"' in l:
            r = json.loads(l)
            if r['id'] in PS and r['id'] not in R: R[r['id']] = r
D = {}
for i, r in L.items():
    if i in SZ and 'total' in SZ[i] and not SZ[i].get('jit') and SZ[i]['total'] <= MAX: D[i] = (r, SZ[i]['total'], 'list')
for i, r in R.items():
    if 'total' in PS[i] and not PS[i].get('jit') and PS[i]['total'] <= MAX and i not in D: D[i] = (r, PS[i]['total'], 'pool')
BEF = {i: (L[i]['total'] if D[i][2] == 'list' else R[i]['total']) for i in D}
def front(tot):
    key = lambda i: (D[i][0]['speed'], D[i][0]['speed32'], tot(i), D[i][0]['rss'])
    K = {i: key(i) for i in D}
    return {i for i in D if not any(all(p <= q for p, q in zip(K[j], K[i])) and K[j] != K[i] for j in D if j != i)}
after, before = front(lambda i: D[i][1]), front(lambda i: BEF[i])
moved = sorted(after - before, key=lambda i: D[i][1]); left = before - after
print('front-after-batch: %d designs up to %d B at master (%d of chain A\'s list, %d off it); the front %d after the batch, '
      '%d before; %d on it only after (%d off chain A\'s list), %d only before' % (len(D), MAX,
      sum(v[2] == 'list' for v in D.values()), sum(v[2] == 'pool' for v in D.values()), len(after), len(before), len(moved),
      sum(D[i][2] == 'pool' for i in moved), len(left)))
for i in moved[:int(os.environ.get('SHOW', '12'))]:
    r, t, w = D[i]
    print('  %s %-4s %6d B (%d before)  in-run %.4f / %.4f  %3d KB' % (i, w, t, BEF[i], r['speed'], r['speed32'], r['rss']))
