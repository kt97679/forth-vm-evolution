#!/usr/bin/env python3
"""results/drafts/jitmiddle-716.py LIST SESSIONS POOLSIZES - chain C's pool-sizes.py JIT finds against c6f1c1331b in
in-run terms (Iteration 716; 713's method, results/drafts/chainC-candidates-713.md): the finds carry their own run's
reading (seed 96's database: speed, speed32); c6f1c1331b's record is the sandbox's, so its in-run reading is its chain C
laptop reading alone times the list's JIT designs' in-run / alone (their records from seeds 92-96, the holders' left out),
the median at each width. Each find is then compared at both widths; the ratio's spread says how far that comparison holds.
LIST: results/followup-seed96-roles-c.md; SESSIONS: results/chain-followup96-roles-c; POOLSIZES: the pack's pool-sizes.md."""
import glob, json, math, os, statistics, sys

lst, ses, pool = sys.argv[1:4]
HOLD = 'c6f1c1331b'
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
A = {'idle': {}, 'idle32': {}}                                       # the laptop alone, by width: id -> [readings]
for p in glob.glob(os.path.join(ses, 's[0-9]*', 'loadtest.md')):
    for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
        for k in A:
            if r.get('id') in C and r.get(k): A[k].setdefault(r['id'], []).append(r[k])
g = lambda v: math.exp(statistics.fmean(math.log(x) for x in v))
alone = {k: {i: g(v) for i, v in A[k].items()} for k in A}
jit = [i for i, r in C.items() if r.get('genome', {}).get('jit') and not (r.get('why') or '').startswith('a holder')]
print('# The JIT middle in in-run terms (results/drafts/jitmiddle-716.py)')
eq = {}
for k, f in (('idle', 'speed'), ('idle32', 'speed32')):
    q = sorted(C[i][f] / alone[k][i] for i in jit if C[i].get(f) and i in alone[k])
    m = statistics.median(q); lo, hi = q[len(q) // 4], q[(3 * len(q)) // 4]
    eq[f] = alone[k][HOLD] * m
    print('%s: in-run / alone over %d JIT designs of the list (not holders) - median %.3f, quartiles %.3f-%.3f (%+.1f%% / %+.1f%%);'
          ' %s alone %.4f -> in-run %.4f' % (f, len(q), m, lo, hi, (lo / m - 1) * 100, (hi / m - 1) * 100, HOLD, alone[k][HOLD], eq[f]))
F = [json.loads(l) for l in open(pool) if l.startswith('{"')]
print('pool-sizes.py finds: %d, %d-%d B after the batch (%s %d B); with both widths\' in-run readings: %d'
      % (len(F), min(r['total'] for r in F), max(r['total'] for r in F), HOLD, C[HOLD]['total'],
         sum(1 for r in F if r.get('speed') and r.get('speed32'))))
rows = []
for r in F:
    if not (r.get('speed') and r.get('speed32')): continue
    d64, d32 = r['speed'] / eq['speed'] - 1, r['speed32'] / eq['speed32'] - 1
    rows.append((max(d64, d32), d64, d32, r['total'], r['id'], r.get('rss')))
for lim in (0.02, 0.05, 0.10, 0.20):
    w = [x for x in rows if x[0] <= lim]
    print('  within %2d%% at both widths: %4d%s' % (lim * 100, len(w), (' - the smallest %s %d B' % (min(w, key=lambda x: x[3])[4], min(w, key=lambda x: x[3])[3])) if w else ''))
print('  the best by the slower width (in-run against %s\'s in-run terms):' % HOLD)
for x in sorted(rows)[:10]:
    print('    %s %6d B (%+.1f%%)  x86-64 %+.1f%%, x86-32 %+.1f%%, rss %s KB' % (x[4], x[3], (x[3] / C[HOLD]['total'] - 1) * 100, x[1] * 100, x[2] * 100, x[5]))
print('  the smallest five: ' + '; '.join('%s %d B %+.0f%% / %+.0f%%' % (x[4], x[3], x[1] * 100, x[2] * 100) for x in sorted(rows, key=lambda x: x[3])[:5]))
print('  the list\'s JIT middle by the same terms (their own runs\' readings - a check on the terms against chain C\'s rule):')
for i in ('15eda54ebd', 'fa38596098', '13a2b38e1b', '08578f5e3d'):
    if i in C: print('    %s %d B  x86-64 %+.1f%%, x86-32 %+.1f%%' % (i, C[i]['total'], (C[i]['speed'] / eq['speed'] - 1) * 100, (C[i]['speed32'] / eq['speed32'] - 1) * 100))
