#!/usr/bin/env python3
"""final-set.py DB|RESULTS.md [...] [--k 10] [--json OUT] | --self-test - the final set's selection (Iteration 571).

GOALS.md, "When the improvements are done", step 3: "the extremes, each re-measured, then designs added one at a time by
their contribution to the hypervolume in the same box, after merging designs within the tolerances, to five or ten; a
knee as a candidate, not an oracle". This is the selection, from the records alone - deterministic, as everything here
judged by counts; the re-measures (alone and under load, on the laptop, dream and the Tegra) come after it, of what it
names. The steps:

  1. The pool: every record of the files given - run databases (db.jsonl) or results files (their {"bin" lines) -
     pooled as the confirmation test pools the method's last runs; a design in several, the last file's record (the
     newest run's measure; the re-measure decides). Its true front: hv.true_front - evolve.dominates, its tolerances.
  2. Merged within the tolerances: designs of the same binary + image whose speeds (64 and 32 bits) lie within
     evolve's SPEED_TOL of each other and memory within MEM_TOL - one design to every measurement, the fastest kept.
     The size is exact (the owner: size savings are exact), so a smaller design is never merged into a larger: on the
     true front a design within the tolerances of a smaller one would be dominated by it.
  3. The four extremes - fastest, smallest, least memory, fastest at 32 bits - first, each over every alive design
     in the pool (the strict extremes, as the stopping rule takes them since Iteration 556: the tolerances can hide
     the fastest behind a smaller design within 2%); ties by the other objectives. With results files the pool is
     their fronts alone; with the runs' db.jsonl, every alive design.
  4. Then, one at a time, the design whose addition grows the set's hypervolume most (lab/evolve/hv.py, the fixed box
     hv-bounds.json; a design outside the box adds nothing), to K (default 10; the owner's five or ten - the table's
     cumulative share says where to cut). Ties by id. It stops early when nothing adds.
  5. A knee as a candidate: the design nearest the ideal corner of the box (every objective at its bound's low end,
     in hv.norm's coordinates) - marked in the set, or listed after it.

stdout: markdown - the pool, the front, the merges, the set (each design's objectives, what it adds, the cumulative
share of the front's hypervolume) and the knee. --json OUT: the set's records, one per line, for the re-measures.
--self-test: synthetic fronts with known answers.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hv


def merge(F, R, E):
    """The front's designs in groups within the tolerances (step 2); -> (representatives, {kept: [merged...]})."""
    tol = lambda a, b: max(a, b) <= min(a, b) * (1 + E.SPEED_TOL)
    groups = []
    for i in sorted(F, key=lambda i: (R[i]['total'], R[i]['speed'], R[i]['speed32'], R[i]['rss'], i)):
        r = R[i]
        for g in groups:
            q = R[g[0]]
            if q['total'] == r['total'] and tol(q['speed'], r['speed']) and tol(q['speed32'], r['speed32']) and abs(q['rss'] - r['rss']) <= E.MEM_TOL:
                g.append(i); break
        else: groups.append([i])
    return [g[0] for g in groups], {g[0]: g[1:] for g in groups if len(g) > 1}


def select(R, E, b, k=10):
    """Steps 1-5 on records R (by id): -> dict(front, kept, merged, set [(id, why, adds)], hv_front, knee)."""
    F = hv.true_front(R, E)
    M, merged = merge(F, R, E)
    A = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')]
    order = lambda key: sorted(A, key=lambda i: tuple(R[i][x] for x in key) + (i,))[0]
    S, why = [], {}
    for name, key in (('fastest', ('speed', 'speed32', 'total', 'rss')), ('smallest', ('total', 'speed', 'speed32', 'rss')),
                      ('least memory', ('rss', 'speed', 'speed32', 'total')), ('fastest at 32 bits', ('speed32', 'speed', 'total', 'rss'))):
        i = order(key)
        if i not in S: S.append(i); why[i] = name
        else: why[i] += ', ' + name
    M = M + [i for i in S if i not in M]                     # a strict extreme the tolerances kept off the front
    Z = {i: hv.norm(R[i], b) for i in M}
    hvf = hv.hv4([z for z in Z.values() if z is not None])
    hvs = lambda ids: hv.hv4([Z[i] for i in ids if Z[i] is not None])
    adds, cur = {}, 0.0
    for i in S: adds[i] = hvs(S[:S.index(i) + 1]) - cur; cur += adds[i]
    while len(S) < k:
        best = None
        for i in sorted(set(M) - set(S)):
            if Z[i] is None: continue
            g = hvs(S + [i]) - cur
            if best is None or g > best[1] + 1e-15: best = (i, g)
        if best is None or best[1] <= 0: break
        S.append(best[0]); why[best[0]] = 'adds the most'; adds[best[0]] = best[1]; cur += best[1]
    inside = [i for i in M if Z[i] is not None]
    knee = min(inside, key=lambda i: (math.sqrt(sum(c * c for c in Z[i])), i)) if inside else None
    return dict(front=len(F), kept=M, merged=merged, set=[(i, why[i], adds[i]) for i in S], hv_front=hvf, hv_set=cur, knee=knee, Z=Z)


