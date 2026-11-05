#!/usr/bin/env python3
"""results/drafts/followup-roles-611.py - the follow-up chain's figures (Iteration 611; results/followup-roles-seed87.md):
the readings of results/chain-followup87/sK pooled as final-pick.py pools them (each source's geometric mean over its
sessions; x86-64 and x86-32 the geometric mean of the laptop alone and dream, ARMv7 the Tegra; the mean of the three),
with errors paired by session (two designs read in the same session; the class's log-difference SE from each source's
per-session log ratios). Prints: each line's completeness; the noise against the chain's sizing (NEXT-RUN 610: a
session moves a design 0.7-0.9%); the five portable roles of results/handoff-relf-601.md against the 45 by the rule fixed
before seed 87 (results/drafts/portable-plan-602.md: speed 2%, binary + image 1%, memory 4 KB); the predictions of 610;
dream's 4-byte line against the laptop's by the genes factor and compiler."""
import glob, json, math, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'results/followup-seed87.md')
SESS = os.path.join(ROOT, 'results/chain-followup87')
SOURCES = ('laptop64', 'laptop32', 'laptop64-loaded', 'laptop32-loaded', 'dream64', 'dream32', 'rage')
HOSTFILE = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json',
            'rage': 'rage.lan-prebuiltarm.out.json'}
LAPKEY = {'laptop64': 'idle', 'laptop32': 'idle32', 'laptop64-loaded': 'loaded', 'laptop32-loaded': 'loaded32'}
PARTS = {'x86-64': ('laptop64', 'dream64'), 'x86-32': ('laptop32', 'dream32'), 'ARMv7': ('rage',)}
T, B, M = 0.02, 0.01, 4                      # speed 2%, binary + image 1%, memory 4 KB
gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)

C = {r['id']: r for r in (json.loads(l) for l in open(CAND) if l.startswith('{'))}
S = {s: {i: [] for i in C} for s in SOURCES}
done = {s: [] for s in SOURCES}
for d in sorted(glob.glob(os.path.join(SESS, 's*')), key=lambda d: int(d.rsplit('s', 1)[1])):
    lt = os.path.join(d, 'loadtest.md')
    if os.path.exists(lt):
        L = {}
        for l in open(lt, errors='replace'):
            if l.startswith('{"'):
                r = json.loads(l); L[r.get('id')] = r
        for s, k in LAPKEY.items():
            n = [i for i in C if L.get(i, {}).get(k)]
            for i in n: S[s][i].append(L[i][k])
            done[s].append(len(n))
    for s, f in HOSTFILE.items():
        if os.path.exists(os.path.join(d, f)):
            o = json.load(open(os.path.join(d, f)))
            n = [x for x in o['designs'] if x.get('id') in C and not x.get('rejected') and x.get('speed_here')]
            for x in n: S[s][x['id']].append(x['speed_here'])
            done[s].append(len(n))
P = {s: {i: gm(v) for i, v in S[s].items() if v} for s in SOURCES}
CL = {}
for i in C:
    c = {k: gm([P[s][i] for s in p]) for k, p in PARTS.items()}
    c['mean'] = gm(list(c.values())); CL[i] = c


def paired(s, a, b):
    d = [math.log(x / y) for x, y in zip(S[s][a], S[s][b])]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))


def cdiff(k, a, b):
    ds = [paired(s, a, b) for s in PARTS[k]]
    return sum(x[0] for x in ds) / len(ds), math.sqrt(sum(x[1] ** 2 for x in ds)) / len(ds)


def mdiff(a, b):
    ds = [cdiff(k, a, b) for k in PARTS]
    return sum(x[0] for x in ds) / 3, math.sqrt(sum(x[1] ** 2 for x in ds)) / 3


print('## Completeness - sessions, and the fewest of the 45 a session measured')
for s in SOURCES:
    print('  %-16s %2d sessions, each %d-%d of 45' % (s, len(done[s]), min(done[s]), max(done[s])))

