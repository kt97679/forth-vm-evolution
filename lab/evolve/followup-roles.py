#!/usr/bin/env python3
"""lab/evolve/followup-roles.py CANDIDATES SESSIONS --roles R [--handoff FILE] [--predictions N] - a follow-up chain's
roles (Iteration 615: results/drafts/followup-roles-611.py made general - its figures to the byte on 611's readings,
results/drafts/followup-rehearsal-615.sh). CANDIDATES: the chain's list (results/followup-seedN.md); SESSIONS: its
readings by session (chain-sessions.py's DEST, sK). R: the handoff's portable roles and their holders, role=id,... -
fastest (the best mean over the three classes), arm (the fastest on ARMv7), knee (x86-64 and x86-32), smallarm (small,
fast on ARMv7), memory (least memory), smallest; each holder must be in CANDIDATES. FILE names the handoff in the roles'
heading (default results/handoff-relf-611.md). Prints each line's completeness; the noise (a design's session-to-session
SD, a paired difference's SE); each role against its holder by the rule fixed before seed 87 (results/drafts/
portable-plan-602.md: speed 2%, binary + image 1%, memory 4 KB) - the designs that beat a holder listed, the trades the
chat's and the owner's; the predictions of iteration N (610: seed 87's follow-up, 614: seed 88's); dream against the laptop
by (factor, compiler). Pooled as final-pick.py pools: each source's geometric mean over its sessions; x86-64 and x86-32
the geometric mean of the laptop alone and dream, ARMv7 the Tegra; the mean of the three; errors paired by session (the
sessions both designs have). A design missing a class is left out of the classes, named.
611's run again: followup-roles.py results/followup-seed87.md results/chain-followup87 --handoff results/handoff-relf-601.md
  --predictions 610 --roles fastest=690981ca5b,arm=690981ca5b,knee=c2ef9488ff,smallarm=22420b3b61,memory=fb0d57c8a2,smallest=cea114f47e"""
import glob, json, math, os, statistics, sys

a = sys.argv[1:]
if len(a) < 2 or '--roles' not in a: sys.exit(__doc__)
opt = lambda n, d=None: a[a.index(n) + 1] if n in a else d
CAND, SESS = a[0], a[1]
R = dict(x.split('=', 1) for x in opt('--roles').split(','))
HAND, PRED = opt('--handoff', 'results/handoff-relf-611.md'), opt('--predictions')
SOURCES = ('laptop64', 'laptop32', 'laptop64-loaded', 'laptop32-loaded', 'dream64', 'dream32', 'rage')
HOSTFILE = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json',
            'rage': 'rage.lan-prebuiltarm.out.json'}
LAPKEY = {'laptop64': 'idle', 'laptop32': 'idle32', 'laptop64-loaded': 'loaded', 'laptop32-loaded': 'loaded32'}
PARTS = {'x86-64': ('laptop64', 'dream64'), 'x86-32': ('laptop32', 'dream32'), 'ARMv7': ('rage',)}
T, B, M = 0.02, 0.01, 4                      # speed 2%, binary + image 1%, memory 4 KB
gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)

C = {r['id']: r for r in (json.loads(l) for l in open(CAND) if l.startswith('{'))}
miss = sorted(set(i for i in R.values() if i not in C))
if miss: sys.exit('followup-roles: holders not in %s: %s' % (CAND, ' '.join(miss)))
NC = len(C)
S = {s: {i: {} for i in C} for s in SOURCES}            # source -> design -> {session: reading}, in session order
done = {s: [] for s in SOURCES}
for k, d in enumerate(sorted(glob.glob(os.path.join(SESS, 's[0-9]*')), key=lambda d: int(d.rsplit('s', 1)[1]))):
    lt = os.path.join(d, 'loadtest.md')
    if os.path.exists(lt):
        L = {}
        for l in open(lt, errors='replace'):
            if l.startswith('{"'):
                r = json.loads(l); L[r.get('id')] = r
        for s, key in LAPKEY.items():
            n = [i for i in C if L.get(i, {}).get(key)]
            for i in n: S[s][i][k] = L[i][key]
            done[s].append(len(n))
    for s, f in HOSTFILE.items():
        if os.path.exists(os.path.join(d, f)):
            o = json.load(open(os.path.join(d, f)))
            n = [x for x in o['designs'] if x.get('id') in C and not x.get('rejected') and x.get('speed_here')]
            for x in n: S[s][x['id']][k] = x['speed_here']
            done[s].append(len(n))
P = {s: {i: gm(list(v.values())) for i, v in S[s].items() if v} for s in SOURCES}
CL, gap = {}, []
for i in C:
    if not all(i in P[s] for p in PARTS.values() for s in p): gap.append(i); continue
    c = {k: gm([P[s][i] for s in p]) for k, p in PARTS.items()}
    c['mean'] = gm(list(c.values())); CL[i] = c
