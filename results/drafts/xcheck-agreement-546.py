#!/usr/bin/env python3
"""results/drafts/xcheck-agreement-546.py CHAIN RESULTS - how far the remote checks agree with the laptop, and why
(Iteration 546). CHAIN: an unpacked chain archive (its remote/<host>/out.json and designs.json - every design's ratios
per workload there); RESULTS: the results file of the run whose front they checked (its records: the laptop's in-run
speeds, per workload in t, and the report's re-measured column). Per host: Spearman with a 95% bootstrap interval; JIT
designs against the rest (here / laptop, and the order within each); per workload; the designs that disagree most;
near ties; dream's two 64-bit sessions against each other; the re-measured speeds; how far the laptop's fastest lands
behind each host's best."""
import glob, json, math, os, random, re, statistics as st, sys
chain, res = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lab/evolve')); import evolve as E
recs, rem = {}, {}
for l in open(res, errors='replace'):
    if l.startswith('{"'):
        try: r = json.loads(l); recs[r['id']] = r
        except ValueError: pass
    f = [x.strip() for x in l.split('|')]
    if len(f) > 6 and re.fullmatch(r'[0-9a-f]{10}', f[1] or '') and re.fullmatch(r'[0-9.]+', f[4] or ''): rem[f[1]] = float(f[4])
W = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']
def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2.0
        i = j + 1
    return r
def sp(a, b):
    ra, rb = ranks(list(a)), ranks(list(b)); ma, mb = st.mean(ra), st.mean(rb)
    d = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / d if d else float('nan')
O, G = {}, {}
for f in sorted(glob.glob(os.path.join(chain, 'remote', '*', 'out.json'))):
    h = os.path.basename(os.path.dirname(f)); O[h] = json.load(open(f))['designs']
    try: G.update({g['id']: g.get('genome') for g in json.load(open(os.path.join(os.path.dirname(f), 'designs.json')))})
    except (OSError, ValueError, TypeError): pass
def jit(i):
    g = (recs.get(i) or {}).get('genome') or G.get(i)
    return bool(g) and bool(E.jit_on(E.canon(g)))
rnd = random.Random(1)
for h, ds in O.items():
    n = len(ds); lap = [d['speed'] for d in ds]; her = [d['speed_here'] for d in ds]; rho = sp(lap, her)
    bs = sorted(sp(*zip(*[(lap[k], her[k]) for k in [rnd.randrange(n) for _ in range(n)]])) for _ in range(2000))
    print('\n%s: %d designs, Spearman %.3f (95%% bootstrap %.3f-%.3f)' % (h, n, rho, bs[50], bs[1949]))
    for name, grp in (('JIT', [d for d in ds if jit(d['id'])]), ('no JIT', [d for d in ds if not jit(d['id'])])):
        if not grp: continue
        q = [d['speed_here'] / d['speed'] for d in grp]
        print('  %-6s %2d: here/laptop median %.2f (%.2f-%.2f), laptop %.3f-%.3f%s' % (name, len(grp), st.median(q), min(q), max(q),
              min(d['speed'] for d in grp), max(d['speed'] for d in grp), ', Spearman within %.3f' % sp([d['speed'] for d in grp], [d['speed_here'] for d in grp]) if len(grp) >= 5 else ''))
    fr = [d for d in ds if d['id'] in recs and recs[d['id']].get('t')]
    print('  per workload (laptop t against here):', ', '.join('%s %.2f' % (w, sp([recs[d['id']]['t'][w] for d in fr if w in recs[d['id']]['t']], [d['ratios'][w] for d in fr if w in recs[d['id']]['t']])) for w in W if len(fr) >= 5))
    loo = sorted(((sp([x for k, x in enumerate(lap) if k != m], [x for k, x in enumerate(her) if k != m]) - rho, ds[m]) for m in range(n)), key=lambda t: -t[0])[:3]
    print('  disagree most (Spearman without it):', '; '.join('%s laptop %.3f here %.3f (%+.3f)' % (d['id'], d['speed'], d['speed_here'], g) for g, d in loo))
    print('  laptop pairs within 3%%: %d of %d' % (sum(1 for a in range(n) for b in range(a + 1, n) if abs(math.log(lap[a] / lap[b])) < 0.03), n * (n - 1) // 2))
    x = [d for d in ds if d['id'] in rem]
    if len(x) >= 5: print('  with the laptop\'s re-measured speeds (%d): %.3f; the laptop in-run against re-measured %.3f' % (len(x), sp([rem[d['id']] for d in x], [d['speed_here'] for d in x]), sp([d['speed'] for d in x], [rem[d['id']] for d in x])))
    best = min(ds, key=lambda d: d['speed_here']); top = sorted(ds, key=lambda d: d['speed'])
    print('  the laptop\'s fastest %.1f%% behind this host\'s best; its six fastest 0.0-%.1f%%; this host\'s best the laptop\'s #%d, %.1f%% behind its fastest there' % (
        100 * (top[0]['speed_here'] / best['speed_here'] - 1), 100 * (max(d['speed_here'] for d in top[:6]) / best['speed_here'] - 1), 1 + top.index(best), 100 * (best['speed'] / top[0]['speed'] - 1)))
a = {d['id']: d['speed_here'] for d in O.get('dream.lan-prebuilt', [])}; b = {d['id']: d['speed_here'] for d in O.get('dream.lan-prebuilt64', [])}
c = sorted(set(a) & set(b)); cj = [i for i in c if jit(i)]
if len(c) >= 5: print('\ndream against itself, prebuilt and prebuilt64 (two sessions): %d designs, Spearman %.3f; within the %d JIT designs %.3f' % (len(c), sp([a[i] for i in c], [b[i] for i in c]), len(cj), sp([a[i] for i in cj], [b[i] for i in cj])))