print('\n## Noise - a design\'s session-to-session SD (median over the 45), without and with each session\'s common shift')
ids = sorted(C)
for s in SOURCES:
    n = len(S[s][ids[0]]); L = {i: [math.log(v) for v in S[s][i]] for i in ids}
    sh = [statistics.median(L[i][k] - statistics.fmean(L[i]) for i in ids) for k in range(n)]
    raw = statistics.median(statistics.stdev(L[i]) for i in ids)
    adj = statistics.median(statistics.stdev([L[i][k] - sh[k] for k in range(n)]) for i in ids)
    t3 = max(1, n // 3)
    print('  %-16s %2d: SD %.2f%%, paired %.2f%%; a paired difference\'s SE %.2f%%; the shift\'s range %.2f%%, first '
          'third to last %+.2f%%' % (s, n, raw * 100, adj * 100, adj * math.sqrt(2 / n) * 100, (max(sh) - min(sh)) * 100,
                                     (statistics.fmean(sh[-t3:]) - statistics.fmean(sh[:t3])) * 100))

print('\n## The roles (results/handoff-relf-601.md) - speed 2%, binary + image 1%, memory 4 KB')
inc = '690981ca5b'; bm = min(C, key=lambda i: CL[i]['mean']); m, se = mdiff(bm, inc)
print('  fastest portable (the best mean): %s %.4f against %s %.4f: %s +/- %.2f%%' % (bm, CL[bm]['mean'], inc,
                                                                                     CL[inc]['mean'], pct(m), se * 100))
for k in PARTS:
    m, se = cdiff(k, bm, inc)
    print('    %s %s %.4f, %s %.4f: %s +/- %.2f%%' % (k, bm, CL[bm][k], inc, CL[inc][k], pct(m), se * 100))
arm = sorted(C, key=lambda i: CL[i]['ARMv7'])
print('  fastest on ARMv7: %s' % ', '.join('%s %.4f' % (i, CL[i]['ARMv7']) for i in arm[:5]))
for i in arm[:4]:
    if i != inc:
        m, se = cdiff('ARMv7', i, inc); print('    %s against %s: %s +/- %.2f%%' % (i, inc, pct(m), se * 100))


def role(inc, keys, name):
    print('  %s - %s: %s, %s B, %d KB' % (name, inc, ', '.join('%s %.4f' % (k, CL[inc][k]) for k in keys),
                                          format(C[inc]['total'], ','), C[inc]['rss']))
    for i in sorted(C, key=lambda i: C[i]['total']):
        if i == inc: continue
        r = {k: CL[i][k] / CL[inc][k] - 1 for k in keys}; r['bytes'] = C[i]['total'] / C[inc]['total'] - 1
        th = dict({k: T for k in keys}, bytes=B)
        if any(r[k] <= -th[k] for k in r) and all(r[k] < th[k] for k in r):
            print('    %s: %s, memory %+d KB' % (i, ', '.join('%s %+.2f%%' % (k, v * 100) for k, v in r.items()),
                                                C[i]['rss'] - C[inc]['rss']))


role('c2ef9488ff', ('x86-64', 'x86-32'), 'the knee')
role('22420b3b61', ('ARMv7',), 'small, fast on ARMv7')
lm = sorted(C, key=lambda i: C[i]['rss'])
print('  least memory - fb0d57c8a2 %d KB; the next %s' % (C['fb0d57c8a2']['rss'],
                                                       ', '.join('%s %d KB' % (i, C[i]['rss']) for i in lm[1:3])))
inc = 'cea114f47e'
print('  smallest - %s %s B; smaller:' % (inc, format(C[inc]['total'], ',')))
for i in sorted(C, key=lambda i: C[i]['total']):
    if C[i]['total'] >= C[inc]['total']: break
    print('    %s %s B (%+.2f%%): %s, memory %+d KB' % (i, format(C[i]['total'], ','),
          (C[i]['total'] / C[inc]['total'] - 1) * 100,
          ', '.join('%s %s +/- %.2f%%' % ((k,) + (lambda d: (pct(d[0]), d[1] * 100))(cdiff(k, i, inc))) for k in PARTS),
          C[i]['rss'] - C[inc]['rss']))

print('\n## The predictions of Iteration 610')
print('  (1) the Tegra %d sessions, each %d of 45' % (len(done['rage']), min(done['rage'])))
run = [i for i in C if C[i]['why'].startswith('the run')]
for f, w in ((min(run, key=lambda i: C[i]['speed']), 'in-run, named "the run - fastest"'),
             (min(run, key=lambda i: P['laptop64'][i]), 're-measured')):
    m, se = paired('laptop64', f, '8cc7f60d6b')
    print('  (2) the run\'s fastest (%s) %s against 8cc7f60d6b, the laptop alone: %s +/- %.2f%%' % (w, f, pct(m), se * 100))
m, se = cdiff('ARMv7', '3452cb633b', '690981ca5b')
print('  (4) ARMv7 3452cb633b against 690981ca5b: %s +/- %.2f%%' % (pct(m), se * 100))

print('\n## dream against the laptop by (factor, compiler) - the median of dream/laptop at 4-byte and 8-byte cells, and '
      'the Tegra/laptop at 4')
g = {}
for i in C:
    k = (C[i]['genome']['factor'], C[i]['genome']['compiler'])
    g.setdefault(k, []).append((P['dream32'][i] / P['laptop32'][i], P['dream64'][i] / P['laptop64'][i],
                                P['rage'][i] / P['laptop32'][i]))
for k in sorted(g):
    print('  factor %d, compiler %d: %2d designs, %.3f %.3f %.3f' % (k + (len(g[k]),) + tuple(
        statistics.median(x[j] for x in g[k]) for j in range(3))))
a = [x for v in g.values() for x in v]
print('  all 45: %.3f %.3f %.3f' % tuple(statistics.median(x[j] for x in a) for j in range(3)))
