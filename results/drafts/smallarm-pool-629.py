#!/usr/bin/env python3
"""results/drafts/smallarm-pool-629.py [DIR ...] - small and fast on ARMv7, decided by the rule fixed before seed 90's
data (Iteration 629; results/followup-roles-seed89.md, "The re-measure's rule"): 8164d3858f and ae99617f06 against
a627b954c6 on the Tegra, every session of every DIR pooled - each session one paired log-difference (the follow-up's at
10 rounds, seed 90's screen's at 3), equal weights, the SE from their spread. A challenger takes the role at 2% faster
and 2 SE (the role rule fixed before seed 87), the faster of the two if both; else a627b954c6 keeps it and the question
is closed. DIR: chain-sessions.py's layout (sK/rage.lan-prebuiltarm.out.json); default results/chain-followup89 and,
when there, results/chain-screen89. Rehearsed at 629 on the follow-up alone: 8164d3858f -2.45% +/- 0.68%, as
results/drafts/followup-check-627.py has it."""
import glob, json, math, os, statistics, sys
H, CH = 'a627b954c6', ('8164d3858f', 'ae99617f06')
D = sys.argv[1:] or [d for d in ('results/chain-followup89', 'results/chain-screen89') if os.path.isdir(d)]
rows = []
for d in D:
    for f in sorted(glob.glob(os.path.join(d, 's*', 'rage.lan-prebuiltarm.out.json')), key=lambda f: int(f.split('/')[-2][1:])):
        o = json.load(open(f))
        rows.append({x['id']: x['speed_here'] for x in o['designs'] if x.get('speed_here') and not x.get('rejected')})
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
print('the Tegra: %d sessions in %s' % (len(rows), ', '.join(D)))
best = None
for c in CH:
    d = [math.log(v[c] / v[H]) for v in rows if c in v and H in v]
    if len(d) < 2: print('  %s: %d sessions with both - too few' % (c, len(d))); continue
    m = statistics.fmean(d); se = statistics.stdev(d) / math.sqrt(len(d)); ok = math.exp(m) - 1 <= -0.02 and m <= -2 * se
    print('  %s against %s, %d sessions: %s; pooled %s +/- %.2f%% - %s' % (c, H, len(d), ' '.join(pct(x) for x in d), pct(m),
          se * 100, 'past 2% at 2 SE' if ok else 'not by the rule'))
    if ok and (best is None or m < best[0]): best = (m, c)
print('verdict: %s' % ('%s takes small and fast on ARMv7 - by 620 the portable search reopens' % best[1] if best else
                       'a627b954c6 keeps small and fast on ARMv7 - the question closed'))
