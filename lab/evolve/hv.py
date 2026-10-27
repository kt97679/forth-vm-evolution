#!/usr/bin/env python3
"""hv.py DB [DB ...] | --self-test - the fixed-reference hypervolume of a run's true front (Iteration 539).

The owner's stopping rule and confirmation test (GOALS.md, "When the improvements are done") judge a run by this number
(results/drafts/ask-front-stats-answers-538.md): the volume of objective space its true front dominates, inside a box
fixed in advance - lab/evolve/hv-bounds.json, written before seed 74, so nothing is fitted after the fact. Four
objectives, all minimised: speed and the 32-bit speed on a log scale (a relative change counts the same at any speed),
binary + image and memory linearly; each mapped to [0, 1] between its bounds, the reference point (1, 1, 1, 1). A design
outside the box adds nothing. The front: by dominates() itself (its tolerances), from the run's own records. Exact, by
slicing - four dimensions to three to an incrementally kept two-dimensional staircase: O(n^3), seconds for a front of a
few hundred. stdout: one line per database - the front's size, its hypervolume, its extremes.
"""
import bisect, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOUNDS = os.path.join(HERE, 'hv-bounds.json')


def hv2(stair):
    """The area a 2-D staircase (x ascending, y descending, all minimised) dominates inside [0, 1]^2."""
    a, px = 0.0, 1.0
    for x, y in reversed(stair):
        a += (px - x) * (1.0 - y); px = x
    return a


def hv3(pts):
    """The volume points in [0, 1]^3 dominate up to (1, 1, 1): swept along the third, a 2-D staircase kept."""
    pts = sorted(pts, key=lambda p: p[2]); stair = []; v = 0.0
    for j, (x, y, z) in enumerate(pts):
        k = bisect.bisect_right(stair, (x, float('inf')))
        if not (k > 0 and stair[k - 1][1] <= y):              # not dominated in the first two
            st = k - 1 if k > 0 and stair[k - 1][0] == x else k   # an equal first coordinate, a worse second: dominated
            m = k
            while m < len(stair) and stair[m][1] >= y: m += 1  # those it dominates go
            stair[st:m] = [(x, y)]
        nz = pts[j + 1][2] if j + 1 < len(pts) else 1.0
        if nz > z: v += (nz - z) * hv2(stair)
    return v


def hv4(pts):
    """The volume points in [0, 1]^4 dominate up to (1, 1, 1, 1)."""
    pts = sorted(pts, key=lambda p: p[3]); v = 0.0
    for k, p in enumerate(pts):
        nw = pts[k + 1][3] if k + 1 < len(pts) else 1.0
        if nw > p[3]: v += (nw - p[3]) * hv3([q[:3] for q in pts[:k + 1]])
    return v


def norm(rec, b):
    """A record's four objectives mapped into [0, 1] by the fixed bounds; None if outside the box."""
    def lg(f, lo, hi): return math.log(f / lo) / math.log(hi / lo)
    def ln(f, lo, hi): return (f - lo) / float(hi - lo)
    z = (lg(rec['speed'], *b['speed']), ln(rec['total'], *b['total']), ln(rec['rss'], *b['rss']), lg(rec['speed32'], *b['speed32']))
    return z if all(0.0 <= c <= 1.0 for c in z) else None


def true_front(R, E):
    ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss') and r.get('speed32')]
    E.TWO_WIDTHS[0] = True
    arch = []
    for i in sorted(ok, key=lambda i: (E.ov(R[i], 'total'), R[i]['speed'])):
        if any(E.dominates(R[a], R[i]) for a in arch): continue
        arch = [a for a in arch if not E.dominates(R[i], R[a])]; arch.append(i)
    by_t = sorted(ok, key=lambda i: E.ov(R[i], 'total')); tots = [E.ov(R[i], 'total') for i in by_t]
    return [b for b in arch if not any(a != b and E.dominates(R[a], R[b]) for a in by_t[:bisect.bisect_right(tots, E.ov(R[b], 'total'))])]


def self_test():
    import random
    rnd = random.Random(539); worst = 0.0
    for t in range(20):
        P = [tuple(rnd.random() * 0.9 for _ in range(4)) for _ in range(rnd.randint(1, 25))]
        exact = hv4(P)
        n = 40000; hit = 0
        for _ in range(n):
            s = tuple(rnd.random() for _ in range(4))
            if any(all(p[c] <= s[c] for c in range(4)) for p in P): hit += 1
        worst = max(worst, abs(exact - hit / float(n)))
    one = hv4([(0.5, 0.5, 0.5, 0.5)])
    ok = abs(one - 0.0625) < 1e-12 and worst < 0.01
    print('hv.py self-test: a single point %.4f (0.0625 expected); 20 random sets against 40,000 samples, worst gap %.4f - %s'
          % (one, worst, 'pass' if ok else 'FAIL'))
    return 0 if ok else 1



def measure(db, E, b=None):
    """A database's true front, measured (Iteration 554 - stopping.py's numbers too): its size, how many inside the box,
    the hypervolume and the four extremes."""
    b = b or json.load(open(BOUNDS)); R = {}
    for l in open(db, errors='replace'):
        if l.startswith('{'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id'):
                r['total'] = E.ov(r, 'total') if r.get('status') == 'ok' and (r.get('total') or r.get('size')) else r.get('total')
                R[r['id']] = r
    F = true_front(R, E)
    Z = [z for z in (norm(R[i], b) for i in F) if z is not None]
    ex = lambda k: min(R[i][k] for i in F)
    A = [r for r in R.values() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')]
    al = lambda k: min(r[k] for r in A)      # 556: the extremes over every alive design - the strict front's, no dominance chain
    return dict(front=len(F), inside=len(Z), hv=hv4(Z), fastest=ex('speed'), smallest=ex('total'), memory=ex('rss'), fastest32=ex('speed32'),
                alive=dict(fastest=al('speed'), smallest=al('total'), memory=al('rss'), fastest32=al('speed32')))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    if args[0] == '--self-test': sys.exit(self_test())
    b = json.load(open(BOUNDS))
    sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
    for db in args:
        m = measure(db, E, b)
        print('%s: true front %d (%d inside the box), hypervolume %.5f | fastest %.4f, smallest %d, least memory %d KB, fastest at 32 bits %.4f'
              % (db, m['front'], m['inside'], m['hv'], m['fastest'], m['smallest'], m['memory'], m['fastest32']), flush=True)
