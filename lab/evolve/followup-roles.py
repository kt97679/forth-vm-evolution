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
--gain (Iteration 616): instead, the rule fixed before seed 88's follow-up returned (results/drafts/portable-plan-602.md,
"After the follow-up") - the run's designs against the best of those found before, re-measured: the laptop alone at each
width, each class and the mean of the three (2%, the paired difference 2 SE or more), binary + image (1%) and memory
(4 KB), exact; the run's designs beating a role's holder; the verdict - another portable run, or the search stops.
--screen (Iteration 617): instead, the screen the next portable run's remote lines measured (portable-followup.py --rest):
each of the run's designs against each speed role's holder on that role's lines, paired by session, flagged by the role's
own rule with dream standing in for the laptop - the fastest portable: the mean over dream at both widths and the Tegra
below the holder's; the fastest on ARMv7: faster on the Tegra; the knee (dream at both widths) and small and fast on ARMv7
(the Tegra): faster on a line or 1% smaller, and no line 4% slower (one machine stands in for two) nor 1% larger. Any gain
counts, so the screen is loose; the flagged join that run's follow-up list (--flagged OUT writes their records for
portable-followup.py --also), where the role's rule decides. On 611's readings with 601's holders it flags the two designs
611 gave roles, 782f3ad7ff first. JIT designs (the JIT expressed) are left out of it (630: seed 89's rest held 82 - a
JIT run's rest, screened for the portable roles).
--roles also takes the x86 roles (Iteration 622, the JIT run's follow-up - results/drafts/jit-run-plan-620.md): fast64 (the
fastest on x86-64), fast32 (on x86-32), allround (the best mean), smalljit (the smallest JIT design), over every design with
the class; the six portable roles then over the JIT-free designs alone (a record's "jit", portable-followup.py --jit), a
design missing a class kept in the classes it has; a screened design (why: flagged by the screen) a portable role's
candidate as the run's are. Rehearsed: results/drafts/jit-rehearsal-622.py.
611's run again: followup-roles.py results/followup-seed87.md results/chain-followup87 --handoff results/handoff-relf-601.md
  --predictions 610 --roles fastest=690981ca5b,arm=690981ca5b,knee=c2ef9488ff,smallarm=22420b3b61,memory=fb0d57c8a2,smallest=cea114f47e"""
import glob, io, json, math, os, re, statistics, sys

a = sys.argv[1:]
if len(a) < 2 or '--roles' not in a: sys.exit(__doc__)
opt = lambda n, d=None: a[a.index(n) + 1] if n in a else d
CAND, SESS = a[0], a[1]
R = dict(x.split('=', 1) for x in opt('--roles').split(','))
HAND, PRED = opt('--handoff', 'results/handoff-relf-611.md'), opt('--predictions')
GAIN, OUT0 = '--gain' in a, sys.stdout
if GAIN: sys.stdout = io.StringIO()          # 616: every section computed, the rule's alone printed
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
jit = lambda i: bool(C[i].get('jit'))                # 622: the JIT run's follow-up marks its JIT designs
XK = {'fast64': 'x86-64', 'fast32': 'x86-32', 'allround': 'mean'}
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
            # 637: a listed design's reading counts however the line came to measure it - seed 91's Tegra line drew
            # 7fb40ff7ba into its rejected sample and so did not ask for it again; dropped, the screen missed its flag
            n = [x for x in o['designs'] if x.get('id') in C and x.get('speed_here')]
            for x in n: S[s][x['id']][k] = x['speed_here']
            done[s].append(len(n))
P = {s: {i: gm(list(v.values())) for i, v in S[s].items() if v} for s in SOURCES}
if '--screen' in a:                                   # 617: the screen (results/drafts/portable-plan-602.md, "After the follow-up")
    sys.stdout = OUT0
    def pd(s, x, y):
        d = [math.log(S[s][x][k] / S[s][y][k]) for k in S[s][x] if k in S[s][y]]
        return (statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d)) if len(d) > 1 else float('nan'), len(d)) if d else None
    SRC = {'fastest': ('dream64', 'dream32', 'rage'), 'arm': ('rage',), 'knee': ('dream64', 'dream32'), 'smallarm': ('rage',)}
    sys.argv = ['x']; import evolve as E               # 630: a portable role's candidate is JIT-free (622) - in the screen too
    rn = [i for i in C if str(C[i].get('why', '')).startswith('the run')]
    xj = [i for i in rn if E.express(E.canon(C[i]['genome'])).get('jit')]; rn = [i for i in rn if i not in xj]
    print('## The screen - the run\'s %d against each speed role\'s holder, the remote lines (the rule of Iterations 616-617)%s'
          % (len(rn), '; %d JIT designs left out (a portable role\'s candidate is JIT-free - 622, 630)' % len(xj) if xj else ''))
    for x in ('dream64', 'dream32', 'rage'):
        print('  %-8s %2d sessions, each %d-%d of %d' % (x, len(done[x]), min(done[x] or [0]), max(done[x] or [0]), NC))
    flag = {}
    for role, src in SRC.items():
        h = R.get(role)
        if not h: continue
        hits = []
        for i in rn:
            if i == h: continue
            r = [pd(x, i, h) for x in src]
            if any(t is None for t in r): continue
            if role == 'fastest':            # the best mean: dream standing in for the laptop's x86 classes, the Tegra for ARMv7
                m = sum(t[0] for t in r) / len(r); ok = m < 0; why = 'the mean of %s %s' % ('+'.join(src), pct(m))
            elif role == 'arm':
                m = r[0][0]; ok = m < 0; why = 'rage %s +/- %.2f%%' % (pct(m), r[0][1] * 100)
            else:                            # the knee, small and fast on ARMv7: the role's rule, any speed gain counted
                b = C[i]['total'] / C[h]['total'] - 1; m = min(t[0] for t in r)
                ok = (m < 0 or b <= -B) and all(math.exp(t[0]) - 1 < 2 * T for t in r) and b < B
                why = '%s, bytes %+.2f%%' % (', '.join('%s %s' % (x, pct(t[0])) for x, t in zip(src, r)), b * 100)
            if ok: hits.append((m, i, why))
        hits.sort()
        print('  %s - %s: %d%s' % (role, h, len(hits), ''.join('\n    %s %s' % (i, w) for m, i, w in hits[:12])
                                  + ('\n    ... %d more' % (len(hits) - 12) if len(hits) > 12 else '')))
        for m, i, w in hits: flag.setdefault(i, []).append(role)
    print('flagged: %d - they join the follow-up\'s list%s' % (len(flag), (': ' + ' '.join(sorted(flag))) if flag else ''))
    if opt('--flagged'):
        with open(opt('--flagged'), 'w') as o:
            o.write('# The screen\'s flagged (lab/evolve/followup-roles.py --screen, Iteration 617), for the next follow-up\'s list\n\n')
            for i in sorted(flag): o.write(json.dumps(dict({k: C[i][k] for k in C[i] if k != 'why'}, why='found before - flagged by the screen (%s)' % ', '.join(flag[i])), sort_keys=True) + '\n')
    sys.exit(0)
CL, gap = {}, []
for i in C:                                          # 622: a design missing a class kept in the classes it has
    c = {k: gm([P[s][i] for s in p]) for k, p in PARTS.items() if all(i in P[s] for s in p)}
    if len(c) < len(PARTS): gap.append(i)
    if len(c) == len(PARTS): c['mean'] = gm(list(c.values()))
    if c: CL[i] = c
D = [i for i in C if 'mean' in CL.get(i, {})]
PD = [i for i in D if not jit(i)]                    # 622: the portable roles over the JIT-free designs
lost = sorted(set(i for r, i in R.items() if (XK[r] not in CL.get(i, {}) if r in XK else i not in CL if r == 'smalljit' else i not in D)))
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


run = lambda i: str(C[i].get('why', '')).startswith(('the run', 'the check'))   # 641: the final check's never-measured, candidates as a run's
cand = lambda i: run(i) or 'flagged by the screen' in str(C[i].get('why', ''))   # 622: a screened design a portable role's candidate
print('## Completeness - sessions, and the fewest of the %d a session measured' % NC)
for s in SOURCES:
    if done[s]: print('  %-16s %2d sessions, each %d-%d of %d' % (s, len(done[s]), min(done[s]), max(done[s]), NC))
    else: print('  %-16s  0 sessions' % s)
if gap: print('  missing a class, left out of the mean and the portable roles: %s' % ' '.join(gap))

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
inc = R['fastest']; bm = min(PD, key=lambda i: CL[i]['mean']); m, se = mdiff(bm, inc)
print('  fastest portable (the best mean): %s %.4f against %s %.4f: %s +/- %.2f%%' % (bm, CL[bm]['mean'], inc,
                                                                                     CL[inc]['mean'], pct(m), se * 100))
if bm != inc and math.exp(m) - 1 <= -T and cand(bm): CH.setdefault('fastest portable', []).append(bm)
for k in PARTS:
    m, se = cdiff(k, bm, inc)
    print('    %s %s %.4f, %s %.4f: %s +/- %.2f%%' % (k, bm, CL[bm][k], inc, CL[inc][k], pct(m), se * 100))
inc = R['arm']; arm = sorted(PD, key=lambda i: CL[i]['ARMv7'])
print('  fastest on ARMv7: %s' % ', '.join('%s %.4f' % (i, CL[i]['ARMv7']) for i in arm[:5]))
for i in arm[:4]:
    if i != inc:
        m, se = cdiff('ARMv7', i, inc); print('    %s against %s: %s +/- %.2f%%' % (i, inc, pct(m), se * 100))
        if math.exp(m) - 1 <= -T and cand(i): CH.setdefault('fastest on ARMv7', []).append(i)


def role(inc, keys, name):
    print('  %s - %s: %s, %s B, %d KB' % (name, inc, ', '.join('%s %.4f' % (k, CL[inc][k]) for k in keys),
                                          format(C[inc]['total'], ','), C[inc]['rss']))
    for i in sorted(PD, key=lambda i: C[i]['total']):
        if i == inc: continue
        r = {k: CL[i][k] / CL[inc][k] - 1 for k in keys}; r['bytes'] = C[i]['total'] / C[inc]['total'] - 1
        th = dict({k: T for k in keys}, bytes=B)
        if any(r[k] <= -th[k] for k in r) and all(r[k] < th[k] for k in r):
            print('    %s: %s, memory %+d KB' % (i, ', '.join('%s %+.2f%%' % (k, v * 100) for k, v in r.items()),
                                                C[i]['rss'] - C[inc]['rss']))
            if cand(i): CH.setdefault(name, []).append(i)


role(R['knee'], ('x86-64', 'x86-32'), 'the knee')
role(R['smallarm'], ('ARMv7',), 'small, fast on ARMv7')
inc = R['memory']; lm = [i for i in sorted(C, key=lambda i: C[i]['rss']) if i != inc and not jit(i)]
print('  least memory - %s %d KB; the next %s' % (inc, C[inc]['rss'], ', '.join('%s %d KB' % (i, C[i]['rss']) for i in lm[:2])))
CH.update({'least memory': [i for i in lm if C[i]['rss'] <= C[inc]['rss'] - M and cand(i)]} if any(
    C[i]['rss'] <= C[inc]['rss'] - M and cand(i) for i in lm) else {})
inc = R['smallest']
print('  smallest - %s %s B; smaller:' % (inc, format(C[inc]['total'], ',')))
for i in sorted(PD, key=lambda i: C[i]['total']):
    if C[i]['total'] >= C[inc]['total']: break
    print('    %s %s B (%+.2f%%): %s, memory %+d KB' % (i, format(C[i]['total'], ','),
          (C[i]['total'] / C[inc]['total'] - 1) * 100,
          ', '.join('%s %s +/- %.2f%%' % ((k,) + (lambda d: (pct(d[0]), d[1] * 100))(cdiff(k, i, inc))) for k in PARTS),
          C[i]['rss'] - C[inc]['rss']))
    if cand(i): CH.setdefault('smallest', []).append(i)
for key, name in (('fast64', 'fastest on x86-64'), ('fast32', 'fastest on x86-32'), ('allround', 'best all-round (the best mean)')):
    inc = R.get(key)                                 # 622: the x86 roles, over every design with the class
    if not inc: continue
    k = XK[key]; xs = sorted((i for i in CL if k in CL[i]), key=lambda i: CL[i][k])
    print('  %s: %s' % (name, ', '.join('%s %.4f' % (i, CL[i][k]) for i in xs[:5])))
    for i in xs[:4]:
        if i == inc: continue
        m, se = mdiff(i, inc) if k == 'mean' else cdiff(k, i, inc)
        print('    %s against %s: %s +/- %.2f%%' % (i, inc, pct(m), se * 100))
        if math.exp(m) - 1 <= -T and run(i): CH.setdefault(name, []).append(i)
inc = R.get('smalljit')
if inc:
    print('  the smallest JIT design - %s %s B; smaller JIT designs:' % (inc, format(C[inc]['total'], ',')))
    for i in sorted((i for i in C if jit(i)), key=lambda i: C[i]['total']):
        if C[i]['total'] >= C[inc]['total']: break
        ks = [k for k in PARTS if k in CL.get(i, {}) and k in CL.get(inc, {})]
        print('    %s %s B (%+.2f%%): %s, memory %+d KB' % (i, format(C[i]['total'], ','), (C[i]['total'] / C[inc]['total'] - 1) * 100,
              ', '.join('%s %s +/- %.2f%%' % ((k,) + (lambda d: (pct(d[0]), d[1] * 100))(cdiff(k, i, inc))) for k in ks) or 'no class in common',
              C[i]['rss'] - C[inc]['rss']))
        if run(i): CH.setdefault('the smallest JIT design', []).append(i)

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


def gain():
    """616: the rule of results/drafts/portable-plan-602.md, "After the follow-up" - a gain is a design of the run beating the
    best of those found before by the stopping rule's thresholds, re-measured"""
    sys.stdout = OUT0
    rn = [i for i in C if run(i)]; fb = [i for i in C if str(C[i].get('why', '')).startswith('found before')]
    print('## The run against the best found before, re-measured - the rule of Iteration 616 (results/drafts/portable-plan-602.md)')
    if not rn or not fb: print('verdict: none - the list has %d of the run\'s and %d found before' % (len(rn), len(fb))); return
    got = []

    def speed(name, key, f):
        r = [i for i in rn if key(i) is not None]; b = [i for i in fb if key(i) is not None]
        if not r or not b: print('  %s: not measured on both' % name); return
        x, y = min(r, key=key), min(b, key=key); m, se = f(x, y)
        g = math.exp(m) - 1 <= -T and (m <= -2 * se if se else m < 0)
        print('  %s: the run\'s %s %.4f, found before %s %.4f: %s +/- %.2f%% - %s' % (name, x, key(x), y, key(y), pct(m), se * 100,
                                                                                  'GAIN' if g else 'no'))
        if g: got.append(name)
    for s, w in (('laptop64', '8-byte'), ('laptop32', '4-byte')):
        speed('the laptop alone, %s cells' % w, lambda i, s=s: P[s].get(i), lambda x, y, s=s: paired(s, x, y))
    for k in PARTS:
        speed(k, lambda i, k=k: CL.get(i, {}).get(k), lambda x, y, k=k: cdiff(k, x, y))
    speed('the mean of the three', lambda i: CL.get(i, {}).get('mean'), mdiff)
    x, y = min(rn, key=lambda i: C[i]['total']), min(fb, key=lambda i: C[i]['total']); d = C[x]['total'] / C[y]['total'] - 1
    print('  binary + image: the run\'s %s %s B, found before %s %s B: %+.2f%% - %s' % (x, format(C[x]['total'], ','), y,
          format(C[y]['total'], ','), d * 100, 'GAIN' if d <= -B else 'no'))
    if d <= -B: got.append('binary + image')
    x, y = min(rn, key=lambda i: C[i]['rss']), min(fb, key=lambda i: C[i]['rss']); d = C[x]['rss'] - C[y]['rss']
    print('  memory: the run\'s %s %d KB, found before %s %d KB: %+d KB - %s' % (x, C[x]['rss'], y, C[y]['rss'], d, 'GAIN' if d <= -M else 'no'))
    if d <= -M: got.append('memory')
    print('  the roles: the run\'s designs beating a holder by the rule - %s' % ('; '.join('%s %s' % (k, ' '.join(v)) for k, v in CH.items())
                                                                              or 'none'))
    n = re.search(r'seed(\d+)', os.path.basename(CAND)); nxt = 'seed %d' % (int(n.group(1)) + 1) if n else 'the next portable run'
    if any(jit(i) for i in C):                       # 622: the JIT run's follow-up (results/drafts/jit-run-plan-620.md)
        nxt = nxt if n else 'the next JIT run'
        if got: print('verdict: a gain confirmed (%s) - another JIT run, %s' % (', '.join(got), nxt))
        elif CH: print('verdict: no extreme gained; role candidates above - another JIT run, %s, if an x86 role goes to one of the '
                       'run\'s; the portable search reopened if a portable role goes to a screened design (the processing decides); '
                       'else the JIT roles final' % nxt)
        else: print('verdict: none confirmed - the JIT roles final, the freeze next')
        return
    if got: print('verdict: a gain confirmed (%s) - another portable run, %s' % (', '.join(got), nxt))
    elif CH: print('verdict: no extreme gained; role candidates above - another portable run, %s, if a role goes to one of them (the '
                   'processing decides), else the portable search stops' % nxt)
    else: print('verdict: none confirmed - the portable search stops')


if GAIN: gain()
