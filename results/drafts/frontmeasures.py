import re, math, random, collections
def rows(path):
    L = open(path).read().split('\n')
    hi = next(i for i, l in enumerate(L) if l.startswith('| run |'))
    hdr = [x.strip() for x in L[hi].split('|')]
    cs, cb, cm = hdr.index('speed now'), hdr.index('binary + image'), hdr.index('memory KB')
    out = collections.defaultdict(list)
    for l in L[hi + 2:]:
        c = [x.strip() for x in l.split('|')]
        if len(c) <= cm or not re.fullmatch(r'\w{10}', c[2] or ''): continue
        try: out[c[1]].append((float(c[cs]), int(c[cb].replace(',', '')), float(c[cm])))
        except ValueError: pass
    return out
def nd(pts):
    return [p for p in pts if not any(all(q[k] <= p[k] for k in range(3)) and q != p for q in pts)]
def hv(pts, ref, lo, n=150000, seed=1):
    rnd = random.Random(seed); P = [tuple(math.log(x) for x in p) for p in nd(pts)]; hit = 0
    for _ in range(n):
        s = tuple(lo[k] + rnd.random() * (ref[k] - lo[k]) for k in range(3))
        if any(all(p[k] <= s[k] for k in range(3)) for p in P): hit += 1
    return hit / n
for sess, path, me in (('34', '/tmp/s39/cmp/pack/compare-fronts.md', 'seed 39'), ('35', '/tmp/s40/cmp/pack/compare-fronts.md', 'seed 40')):
    R = rows(path); allp = [p for v in R.values() for p in v]
    lp = [tuple(math.log(x) for x in p) for p in allp]
    lo = tuple(min(p[k] for p in lp) for k in range(3)); ref = tuple(max(p[k] for p in lp) + 0.05 for k in range(3))
    mine = [k for k in R if k.startswith('this clone')][0]; others = [p for k, v in R.items() if k != mine for p in v]
    h0, h1 = hv(others, ref, lo), hv(others + R[mine], ref, lo)
    q = lambda p: p[0] * p[1] * p[2]
    q0, q1 = min(map(q, others)), min(map(q, R[mine]))
    f0, f1 = min(p[0] for p in others), min(p[0] for p in R[mine])
    s0, s1 = min(p[1] for p in others), min(p[1] for p in R[mine])
    print('session %s, %s against the rest: hypervolume %+.1f%%; best Q %+.1f%%; [the rule: fastest %+.1f%%, smallest %+.2f%%]'
          % (sess, me, 100 * (h1 / h0 - 1), 100 * (q0 / q1 - 1), 100 * (f0 / f1 - 1), 100 * (s0 / s1 - 1)))