def report(files, R, src, res, b, k):
    print('# The final set - %d design(s) of %d (lab/evolve/final-set.py, GOALS.md step 3)\n' % (len(res['set']), k))
    print('The pool: %d records from %s; its true front %d designs, %d after merging within the tolerances (%d merged), '
          '%d of them inside the box (with any strict extreme off it). Their hypervolume %.5f; the set\'s %.5f (%.1f%%).\n' % (
              len(R), ', '.join(os.path.basename(f) for f in files), res['front'], len(res['kept']),
              sum(len(v) for v in res['merged'].values()), sum(1 for i in res['kept'] if res['Z'][i] is not None),
              res['hv_front'], res['hv_set'], 100 * res['hv_set'] / res['hv_front'] if res['hv_front'] else 0))
    print('| # | design | why | speed | binary + image | memory KB | speed at 32 bits | adds | cumulative | from |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    c = 0.0
    for n, (i, w, a) in enumerate(res['set'], 1):
        c += a; r = R[i]
        print('| %d | %s | %s%s | %.4f | %s | %d | %.4f | %.5f | %.1f%% | %s |' % (
            n, i, w, ', the knee' if i == res['knee'] else '', r['speed'], format(r['total'], ','), r['rss'], r['speed32'], a,
            100 * c / res['hv_front'] if res['hv_front'] else 0, src[i]))
    kn = res['knee']
    if kn and kn not in [x[0] for x in res['set']]:
        r = R[kn]; print('\nThe knee, a candidate (nearest the box\'s ideal corner), not in the set: %s - speed %.4f, %s bytes, %d KB, '
                         '32-bit %.4f (%s).' % (kn, r['speed'], format(r['total'], ','), r['rss'], r['speed32'], src[kn]))
    if res['merged']:
        g = sorted(res['merged'].items(), key=lambda x: (-len(x[1]), x[0]))
        print('\nMerged within the tolerances, kept: merged - %s%s.' % ('; '.join('%s: %s' % (a, ', '.join(m)) for a, m in g[:8]),
              '; and %d more groups' % (len(g) - 8) if len(g) > 8 else ''))
    print('\nNext (GOALS.md step 3): the extremes and the set re-measured - alone and under load, on the laptop, dream and '
          'the Tegra; a knee is a candidate, not an oracle.')


def self_test(E, b):
    """Known answers on synthetic records: the extremes first, a dominated design never in, a tie merged, the greedy
    step taking the bigger gain, the order the same however the records come."""
    import random
    def rec(i, s, t, m, w): return dict(id=i, status='ok', speed=s, total=t, size=t, rss=m, speed32=w)
    base = [rec('fast', 0.15, 40000, 200, 0.16), rec('small', 1.5, 14000, 200, 1.5), rec('lean', 1.0, 30000, 80, 1.0),
            rec('fast32', 0.2, 38000, 200, 0.12),
            rec('mid', 0.4, 20000, 120, 0.4), rec('edge', 0.16, 39000, 199, 0.17),        # mid adds more than edge (by fast)
            rec('near', 0.45, 21000, 125, 0.45),                                           # dominated by mid
            rec('twin', 0.401, 20000, 121, 0.401),                                         # mid's twin: merged
            rec('worse', 0.5, 25000, 150, 0.5)]                                            # dominated by mid
    ok = True
    def check(c, what):
        nonlocal ok
        if not c: ok = False; print('final-set self-test: FAIL - %s' % what)
    R = {r['id']: r for r in base}; res = select(R, E, b, k=6); ids = [x[0] for x in res['set']]
    check(ids[:4] == ['fast', 'small', 'lean', 'fast32'], 'the extremes first: %s' % ids[:4])
    check(not {'worse', 'near'} & set(ids + res['kept']), 'the dominated designs out')
    check(res['merged'].get('mid') == ['twin'], 'the twin merged into mid: %s' % res['merged'])
    check(ids[4:] == ['mid', 'edge'], 'the bigger gain taken first: %s' % ids[4:])
    check(all(a >= 0 for _, _, a in res['set']) and res['hv_set'] <= res['hv_front'] + 1e-12, 'the gains non-negative, the set within the front')
    order = []
    for t in range(5):
        L = list(base); random.Random(t).shuffle(L); order.append([x[0] for x in select({r['id']: r for r in L}, E, b, k=6)['set']])
    check(all(o == order[0] for o in order), 'the same set whatever the order')
    print('final-set self-test: the extremes, a dominated design, a merge, the greedy step, the order - %s' % ('pass' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if not A: sys.exit(__doc__)
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS))
    if A[0] == '--self-test': sys.exit(self_test(E, b))
    k = 10; out = None
    if '--k' in A: j = A.index('--k'); k = int(A[j + 1]); del A[j:j + 2]
    if '--json' in A: j = A.index('--json'); out = A[j + 1]; del A[j:j + 2]
    R, src = {}, {}
    for f in A:
        for i, r in hv.load(f, E).items(): R[i] = r; src[i] = os.path.basename(f)
    res = select(R, E, b, k)
    report(A, R, src, res, b, k)
    if out:
        with open(out, 'w') as o:
            for i, w, a in res['set']: o.write(json.dumps(dict(R[i], why=w, adds=a), sort_keys=True) + '\n')
