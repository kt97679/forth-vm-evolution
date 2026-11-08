#!/usr/bin/env python3
"""results/drafts/followup-check-627.py - seed 89's follow-up (Iteration 627): the role changes the rule lists, checked
session by session - each pair's paired log-difference per source and session, the class figure with its SE, and for the
Tegra's three sessions the t-interval (2 degrees of freedom) beside the rule's 2 SE. Reuses followup-roles.py's pooling
(exec'd with --gain, its namespace kept). Run from the top: python3 results/drafts/followup-check-627.py"""
import io, math, statistics, sys
ROLES = ('fastest=782f3ad7ff,arm=690981ca5b,knee=c2ef9488ff,smallarm=a627b954c6,memory=fb0d57c8a2,smallest=64a7345393,'
         'fast64=c7c35f9c97,fast32=4ef851fd8e,allround=06b188f45b,smalljit=bac37f35a2')
sys.argv = ['followup-roles.py', 'results/followup-seed89.md', 'results/chain-followup89', '--roles', ROLES, '--gain']
ns, out = {'__name__': 'x'}, sys.stdout
try: exec(open('lab/evolve/followup-roles.py').read(), ns)
except SystemExit: pass
sys.stdout = out
S, C, CL, cdiff = ns['S'], ns['C'], ns['CL'], ns['cdiff']
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}
def sess(s, a, b):
    k = [k for k in S[s][a] if k in S[s][b]]
    return [math.log(S[s][a][j] / S[s][b][j]) for j in k]
PAIRS = [('fast32', 'ee34931cd7', '4ef851fd8e', ('laptop32', 'dream32'), 'x86-32'),
         ('fast32', '68f5ce466c', '4ef851fd8e', ('laptop32', 'dream32'), 'x86-32'),
         ('extreme 32 laptop', '68f5ce466c', '06b188f45b', ('laptop32',), None),
         ('arm', '3eb59b271d', '690981ca5b', ('rage',), 'ARMv7'),
         ('arm', '768bd275d8', '690981ca5b', ('rage',), 'ARMv7'),
         ('smallarm', '8164d3858f', 'a627b954c6', ('rage',), 'ARMv7'),
         ('smallarm', 'ae99617f06', 'a627b954c6', ('rage',), 'ARMv7'),
         ('smalljit', 'c6f1c1331b', 'bac37f35a2', ('laptop64', 'dream64', 'laptop32', 'dream32'), None),
         ('smalljit', '93364d4fc2', 'bac37f35a2', ('laptop64', 'dream64', 'laptop32', 'dream32'), None)]
for role, a, b, srcs, cls in PAIRS:
    print('%s: %s against %s - bytes %+.2f%% (%d against %d), memory %+d KB' % (role, a, b,
          (C[a]['total'] / C[b]['total'] - 1) * 100, C[a]['total'], C[b]['total'], C[a]['rss'] - C[b]['rss']))
    for s in srcs:
        d = sess(s, a, b); m = statistics.fmean(d); se = statistics.stdev(d) / math.sqrt(len(d))
        t = T975.get(len(d) - 1)
        print('  %-9s %2d sessions: %s +/- %.2f%% (SE), range %s .. %s%s' % (s, len(d), pct(m), se * 100, pct(min(d)),
              pct(max(d)), '; 95%% t-interval %s .. %s' % (pct(m - t * se), pct(m + t * se)) if t else ''))
        if len(d) <= 5: print('            per session: %s' % ' '.join(pct(x) for x in d))
    if cls:
        m, se = cdiff(cls, a, b); print('  class %s: %s +/- %.2f%%' % (cls, pct(m), se * 100))
