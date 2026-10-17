#!/usr/bin/env python3
"""footprint-gen.py N [--calls T] [--levels L] [--seed S] [--defs-only] - a program of N words
whose code footprint grows with N (Iteration 370; results/generalization.md, section 3).

Selection measures small programs: their hot code fits the caches and the predictors see few
dispatch contexts. This writes one Forth program to standard output: N colon definitions in L
levels - a word of level 0 calls nothing, a word of level k > 0 calls one word of level k - 1,
chosen by a test on its argument (two candidates, IF ... ELSE ... THEN), so every call runs a
chain of at most L words and the return stack stays shallow at any N. Then a table of every
word's execution token, and a driver that runs the table round-robin until T calls are made in
all: the same work at every N, so the time per call compares across N - at N = 100 each word is
run thousands of times (hot), at N = 30,000 a few (cold: the caches, the predictors, a JIT's
translation of code run once). The definitions are the compile-heavy part: N names compiled,
each body finding its callees in a dictionary of up to N words. --defs-only stops after the
table, before the run, so a design's run time is the full program's less the definitions-only
one's.

Prints a checksum - the same for every correct design, and for the hand-made s6. Deterministic
for given N, T, L and S: the same program everywhere. Words used: : ; IF ELSE THEN DUP
+ - AND XOR 2* 2/ ' , CREATE CELLS @ EXECUTE DO LOOP I . CR - core words only.
"""
import argparse, random, sys

def program(n, calls, levels, seed, defs_only):
    rnd = random.Random(seed * 1000003 + n)
    levels = max(1, min(levels, n))
    lv = [[] for _ in range(levels)]
    for i in range(n): lv[i * levels // n].append(i)        # level k: the k-th slice of the words
    out = ['\\ footprint-gen.py %d --calls %d --levels %d --seed %d%s' % (n, calls, levels, seed, ' --defs-only' if defs_only else '')]
    ops = ['1 +', '3 XOR', 'DUP 2* XOR', 'DUP 7 AND +', '2/ 1 +', 'DUP 5 AND XOR', '11 -', 'DUP 3 AND +']
    for k in range(levels):
        for i in lv[k]:
            a, b = rnd.choice(ops), rnd.choice(ops)
            if k == 0:
                body = '%s %s' % (a, b)
            else:
                c1, c2 = rnd.choice(lv[k - 1]), rnd.choice(lv[k - 1])
                m = rnd.choice([1, 2, 4, 8])
                body = '%s DUP %d AND IF w%d ELSE w%d THEN %s' % (a, m, c1, c2, b)
            out.append(': w%d ( n -- n ) %s ;' % (i, body))
    out.append('CREATE XTS')                                  # the table: N names found - in both variants
    for i in range(0, n, 8):
        out.append(' '.join("' w%d ," % j for j in range(i, min(i + 8, n))))
    if defs_only:
        out.append('0 w%d . CR' % (n - 1))
        return '\n'.join(out) + '\n'
    rounds, rest = divmod(calls, n)
    out.append(': RUN ( -- sum )  0  %d 0 DO  %d 0 DO  I CELLS XTS + @ EXECUTE 65535 AND  LOOP  LOOP' % (rounds, n)
               + ('  %d 0 DO  I CELLS XTS + @ EXECUTE 65535 AND  LOOP ;' % rest if rest else ' ;'))
    out.append('RUN . CR')
    return '\n'.join(out) + '\n'

if __name__ == '__main__':
    ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
    ap.add_argument('n', type=int)
    ap.add_argument('--calls', type=int, default=200000)
    ap.add_argument('--levels', type=int, default=8)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--defs-only', action='store_true')
    a = ap.parse_args()
    if a.n < 1 or a.calls < 1: sys.exit('footprint-gen: N and --calls must be at least 1')
    sys.stdout.write(program(a.n, a.calls, a.levels, a.seed, a.defs_only))
