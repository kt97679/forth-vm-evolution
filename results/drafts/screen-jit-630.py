#!/usr/bin/env python3
"""results/drafts/screen-jit-630.py - the 82 JIT designs of seed 89's rest (results/screen-seed89.md) that seed 90's remote
lines measured beside the portable ones (Iteration 630: the screen leaves them out - a portable role's candidate is
JIT-free), read against the four x86 roles' holders on dream, paired by session (results/chain-screen89): x86-64
c7c35f9c97 (dream64), x86-32 ee34931cd7 (dream32 - its sessions 4-6 under load, results/drafts/dream-load-630.py), best
all-round 06b188f45b (the mean of dream64, dream32 and the Tegra's JIT-off build), the smallest JIT design c6f1c1331b
(binary + image, exact). Information only: by 620 seed 90's no-gain leaves the x86 roles final; the laptop not measured."""
import glob, json, math, os, statistics, sys
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open('results/screen-seed89.md') if l.startswith('{'))}
J = [i for i in C if str(C[i].get('why', '')).startswith('the run') and E.express(E.canon(C[i]['genome'])).get('jit')]
F = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
S = {x: [{d['id']: math.log(d['speed_here']) for d in json.load(open(f))['designs'] if d.get('speed_here') and not d.get('rejected')}
         for f in sorted(glob.glob('results/chain-screen89/s*/' + n), key=lambda f: int(f.split('/')[-2][1:]))] for x, n in F.items()}
def pd(x, i, h):
    d = [s[i] - s[h] for s in S[x] if i in s and h in s]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
print('the JIT designs of seed 89\'s rest: %d' % len(J))
for role, h, src in (('x86-64', 'c7c35f9c97', ('dream64',)), ('x86-32', 'ee34931cd7', ('dream32',)), ('best all-round', '06b188f45b', ('dream64', 'dream32', 'rage'))):
    r = sorted((sum(pd(x, i, h)[0] for x in src) / len(src), i, [pd(x, i, h) for x in src]) for i in J)
    fast = [t for t in r if t[0] < 0]
    past = [t for t in fast if len(src) > 1 and math.exp(t[0]) - 1 <= -0.02 or len(src) == 1 and math.exp(t[0]) - 1 <= -0.02 and t[0] <= -2 * t[2][0][1]]
    print('  %s - %s on %s: faster %d, past 2%%%s %d%s' % (role, h, '+'.join(src), len(fast), '' if len(src) > 1 else ' at 2 SE', len(past),
          ''.join('\n    %s %s%s' % (i, pct(m), '' if len(src) > 1 else ' +/- %.2f%%' % (e[0][1] * 100)) for m, i, e in fast[:5])))
h = 'c6f1c1331b'; sm = sorted((C[i]['total'], i) for i in J if C[i]['total'] < C[h]['total'])
print('  the smallest JIT design - %s %s bytes: smaller %d%s' % (h, format(C[h]['total'], ','), len(sm), ''.join(' %s %s' % (i, format(t, ',')) for t, i in sm[:5])))
ok = [(t, i, pd('dream64', i, h)[0], pd('dream32', i, h)[0]) for t, i in sm]   # the trade (611, 621): 1% smaller, no speed lost
ok = [x for x in ok if x[0] <= 0.99 * C[h]['total'] and math.exp(x[2]) - 1 < 0.02 and math.exp(x[3]) - 1 < 0.02]
print('    1%% smaller and under 2%% slower on dream at both widths: %d%s' % (len(ok), ''.join('\n    %s %s B (%+.2f%%): dream64 %s, dream32 %s'
      % (i, format(t, ','), (t / C[h]['total'] - 1) * 100, pct(a), pct(b)) for t, i, a, b in ok[:8])))
