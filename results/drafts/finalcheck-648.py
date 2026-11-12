#!/usr/bin/env python3
"""results/drafts/finalcheck-648.py - the final check's (results/followup-seed91-final.md, chain 16681a02bf) figures beyond
process-followup.sh's summary (Iteration 648), from results/chain-followup91-final and the earlier chains' readings:
  1. the smallest's one candidate without a trade, d180351903 against 64a7345393 - each line by session (paired), the
     classes as followup-roles.py pools them, and the two genomes' expressed difference;
  2. small and fast on ARMv7 - a627b954c6 (-3.21% here) against the holder ae99617f06, every Tegra session of every chain
     that measured both, 629's way (each session one paired log-difference, equal weights; 2% at 2 SE);
  3. the Tegra's first session (load 3.0 on average, peak 8 - remote-load.py) against its second: the 435's shift and
     spread, and the ARMv7 pairs above session by session.
Run from the repository's top: python3 results/drafts/finalcheck-648.py"""
import contextlib, glob, io, json, math, os, statistics, sys
sys.path.insert(0, 'lab/evolve')
ROLES = 'fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,smallest=64a7345393'
F = 'lab/evolve/followup-roles.py'
sys.argv = [F, 'results/followup-seed91-final.md', 'results/chain-followup91-final', '--roles', ROLES,
            '--handoff', 'results/handoff-relf-636.md']
g = {'__name__': 'finalcheck', '__file__': F}
with contextlib.redirect_stdout(io.StringIO()):
    try: exec(compile(open(F).read(), F, 'exec'), g)
    except SystemExit: pass
S, C, PARTS, cdiff = g['S'], g['C'], g['PARTS'], g['cdiff']
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)


def pairs(s, a, b):
    return [(k, math.log(S[s][a][k] / S[s][b][k])) for k in sorted(S[s][a]) if k in S[s][b]]


def ms(d):
    return statistics.fmean(d), (statistics.stdev(d) / math.sqrt(len(d)) if len(d) > 1 else float('nan'))


A, H = 'd180351903', '64a7345393'
print('## 1. %s (%s B) against the smallest, %s (%s B): %+d B' % (A, format(C[A]['total'], ','), H,
      format(C[H]['total'], ','), C[A]['total'] - C[H]['total']))
print('  engine %+d B, image %+d B, memory %+d KB; %s' % (C[A]['bin'] - C[H]['bin'], C[A]['size'] - C[H]['size'],
      C[A]['rss'] - C[H]['rss'], C[A]['why']))
for s in S:
    p = pairs(s, A, H)
    if p:
        m, se = ms([d for k, d in p])
        print('  %-16s %s +/- %.2f%% (%d sessions: %s)' % (s, pct(m), se * 100, len(p), ' '.join(pct(d) for k, d in p)))
for k in PARTS:
    m, se = cdiff(k, A, H); print('  class %-7s %s +/- %.2f%%' % (k, pct(m), se * 100))
sys.argv = ['x']
import evolve as E
xa, xh = (E.express(E.canon(C[i]['genome'])) for i in (A, H))
print('  expressed genes that differ (%s -> %s): %s' % (H, A, '; '.join('%s %s -> %s' % (k, xh.get(k), xa.get(k))
      for k in sorted(set(xa) | set(xh)) if xa.get(k) != xh.get(k))))

print('\n## 2. Small and fast on ARMv7 - a627b954c6 against ae99617f06, every Tegra session that measured both')
CH, HO = 'a627b954c6', 'ae99617f06'
rows = []
for f in sorted(glob.glob('results/chain-*/s*/rage.lan-prebuiltarm.out.json')):
    o = json.load(open(f))
    v = {x['id']: x['speed_here'] for x in o['designs'] if x.get('speed_here')}
    if CH in v and HO in v: rows.append((f.split('/')[1] + '/' + f.split('/')[2], math.log(v[CH] / v[HO])))
