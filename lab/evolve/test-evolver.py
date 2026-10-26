#!/usr/bin/env python3
"""test-evolver.py - the evolver's own functions held to what their comments promise (Iteration 530).

The bug hunt of 524-527 found the front shortcut (first_front, behind every report, the gate, the re-measure, the
appbench sample) far from the dominance it claimed - for many runs, and nothing noticed. These checks would have:
  first_front   equal to fronts()[0] on generated populations, with and without the 32-bit speed (TWO_WIDTHS)
  stop_beaten   one round first (529): beaten by STOP1 in speed by a no larger design within MEM_TOL - and not otherwise
  aos_update    adaptive operators (526): the class shares follow the yields, the floor holds, too few children - no change
  gate_again    a gated design's second reading (446, 527): joined by the geometric mean; a failed second run kills
Pure functions - nothing built or run. tools/run-tests.sh runs it; exit 1 on any failure.
"""
import math, os, random, sys
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
fails, n = [], [0]
def check(name, ok, why=''):
    n[0] += 1
    if not ok: fails.append(name + (' - ' + why if why else ''))
def rec(i, s, tot, m, s32=None, **k):
    r = dict({'id': i, 'status': 'ok', 'speed': s, 'total': tot, 'size': tot, 'rss': m}, **k)
    if s32 is not None: r['speed32'] = s32
    return r
tw0 = E.TWO_WIDTHS[0]
try:
    # first_front against fronts()[0]
    for tw in (False, True):
        E.TWO_WIDTHS[0] = tw
        R = {'A': rec('A', 1.000, 1000, 100, 1.0), 'B': rec('B', 1.010, 1000, 100, 0.5 if tw else 1.0)}
        check('first_front, two designs 1%% apart (widths %s)' % tw, E.first_front(['A', 'B'], R) == E.fronts(['A', 'B'], R)[0],
              '%s against %s' % (E.first_front(['A', 'B'], R), E.fronts(['A', 'B'], R)[0]))
    rnd = random.Random(530); bad = 0
    for k in range(300):
        E.TWO_WIDTHS[0] = k % 2 == 1
        R = {str(q): rec(str(q), rnd.uniform(1, 1.3), rnd.choice([1000, 1010, 1020, 1100]), rnd.choice([100, 104, 108, 140]),
                         rnd.uniform(1, 1.3)) for q in range(25)}
        if E.first_front(list(R), R) != E.fronts(list(R), R)[0]: bad += 1
    check('first_front against fronts()[0] on 300 random populations of 25', bad == 0, '%d differ' % bad)
    E.TWO_WIDTHS[0] = tw0
    # one round first
    if hasattr(E, 'stop_beaten'):
        R = {'X': rec('X', 1.0, 1000, 100, gen=0)}
        st = E.stop_stair(R, 1); s1 = 1 + E.STOP1
        check('stop_beaten: beaten by more than STOP1, no larger, same memory', E.stop_beaten(st, s1 * 1.001, 1000, 100))
        check('stop_beaten: within STOP1', not E.stop_beaten(st, s1 * 0.99, 1000, 100))
        check('stop_beaten: the earlier design larger', not E.stop_beaten(st, s1 * 1.5, 999, 100))
        check('stop_beaten: the earlier design over the memory tolerance', not E.stop_beaten(st, s1 * 1.5, 1000, 100 - E.MEM_TOL - 1))
        check('stop_stair: only designs of earlier generations', E.stop_stair(R, 0) is None)
    else: check('stop_beaten exists (one round first, 529)', False)
    # adaptive operators
    if hasattr(E, 'aos_update'):
        E.OPS.update(xover=0.25, borrow=0.15)
        R = {}; rk = {}; q = 0
        for cls, made, hits in (('crossover', 100, 0), ('borrowed x from y', 100, 2), ('mutation', 100, 10)):
            for j in range(made):
                i = 'c%d' % q; q += 1
                R[i] = {'gen': 5, 'parents': ['p'], 'how': cls if cls != 'mutation' else 'mutation: tos 0 -> 1'}
                rk[i] = 0 if j < hits else 1
        y = E.aos_update(R, rk, 6)
        check('aos_update: crossover gets the least', y and E.OPS['xover'] < 0.25 and E.OPS['xover'] >= E.AOS_FLOOR,
              'xover %.3f' % E.OPS['xover'])
        sh_b = E.OPS['borrow'] * (1 - E.OPS['xover']); sh_m = 1 - E.OPS['xover'] - sh_b
        check('aos_update: mutation the most, borrowing between', sh_m > sh_b > E.OPS['xover'] - 1e-9, 'shares %.3f %.3f %.3f' % (E.OPS['xover'], sh_b, sh_m))
        E.OPS.update(xover=0.25, borrow=0.15)
        check('aos_update: under 50 children nothing changes', E.aos_update({k: R[k] for k in list(R)[:40]}, rk, 6) is None and E.OPS['xover'] == 0.25)
        check('aos_update: other generations do not count', E.aos_update(R, rk, 20) is None)
    else: check('aos_update exists (adaptive operators, 526)', False)
    # the gated design's second reading
    if hasattr(E, 'gate_again'):
        ws = E.WORK_SEL
        r = rec('G', 0.5, 1000, 100, t={w: 0.5 for w in ws}, raw={w: 1.0 for w in ws}, gated=1)
        E.gate_again(r, {'status': 'ok', 'speed': 0.8, 't': {w: 0.8 for w in ws}, 'raw': {w: 2.0 for w in ws}})
        check('gate_again: the geometric mean of the two', abs(r['speed'] - math.sqrt(0.5 * 0.8)) < 1e-12 and r['gated'] == 2 and r['status'] == 'ok')
        r = rec('H', 0.5, 1000, 100, t={w: 0.5 for w in ws}, gated=1)
        E.gate_again(r, {'status': 'wrong output: apps'})
        check('gate_again: a failed second run kills', r['status'] == 'wrong output: apps' and r['gated'] == 2, r['status'])
    else: check('gate_again exists (the gated second reading, 527/530)', False)
finally:
    E.TWO_WIDTHS[0] = tw0
for f in fails: print('FAIL', f)
print('test-evolver: %d checks, %s' % (n[0], 'all pass' if not fails else '%d FAIL' % len(fails)))
sys.exit(1 if fails else 0)