D = [i for i in C if i in CL]
lost = sorted(set(i for i in R.values() if i not in CL))
if lost: sys.exit('followup-roles: holders without a reading in every class: %s' % ' '.join(lost))
CH = {}                                              # role -> the run's designs that beat its holder by the rule


def paired(s, a, b):
    d = [math.log(S[s][a][k] / S[s][b][k]) for k in S[s][a] if k in S[s][b]]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))


def cdiff(k, a, b):
    ds = [paired(s, a, b) for s in PARTS[k]]
    return sum(x[0] for x in ds) / len(ds), math.sqrt(sum(x[1] ** 2 for x in ds)) / len(ds)


def mdiff(a, b):
    ds = [cdiff(k, a, b) for k in PARTS]
    return sum(x[0] for x in ds) / 3, math.sqrt(sum(x[1] ** 2 for x in ds)) / 3


run = lambda i: str(C[i].get('why', '')).startswith('the run')
print('## Completeness - sessions, and the fewest of the %d a session measured' % NC)
for s in SOURCES:
    if done[s]: print('  %-16s %2d sessions, each %d-%d of %d' % (s, len(done[s]), min(done[s]), max(done[s]), NC))
    else: print('  %-16s  0 sessions' % s)
if gap: print('  missing a class, left out of the classes: %s' % ' '.join(gap))