for name, sel in (('every chain', rows), ('before this chain', [r for r in rows if 'final' not in r[0]]),
                  ('this chain', [r for r in rows if 'final' in r[0]]),
                  ('every chain, this one\'s loaded s1 out', [r for r in rows if r[0] != 'chain-followup91-final/s1'])):
    if len(sel) < 2: print('  %s: %d sessions' % (name, len(sel))); continue
    m, se = ms([d for k, d in sel]); ok = math.exp(m) - 1 <= -0.02 and m <= -2 * se
    print('  %-38s %2d sessions: %s +/- %.2f%% - %s' % (name, len(sel), pct(m), se * 100,
          'a627b954c6 past 2% at 2 SE' if ok else 'not by the rule'))
by = {}
for k, d in rows: by.setdefault(k.split('/')[0], []).append(pct(d))
print('  by chain: ' + '; '.join('%s %s' % (c, ' '.join(v)) for c, v in by.items()))

print('\n## 3. The Tegra\'s first session (loaded) against its second, this chain')
r = S['rage']; both = [i for i in r if 0 in r[i] and 1 in r[i]]
d = sorted(math.log(r[i][0] / r[i][1]) for i in both)
q = lambda p: d[min(len(d) - 1, int(p * len(d)))]
print('  %d designs in both: s1/s2 median %s, quartiles %s %s, 5%%-95%% %s %s' % (len(both), pct(q(.5)), pct(q(.25)),
      pct(q(.75)), pct(q(.05)), pct(q(.95))))
for a, b in ((CH, HO), (A, H), ('7fb40ff7ba', '3eb59b271d')):
    p = pairs('rage', a, b); print('  %s against %s: %s' % (a, b, ', '.join('s%d %s' % (k + 1, pct(x)) for k, x in p)))

print('\n## 4. The Tegra\'s kernel - 7.3.1 to 7.3.3 between seed 90\'s screen (2026-11-10 10:48) and seed 91\'s follow-up (23:07)')
import collections
K = collections.defaultdict(lambda: collections.defaultdict(list))     # kernel -> design -> [log speed_here]
CK = collections.defaultdict(lambda: collections.defaultdict(list))    # chain -> design -> [log speed_here]
for f in glob.glob('results/chain-*/s*/rage.lan-prebuiltarm.out.json'):
    o = json.load(open(f)); kern = str(o.get('env', {}).get('kernel', '?'))
    for x in o['designs']:
        if x.get('speed_here'):
            K[kern][x['id']].append(math.log(x['speed_here'])); CK[f.split('/')[1]][x['id']].append(math.log(x['speed_here']))


def shift(a, b, label):          # each design's mean log reading in b against a; the spread around the median is re-ranking
    both = [i for i in a if i in b]
    d = sorted(statistics.fmean(b[i]) - statistics.fmean(a[i]) for i in both)
    if len(d) < 8: print('  %s: %d designs in both' % (label, len(d))); return
    q = lambda p: d[min(len(d) - 1, int(p * len(d)))]; med = q(.5)
    print('  %-44s %3d designs: median %s; around it IQR %s, 5%%-95%% %s' % (label, len(d), pct(med),
          '%.2f%%' % ((q(.75) - q(.25)) * 100), '%.2f%%' % ((q(.95) - q(.05)) * 100)))


ks = sorted(K)
print('  kernels: ' + ', '.join('%s %d designs' % (k, len(K[k])) for k in ks))
if len(ks) == 2: shift(K[ks[0]], K[ks[1]], 'across the kernels (%s -> %s)' % tuple(ks))
shift(CK['chain-followup89'], CK['chain-screen89'], 'the same kernel: chain-followup89 -> chain-screen89')
shift(CK['chain-screen89'], CK['chain-screen90'], 'the same kernel: chain-screen89 -> chain-screen90')
shift(CK['chain-followup91'], CK['chain-followup91-final'], 'the same kernel: chain-followup91 -> the final')
for i in ('ae99617f06', 'a627b954c6', '3eb59b271d', '7fb40ff7ba', '782f3ad7ff', '64a7345393', 'd180351903'):
    if len(ks) == 2 and i in K[ks[0]] and i in K[ks[1]]:
        print('  %s %s -> %s: %s' % (i, ks[0], ks[1], pct(statistics.fmean(K[ks[1]][i]) - statistics.fmean(K[ks[0]][i]))))
