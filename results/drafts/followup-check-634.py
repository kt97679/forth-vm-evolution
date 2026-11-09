#!/usr/bin/env python3
"""results/drafts/followup-check-634.py - seed 90's follow-up (Iteration 634): the one change the rule lists, the knee -
11a56ff9e4 against c2ef9488ff - checked line by line and session by session (each line's paired log-difference, its SE,
its range and how many sessions favour each), the classes with final-pick.py's pooling, and Iteration 631's four
predictions scored. Reuses followup-roles.py's pooling (exec'd with --gain, its namespace kept), as 627's check.
Run from the top: python3 results/drafts/followup-check-634.py"""
import math, statistics, sys
ROLES = 'fastest=782f3ad7ff,arm=3eb59b271d,knee=c2ef9488ff,smallarm=ae99617f06,memory=fb0d57c8a2,smallest=64a7345393'
sys.argv = ['followup-roles.py', 'results/followup-seed90.md', 'results/chain-followup90', '--roles', ROLES, '--gain']
ns, out = {'__name__': 'x'}, sys.stdout
try: exec(open('lab/evolve/followup-roles.py').read(), ns)
except SystemExit: pass
sys.stdout = out
S, C, CL, cdiff, done = ns['S'], ns['C'], ns['CL'], ns['cdiff'], ns['done']
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
A, B = '11a56ff9e4', 'c2ef9488ff'


def sess(s, a, b):
    k = [k for k in S[s][a] if k in S[s][b]]
    return [math.log(S[s][a][j] / S[s][b][j]) for j in k]


print('the knee: %s against %s - bytes %+.2f%% (%d against %d), memory %+d KB' % (
    A, B, (C[A]['total'] / C[B]['total'] - 1) * 100, C[A]['total'], C[B]['total'], C[A]['rss'] - C[B]['rss']))
L = {}
for s in ('laptop64', 'dream64', 'laptop32', 'dream32', 'laptop64-loaded', 'laptop32-loaded', 'rage'):
    d = sess(s, A, B); L[s] = d
    m = statistics.fmean(d); se = statistics.stdev(d) / math.sqrt(len(d))
    print('  %-16s %2d sessions: %s +/- %.2f%% (SE), range %s .. %s, %d of %d faster' % (
        s, len(d), pct(m), se * 100, pct(min(d)), pct(max(d)), sum(x < 0 for x in d), len(d)))
K = {}
for k in ('x86-64', 'x86-32', 'ARMv7'):
    K[k] = cdiff(k, A, B)
    print('  class %-6s %s %.4f, %s %.4f: %s +/- %.2f%%, %.1f SE' % (k, A, CL[A][k], B, CL[B][k], pct(K[k][0]),
                                                                  K[k][1] * 100, K[k][0] / K[k][1]))

print('\nThe predictions of Iteration 631 (results/predictions.md)')
full = all(len(done[s]) == n for s, n in (('laptop64', 20), ('dream64', 10), ('dream32', 10), ('rage', 2)))
print('  (1) every line complete: %s (%s); the chain 21:06:55-23:01:08 UTC (its directory and archive), 13:06-15:01 '
      'Pacific - before 9 pm: %s' % ('yes' if full else 'NO', ', '.join('%s %d' % (s, len(done[s])) for s in
                                                                         ('laptop64', 'dream64', 'dream32', 'rage')),
                                     'RIGHT' if full else 'WRONG'))
r = {k: math.exp(K[k][0]) - 1 for k in ('x86-64', 'x86-32')}; r['bytes'] = C[A]['total'] / C[B]['total'] - 1
take = (any(r[k] <= -0.02 for k in ('x86-64', 'x86-32')) or r['bytes'] <= -0.01) and \
    all(r[k] < 0.02 for k in ('x86-64', 'x86-32')) and r['bytes'] < 0.01
print('  (2) the knee by the role\'s rule (1%% smaller or 2%% faster in a class, neither class 2%% slower nor 1%% larger): '
      'x86-64 %+.2f%%, x86-32 %+.2f%%, bytes %+.2f%% - %s' % (r['x86-64'] * 100, r['x86-32'] * 100, r['bytes'] * 100,
                                                            'takes it: RIGHT' if take else 'does not: WRONG'))
m, se = K['x86-32']
print('  (3) 2%% or more faster on x86-32 at 2 SE: %s +/- %.2f%% - %s' % (
    pct(m), se * 100, 'RIGHT' if math.exp(m + 2 * se) - 1 <= -0.02 else
    'WRONG (the point past 2%%, the bound at 2 SE %s)' % pct(m + 2 * se) if math.exp(m) - 1 <= -0.02 else 'WRONG'))
lp, dr = statistics.fmean(L['laptop64']), statistics.fmean(L['dream64'])
print('  (4) the laptop agrees with dream in sign at 64 bits (faster): the laptop %s, dream %s - %s' % (
    pct(lp), pct(dr), 'RIGHT' if lp < 0 and dr < 0 else 'WRONG (%s)' % (
        'both slower' if lp > 0 and dr > 0 else 'the laptop slower, dream faster' if lp > 0 else 'dream slower')))
