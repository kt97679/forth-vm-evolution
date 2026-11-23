#!/usr/bin/env python3
"""results/drafts/series-shift-744.py DB97 CHAINB RESULTS93 RESULTS94 RESULTS95 RESULTS96 (Iteration 744) - the new series'
scale against the old one, from seed 97's generation 0: the carried designs (the fronts of seeds 93-96, measured again
in seed 97's generation 0 before any selection in it) against earlier readings of the same designs.

  0. against chain A's laptop readings (CHAINB: results/followup-seed96-roles-b.md, whose records carry them - 5
     sessions, before the after-seed-96 batch) - the reference: no selection on either side;
  1. against seed 96's re-measured fast end (the front table's 're-measured' column: 6 rounds after the run);
  2. against the fronts' in-run readings (seeds 93-96, the newest table for a design; these carry the curse, about
     1.00-1.08), by speed band, JIT or not;
  3. the bytes and the memory, exact and by page.
Seed 97's method differs from seed 96's by the after-seed-96 batch (713), the fixed measuring environment (fixenv, 727:
EVOLVE_PAD to 1,024 bytes of the initial stack), the fixed data layout (734: engine/data-layout.ld) and the five new
genes (off in a carried genome). Speeds are time / s6-cv8b's time in the same round, so a shift is against s6.
Reads only. Run with python3 -I -B."""
import json, re, statistics, sys

db, chainb, *results = sys.argv[1:]
g0 = {}
for line in open(db, errors='replace'):
    try: r = json.loads(line)
    except Exception: continue
    if r.get('gen') == 0 and r.get('status') == 'ok': g0[r['id']] = r


def front(res):
    body = open(res, errors='replace').read().split('## The Pareto front')[1].split('## How the front came about')[0]
    for l in body.split('\n'):
        c = [x.strip() for x in l.split('|')]
        if len(c) > 9 and re.fullmatch(r'[0-9a-f]{10}', c[1]):
            try: yield c[1], float(c[2]), (float(c[4]) if c[4] not in ('-', '') else None), int(c[7].replace(',', '')), int(c[8])
            except ValueError: pass


def q(v):
    v = sorted(v)
    return '%.3f (IQR %.3f-%.3f, n %d)' % (statistics.median(v), v[len(v) // 4], v[3 * len(v) // 4], len(v)) if v else '-'


jit = lambda i: bool(g0[i]['genome'].get('jit'))
print('seed 97 generation 0: %d alive' % len(g0))

print('\n0. seed 97 generation 0 / chain A\'s laptop readings (chain B\'s records)')
B = {}
for l in open(chainb, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except Exception: continue
        if r.get('id') in g0: B[r['id']] = r
for name, sel in (('JIT', jit), ('not JIT', lambda i: not jit(i))):
    ids0 = [i for i in B if sel(i)]
    print('  %-8s %s' % (name, q([g0[i]['speed'] / B[i]['speed'] for i in ids0])))
    for w in ('kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps'):
        v = [g0[i]['t'][w] / B[i]['t'][w] for i in ids0 if w in g0[i]['t'] and w in B[i].get('t', {})]
        if v: print('    %-9s %.3f' % (w, statistics.median(v)))
F = {}
for res in results:
    for i, s, r, t, m in front(res): F[i] = s
c = [B[i]['speed'] / F[i] for i in B if i in F and not jit(i)]
print('  chain A / the fronts\' in-run, not JIT (the old in-run readings\' optimism): %s' % q(c))

print('\n1. seed 97 generation 0 / seed 96 re-measured (no curse on either side)')
rm = [(i, s, r) for i, s, r, t, m in front(results[-1]) if r and i in g0]
for name, sel in (('all', lambda i: True), ('JIT', jit), ('not JIT', lambda i: not jit(i))):
    print('  %-8s %s   (seed 96 in-run / re-measured, its curse: %s)' % (
        name, q([g0[i]['speed'] / r for i, s, r in rm if sel(i)]), q([s / r for i, s, r in rm if sel(i)])))

print('\n2. seed 97 generation 0 / the fronts\' in-run readings (seeds 93-96, the newest table for a design)')
old = {}
for res in results:
    for i, s, r, t, m in front(res):
        if i in g0: old[i] = (s, t, m)
ids = sorted(old, key=lambda i: old[i][0])
ratio = {i: g0[i]['speed'] / old[i][0] for i in ids}
for name, sel in (('JIT', jit), ('not JIT', lambda i: not jit(i))):
    print('  %-8s %s' % (name, q([ratio[i] for i in ids if sel(i)])))
k = len(ids) // 6
for a in range(0, 6 * k, k):
    part = ids[a:a + k]
    print('  speed %.3f-%.3f: %s, JIT %d' % (old[part[0]][0], old[part[-1]][0], q([ratio[i] for i in part]), sum(map(jit, part))))

print('\n3. bytes (binary + image + the five programs\' code) and memory, seed 97 - own run')
db_ = [g0[i]['total'] - old[i][1] for i in ids]
dm = [g0[i]['rss'] - old[i][2] for i in ids]
print('  bytes median %+d (%+d to %+d); memory KB median %+d (%+d to %+d); n %d' % (
    statistics.median(db_), min(db_), max(db_), statistics.median(dm), min(dm), max(dm), len(ids)))