print('\n## Noise - a design\'s session-to-session SD (median over the %d), without and with each session\'s common shift' % NC)
ids = sorted(D)
for s in SOURCES:
    ks = [k for k in S[s][ids[0]] if all(k in S[s][i] for i in ids)] if ids else []
    n = len(ks)
    if n < 2: print('  %-16s %2d: too few sessions' % (s, n)); continue
    L = {i: [math.log(S[s][i][k]) for k in ks] for i in ids}
    sh = [statistics.median(L[i][k] - statistics.fmean(L[i]) for i in ids) for k in range(n)]
    raw = statistics.median(statistics.stdev(L[i]) for i in ids)
    adj = statistics.median(statistics.stdev([L[i][k] - sh[k] for k in range(n)]) for i in ids)
    t3 = max(1, n // 3)
    print('  %-16s %2d: SD %.2f%%, paired %.2f%%; a paired difference\'s SE %.2f%%; the shift\'s range %.2f%%, first '
          'third to last %+.2f%%' % (s, n, raw * 100, adj * 100, adj * math.sqrt(2 / n) * 100, (max(sh) - min(sh)) * 100,
                                     (statistics.fmean(sh[-t3:]) - statistics.fmean(sh[:t3])) * 100))

print('\n## The roles (%s) - speed 2%%, binary + image 1%%, memory 4 KB' % HAND)
inc = R['fastest']; bm = min(D, key=lambda i: CL[i]['mean']); m, se = mdiff(bm, inc)
print('  fastest portable (the best mean): %s %.4f against %s %.4f: %s +/- %.2f%%' % (bm, CL[bm]['mean'], inc,
                                                                                     CL[inc]['mean'], pct(m), se * 100))
if bm != inc and math.exp(m) - 1 <= -T and run(bm): CH.setdefault('fastest portable', []).append(bm)
for k in PARTS:
    m, se = cdiff(k, bm, inc)
    print('    %s %s %.4f, %s %.4f: %s +/- %.2f%%' % (k, bm, CL[bm][k], inc, CL[inc][k], pct(m), se * 100))
inc = R['arm']; arm = sorted(D, key=lambda i: CL[i]['ARMv7'])
print('  fastest on ARMv7: %s' % ', '.join('%s %.4f' % (i, CL[i]['ARMv7']) for i in arm[:5]))
for i in arm[:4]:
    if i != inc:
        m, se = cdiff('ARMv7', i, inc); print('    %s against %s: %s +/- %.2f%%' % (i, inc, pct(m), se * 100))
        if math.exp(m) - 1 <= -T and run(i): CH.setdefault('fastest on ARMv7', []).append(i)


def role(inc, keys, name):
    print('  %s - %s: %s, %s B, %d KB' % (name, inc, ', '.join('%s %.4f' % (k, CL[inc][k]) for k in keys),
                                          format(C[inc]['total'], ','), C[inc]['rss']))
    for i in sorted(D, key=lambda i: C[i]['total']):
        if i == inc: continue
        r = {k: CL[i][k] / CL[inc][k] - 1 for k in keys}; r['bytes'] = C[i]['total'] / C[inc]['total'] - 1
        th = dict({k: T for k in keys}, bytes=B)
        if any(r[k] <= -th[k] for k in r) and all(r[k] < th[k] for k in r):
            print('    %s: %s, memory %+d KB' % (i, ', '.join('%s %+.2f%%' % (k, v * 100) for k, v in r.items()),
                                                C[i]['rss'] - C[inc]['rss']))
            if run(i): CH.setdefault(name, []).append(i)


role(R['knee'], ('x86-64', 'x86-32'), 'the knee')
role(R['smallarm'], ('ARMv7',), 'small, fast on ARMv7')
inc = R['memory']; lm = [i for i in sorted(C, key=lambda i: C[i]['rss']) if i != inc]
print('  least memory - %s %d KB; the next %s' % (inc, C[inc]['rss'], ', '.join('%s %d KB' % (i, C[i]['rss']) for i in lm[:2])))
CH.update({'least memory': [i for i in lm if C[i]['rss'] <= C[inc]['rss'] - M and run(i)]} if any(
    C[i]['rss'] <= C[inc]['rss'] - M and run(i) for i in lm) else {})
inc = R['smallest']
print('  smallest - %s %s B; smaller:' % (inc, format(C[inc]['total'], ',')))
for i in sorted(D, key=lambda i: C[i]['total']):
    if C[i]['total'] >= C[inc]['total']: break
    print('    %s %s B (%+.2f%%): %s, memory %+d KB' % (i, format(C[i]['total'], ','),
          (C[i]['total'] / C[inc]['total'] - 1) * 100,
          ', '.join('%s %s +/- %.2f%%' % ((k,) + (lambda d: (pct(d[0]), d[1] * 100))(cdiff(k, i, inc))) for k in PARTS),
          C[i]['rss'] - C[inc]['rss']))
    if run(i): CH.setdefault('smallest', []).append(i)

if PRED == '610':
    print('\n## The predictions of Iteration 610')
    print('  (1) the Tegra %d sessions, each %d of 45' % (len(done['rage']), min(done['rage'])))
    rn = [i for i in C if C[i]['why'].startswith('the run')]
    for f, w in ((min(rn, key=lambda i: C[i]['speed']), 'in-run, named "the run - fastest"'),
                 (min(rn, key=lambda i: P['laptop64'][i]), 're-measured')):
        m, se = paired('laptop64', f, '8cc7f60d6b')
        print('  (2) the run\'s fastest (%s) %s against 8cc7f60d6b, the laptop alone: %s +/- %.2f%%' % (w, f, pct(m), se * 100))
    m, se = cdiff('ARMv7', '3452cb633b', '690981ca5b')
    print('  (4) ARMv7 3452cb633b against 690981ca5b: %s +/- %.2f%%' % (pct(m), se * 100))
elif PRED == '614':
    print('\n## The predictions of Iteration 614')
    print('  (1) %s' % '; '.join('%s %d sessions, each %d-%d of %d' % (s, len(done[s]), min(done[s] or [0]),
                                                                       max(done[s] or [0]), NC) for s in SOURCES[:2] + SOURCES[4:]))
    print('  (2) the run\'s designs beating a holder by the rule: %s' % ('; '.join('%s %s' % (k, ' '.join(v)) for k, v in CH.items()) or 'none'))
    rn = [i for i in D if run(i)]; br = min(rn, key=lambda i: CL[i]['mean']); m, se = mdiff(br, R['fastest'])
    print('  (3) the run\'s best mean %s %.4f against %s %.4f: %s +/- %.2f%%' % (br, CL[br]['mean'], R['fastest'],
                                                                              CL[R['fastest']]['mean'], pct(m), se * 100))
    c = 'c7814def6d'
    print('  (4) %s dream/laptop at 4-byte cells %.3f (the bar 1.36)' % (c, P['dream32'][c] / P['laptop32'][c])
          if c in P['dream32'] and c in P['laptop32'] else '  (4) %s not measured on both' % c)

print('\n## dream against the laptop by (factor, compiler) - the median of dream/laptop at 4-byte and 8-byte cells, and '
      'the Tegra/laptop at 4')
g = {}
for i in D:
    k = (C[i]['genome']['factor'], C[i]['genome']['compiler'])
    g.setdefault(k, []).append((P['dream32'][i] / P['laptop32'][i], P['dream64'][i] / P['laptop64'][i],
                                P['rage'][i] / P['laptop32'][i]))
for k in sorted(g):
    print('  factor %d, compiler %d: %2d designs, %.3f %.3f %.3f' % (k + (len(g[k]),) + tuple(
        statistics.median(x[j] for x in g[k]) for j in range(3))))
x = [y for v in g.values() for y in v]
print('  all %d: %.3f %.3f %.3f' % ((len(x),) + tuple(statistics.median(y[j] for y in x) for j in range(3))))
