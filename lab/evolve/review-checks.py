#!/usr/bin/env python3
"""review-checks.py CHECK ARGS - the figures of the methodology review (Iteration 386,
results/review-methodology-386.md), each reproducible:

  pedigree DB RESULTS.md   each front design's expected share from every generation-0 design (every listed
                           parent weighted equally - an approximation), summed by kind of ancestor, by thirds
                           of the front by 64-bit speed: does a "from scratch" run descend from evolved founders?
  curse RESULTS.md         re-measured / in-run speed by in-run rank (winner's curse), and the held-out
                           Spearman over the whole front against its fastest third and tenth
  cpus COMPARE.md N        session N's verdict measures (fastest, best Q, against all the other runs) computed
                           from each CPU alone - how far one CPU's noise moves them - and the front membership
                           agreement between the two CPUs in every session that printed it
  progress DB              is the search stuck? (Iteration 392, the owner's worry of a local minimum) - by
                           generation: the best speed and the smallest binary + image so far (size exact, so a
                           late gain in it is no noise), the generations of the last gains, and diversity - the
                           mean share of genes two designs of a generation differ in, and the encodings alive
  spread DB[@G] DB[@G] ... runs from one start compared at one generation (Iteration 393: the replicates of the
                           owner's local-minimum question) - each database cut at generation G (default: the
                           earliest last generation of them all), its front's fastest, smallest, least memory,
                           best Q and hypervolume (log space, one reference for all), and how far apart their
                           fronts' gene usage lies (the mean difference in points, every built gene)
  verdicts COMPARE.md      every session's verdict (Iteration 188's five measures) rebuilt from its own tables -
                           checked against the printed one - then from each CPU alone: does "small" depend on
                           which CPU is asked? (Iteration 388) - and from both, each design's speed the
                           geometric mean of its two: the owner's rule from Iteration 389
  fail32 DB                the run's 32-bit failures by cause (Iteration 427: seed 61's, classed by hand at 425) -
                           died on the corpus with bfind and no tos, or no engine from the tail engine (by
                           compiler), the causes the after-seed-62 batch fixes (from seed 63 on, any is a
                           regression); anything else by its message, "not a known cause" - look
  generic REMOTE_DIR       the best design across the machine classes (Iteration 430; GOALS.md, Iteration 377): a
                           chain's remote checks (CHAIN/remote), the designs measured on x86-64, 32-bit x86 and
                           ARMv7 - each class once, prebuilt64 for x86-64 where there is one - ranked by the
                           geometric mean of their speeds against s6 there; vetoed: more than 25% behind the
                           class's best of them (GOALS.md's margin)
  votes RESULTS.md [--seed N] [--at COMMIT] [--ledger FILE [--append]]
                           the gene votes (Iteration 432; results/seed63-rules.md): for each gene, the run's
                           votes for its removal - on under 10% of the front, on no design of its fastest tenth,
                           of its smallest, of its best-Q tenth - and with a ledger (results/gene-votes.md) the
                           tally over the last three runs: a keep vote when it was in any such tenth; a
                           candidate at 11 of 12 votes and no keep vote. --append adds the run to the ledger
  rules RESULTS.md [--db DB] [--ledger FILE] [--seed N]
                           results/seed63-rules.md's ten rules, measured (Iteration 438): one line each - what
                           was measured, the rule, and PASS, ATTENTION (the rule's "then" applies), PROPOSE,
                           NOTED or SEE (another step of the routine reads it); --db for the reach limit and the
                           32-bit failures, --ledger (results/gene-votes.md) for the genes' three-run tallies
  screen DB RESULTS.md     the surrogate screen's audit: screened children measured anyway that reached the
                           final front, against the base rate; the tag-2 share screened and not
"""
import collections, json, os, re, sys
if len(sys.argv) < 3: sys.exit(__doc__)
sys.setrecursionlimit(100000)

def db(path):
    R = {}
    for l in open(path):
        try: d = json.loads(l)
        except ValueError: continue
        R[d['id']] = d
    return R

def front_rows(path):
    """the report's front table: id, speed, 32-bit speed, re-measured, sieve (held out)"""
    rows = []
    for l in open(path):
        f = [x.strip() for x in l.split('|')]
        if len(f) > 10 and re.fullmatch(r'[0-9a-f]{10}', f[1] or ''):
            try: rows.append(dict(id=f[1], sp=float(f[2]), s32=float(f[3]), rem=float(f[4]), sieve=float(f[9])))
            except ValueError: pass
    return rows

def spearman(a, b):
    def ranks(v):
        r = [0] * len(v)
        for k, i in enumerate(sorted(range(len(v)), key=lambda i: v[i])): r[i] = k
        return r
    ra, rb = ranks(a), ranks(b); m = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (m * (m * m - 1))

def thirds(rows):
    n = len(rows); return (('fastest third', rows[:n // 3]), ('middle third', rows[n // 3:2 * n // 3]), ('slowest third', rows[2 * n // 3:]))

check = sys.argv[1]
if check == 'pedigree':
    R = db(sys.argv[2]); rows = sorted(front_rows(sys.argv[3]), key=lambda r: r['sp'])
    kind = {}
    for i, d in R.items():
        if d.get('parents'): continue
        h = str(d.get('how', ''))
        kind[i] = ("seed 37's fastest" if '38446e6c09' in h else "seed 40's knee" if 'd99e3d9ed9' in h else
                   'hand-made' if h.startswith('hand-made') else 'founder from s4/s6' if h.startswith('founder') else 'random or seeded')
    memo = {}
    def share(i):
        if i not in memo:
            ps = [p for p in (R[i].get('parents') or []) if p in R]
            if not ps: memo[i] = {kind.get(i, 'random or seeded'): 1.0}
            else:
                c = collections.Counter()
                for p in ps:
                    for k, v in share(p).items(): c[k] += v / len(ps)
                memo[i] = dict(c)
        return memo[i]
    full = {i[:10]: i for i in R}
    print('generation 0: %d designs - %s' % (len(kind), dict(collections.Counter(kind.values()))))
    keys = ["seed 37's fastest", "seed 40's knee", 'founder from s4/s6', 'hand-made', 'random or seeded']
    print('| front, by 64-bit speed | ' + ' | '.join(keys) + ' |\n|---|' + '---|' * len(keys))
    for name, part in thirds(rows):
        t = collections.Counter()
        for r in part:
            for k, v in share(full[r['id']]).items(): t[k] += v / len(part)
        print('| %s (%d) | ' % (name, len(part)) + ' | '.join('%.1f%%' % (100 * t[k]) for k in keys) + ' |')
elif check == 'curse':
    rows = sorted(front_rows(sys.argv[2]), key=lambda r: r['sp']); n = len(rows)
    print('re-measured / in-run speed (above 1: the in-run number was lucky), by in-run rank:')
    for name, part in (('fastest tenth', rows[:n // 10]),) + thirds(rows):
        r = sorted(x['rem'] / x['sp'] for x in part)
        print('  %-14s %3d designs: median %.3f, range %.3f-%.3f' % (name, len(part), r[len(r) // 2], r[0], r[-1]))
    print('held out (sieve), Spearman with the selection speed:')
    for name, part in (('whole front', rows), ('fastest third', rows[:n // 3]), ('fastest tenth', rows[:n // 10])):
        print('  %-14s %3d designs: %.3f' % (name, len(part), spearman([r['sp'] for r in part], [r['sieve'] for r in part])))
elif check == 'cpus':
    S = open(sys.argv[2]).read()
    print('front of all runs, the two CPUs\' members in common, each session that printed it:')
    for m in re.finditer(r'^On both fronts: (\d+) of (\d+) and (\d+)\.', S, re.M):
        a, b, c = map(int, m.groups()); print('  %d of %d and %d - %.0f%% and %.0f%%' % (a, b, c, 100 * a / b, 100 * a / c))
    S = S[S.index('## Session %s ' % sys.argv[3]):]; S = S[:S.index('\n## Session ', 10)] if '\n## Session ' in S[10:] else S
    main = {}
    for l in S.split('\n'):
        f = [x.strip() for x in l.split('|')]
        if len(f) > 10 and 'db.jsonl' in f[1] and re.fullmatch(r'[0-9a-f]{10}', f[2]):
            main[f[2]] = (f[1].split(':')[0], int(f[8].replace(',', '')), float(f[9]))
    cpu = {}
    for l in S[S.index('| design | speed cpu 2 | speed cpu 8 | ratio |'):].split('\n')[2:]:
        f = [x.strip() for x in l.split('|')]
        if len(f) < 5 or not re.fullmatch(r'[0-9a-f]{10}', f[1] or ''): break
        cpu[f[1]] = (float(f[2]), float(f[3]))
    runs = sorted({v[0] for v in main.values()})
    def ms(c):
        return {r: (min(cpu[d][c] for d in main if main[d][0] == r and d in cpu),
                    min(main[d][1] * cpu[d][c] * main[d][2] for d in main if main[d][0] == r and d in cpu)) for r in runs}
    m = (ms(0), ms(1))
    print('session %s, %d designs on both CPUs; against all the other runs, + the run ahead (as the verdict reads):' % (sys.argv[3], len(set(cpu) & set(main))))
    print('| run | fastest, cpu 2 / cpu 8 | best Q, cpu 2 / cpu 8 |\n|---|---|---|')
    for r in runs:
        cell = lambda k: ' / '.join('%+.1f%%' % (100 * (min(x[o][k] for o in runs if o != r) / x[r][k] - 1)) for x in m)
        print('| %s | %s | %s |' % (r, cell(0), cell(1)))
elif check == 'screen':
    R = db(sys.argv[2]); front = {r['id'] for r in front_rows(sys.argv[3])}
    kids = [d for d in R.values() if d.get('parents')]
    aud = [d for d in kids if 'screened, audited' in str(d.get('how', ''))]
    meas = [d for d in kids if d.get('status') != 'screened' and d not in aud]
    on = lambda ds: sum(1 for d in ds if d['id'][:10] in front)
    print('screened and not measured: %d; screened and audited (measured anyway): %d' % (sum(1 for d in kids if d.get('status') == 'screened'), len(aud)))
    print('reached the final front: audited %d of %d; other measured children %d of %d (%.2f%%) - %.1f expected among the audited at that rate'
          % (on(aud), len(aud), on(meas), len(meas), 100 * on(meas) / len(meas), len(aud) * on(meas) / len(meas)))
    t2 = lambda ds: 100 * sum(1 for d in ds if (d.get('genome') or {}).get('tag2')) / max(1, len(ds))
    print('tag-2 share: screened (status or audited) %.1f%%, measured unscreened %.1f%%' % (t2([d for d in kids if d.get('status') == 'screened'] + aud), t2(meas)))
elif check == 'verdicts':
    import math
    import numpy as np
    def hv(pts, lo, ref, n=100000):     # compare-fronts.py's _hv, its numpy path, verbatim
        P = [p for p in pts if not any(all(q[k] <= p[k] for k in range(3)) and q != p for q in pts)]
        rng = np.random.default_rng(1); S = np.asarray(lo) + rng.random((n, 3)) * (np.asarray(ref) - np.asarray(lo))
        hit = np.zeros(n, bool)
        for p in P: hit |= (S >= np.asarray(p)).all(axis=1)
        return hit.mean()
    def measures(main, speed):
        ids = [d for d in main if d in speed]
        lp = {d: (math.log(speed[d]), math.log(main[d][1]), math.log(main[d][2])) for d in ids}
        lo = tuple(min(v[k] for v in lp.values()) for k in range(3)); ref = tuple(max(v[k] for v in lp.values()) + 0.05 for k in range(3))
        out = {}
        for r in sorted({main[d][0] for d in ids}):
            mine = [d for d in ids if main[d][0] == r]; rest = [d for d in ids if main[d][0] != r]
            q = lambda d: speed[d] * main[d][1] * main[d][2]
            fg = min(speed[d] for d in rest) / min(speed[d] for d in mine) - 1
            sg = min(main[d][1] for d in rest) / min(main[d][1] for d in mine) - 1
            mg = min(main[d][2] for d in rest) - min(main[d][2] for d in mine)
            h0 = hv([lp[d] for d in rest], lo, ref); hg = hv([lp[d] for d in rest + mine], lo, ref) / h0 - 1
            qg = min(map(q, rest)) / min(map(q, mine)) - 1
            out[r] = (fg, sg, mg, hg, qg, fg < .05 and sg < .02 and mg < 8 and hg < .02 and qg < .02)
        return out
    fmt = lambda m: '%+.1f%% %+.2f%% %+d KB %+.1f%% %+.1f%%' % (100 * m[0], 100 * m[1], m[2], 100 * m[3], 100 * m[4])
    word = lambda b: 'small' if b else 'not small'
    rows = []
    for sec in re.split(r'(?m)^(?=## Session \d+ )', open(sys.argv[2]).read()):
        m = re.match(r'## Session (\d+) - Iteration (\d+)', sec)
        if not m or '## Judging the runs' not in sec or '| design | speed cpu 2 | speed cpu 8 | ratio |' not in sec: continue
        L = sec.split('\n')
        h = next(k for k, l in enumerate(L) if l.startswith('| run | design | speed now'))
        hd = [x.strip() for x in L[h].split('|')]; ci = {c: hd.index(c) for c in ('run', 'design', 'speed now', 'binary + image', 'memory KB')}
        main, now = {}, {}
        for l in L[h + 2:]:
            if not l.startswith('|'): break
            f = [x.strip() for x in l.split('|')]
            if 'db.jsonl' not in f[ci['run']]: continue
            try:
                main[f[ci['design']]] = (f[ci['run']].split(':')[0], int(f[ci['binary + image']].replace(',', '')), float(f[ci['memory KB']]))
                now[f[ci['design']]] = float(f[ci['speed now']])
            except ValueError: pass
        k0 = next(k for k, l in enumerate(L) if l.startswith('| design | speed cpu 2 | speed cpu 8 | ratio |')); c2, c8 = {}, {}
        for l in L[k0 + 2:]:
            f = [x.strip() for x in l.split('|')]
            if len(f) < 5 or not re.fullmatch(r'[0-9a-f]{10}', f[1] or ''): break
            c2[f[1]], c8[f[1]] = float(f[2]), float(f[3])
        j0 = next(k for k, l in enumerate(L) if l.startswith('| run | fastest | smallest | memory | hypervolume | best Q | verdict |'))
        pr = next(([x.strip() for x in l.split('|')] for l in L[j0 + 2:] if l.startswith('| this clone')), None)
        if not pr or 'this clone' not in {v[0] for v in main.values()}: continue
        a, b2, b8, bb = (measures(main, sp)['this clone'] for sp in (now, c2, c8, {d: math.sqrt(c2[d] * c8[d]) for d in c2 if d in c8}))
        rows.append((int(m.group(1)), int(m.group(2)), pr[7], a, b2, b8, len(main), len(set(c2) & set(main)), bb))
        print('session %s (Iteration %s), %d designs, %d on both CPUs' % (m.group(1), m.group(2), len(main), len(set(c2) & set(main))))
        print('  printed      %s  %s' % ('  '.join(pr[2:7]), pr[7]))
        print('  rebuilt      %s  %s' % (fmt(a), word(a[5])))
        print('  cpu 2 alone  %s  %s' % (fmt(b2), word(b2[5])))
        print('  cpu 8 alone  %s  %s' % (fmt(b8), word(b8[5])))
        print('  both CPUs    %s  %s' % (fmt(bb), word(bb[5])), flush=True)
    print('\n| session | iteration | printed | rebuilt | cpu 2 alone | cpu 8 alone | the CPUs agree | both CPUs (the rule from 389) |\n|---|---|---|---|---|---|---|---|')
    for sn, it, p_, a, b2, b8, n, nb, bb in rows:
        print('| %d | %d | %s | %s | %s | %s | %s | %s |' % (sn, it, p_, word(a[5]), word(b2[5]), word(b8[5]), 'yes' if b2[5] == b8[5] else '**no**', word(bb[5])))
    agree = sum(1 for r in rows if r[4][5] == r[5][5]); rep_ = sum(1 for r in rows if word(r[3][5]) == r[2])
    same = sum(1 for r in rows if r[8][5] == (r[2] == 'small'))
    print('\n%d sessions: the printed verdict rebuilt in %d; the two CPUs alone agree in %d; both CPUs give the printed verdict in %d.' % (len(rows), rep_, agree, same))
elif check == 'progress':
    _db = sys.argv[2]
    import random
    sys.argv = ['x']; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); import evolve as E
    R = db(sys.argv[2] if len(sys.argv) > 2 else _db); kids = collections.defaultdict(list)
    for d in R.values():
        if d.get('status') == 'ok' and d.get('speed') and d.get('total'): kids[d.get('gen', 0)].append(d)
    G = sorted(kids); best = small = b32 = None; gain_sz, gain_sp = [], []
    keys = sorted({k for d in R.values() for k in (d.get('genome') or {})})
    memo = {}
    def ex(d):      # what is built: express(), each value as text
        if d['id'] not in memo: memo[d['id']] = {k: json.dumps(v, sort_keys=True) for k, v in E.express(E.canon(d['genome'])).items()}
        return memo[d['id']]
    def diversity(ds, n=300):
        """the mean share of built genes two designs differ in (a gene built in one and not the other differs)"""
        if len(ds) < 2: return float('nan')
        rnd = random.Random(1); t = 0
        for a, b in (rnd.sample(ds, 2) for _ in range(n)):
            A, B = ex(a), ex(b); ks = set(A) | set(B); t += sum(A.get(k) != B.get(k) for k in ks) / len(ks)
        return t / n
    fam = lambda ds, t2: [d for d in ds if (ex(d).get('tag2') not in (None, '0', 'null', 'false')) == t2]
    print('| generation | alive | best speed so far | smallest so far | best 32-bit so far | diversity: all / tag-2 family / plain family | encodings alive (enc/tag2: designs) |\n|---|---|---|---|---|---|---|')
    for g in G:
        ds = kids[g]; sp = min(d['speed'] for d in ds); sz = min(d['total'] for d in ds)
        s32 = min((d['speed32'] for d in ds if d.get('speed32')), default=None)
        if best is not None and sp < best * 0.98: gain_sp.append((g, best / sp - 1))
        if small is not None and sz < small: gain_sz.append((g, small - sz))
        best = sp if best is None else min(best, sp); small = sz if small is None else min(small, sz)
        b32 = s32 if b32 is None else (min(b32, s32) if s32 else b32)
        if g in (G[0], G[-1]) or g % 10 == 0:
            enc = collections.Counter('%s/%s' % ((d.get('genome') or {}).get('enc'), (d.get('genome') or {}).get('tag2', 0)) for d in ds)
            print('| %d | %d | %.4f | %s | %s | %.3f / %.3f / %.3f | %s |' % (g, len(ds), best, format(small, ','), '%.4f' % b32 if b32 else '-',
                  diversity(ds), diversity(fam(ds, True)), diversity(fam(ds, False)), ', '.join('%s: %d' % kv for kv in enc.most_common(4))))
    last = G[-1]; late = [x for x in gain_sz if x[0] > last * 2 // 3]
    print('\nthe smallest binary + image (exact) gained in %d generations; the last at generation %d of %d; in the last third %d gains, %d bytes in all'
          % (len(gain_sz), gain_sz[-1][0] if gain_sz else -1, last, len(late), sum(b for _, b in late)))
    print('the best speed gained 2%% or more in %d generations; the last at generation %d (%s)' % (len(gain_sp), gain_sp[-1][0] if gain_sp else -1,
          ', '.join('%d: %.1f%%' % (g, 100 * x) for g, x in gain_sp[-5:])))
elif check == 'spread':
    import math, os
    import numpy as np
    sys_args = sys.argv[2:]; sys.argv = ['x']
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
    def hv(pts, lo, ref, n=100000):     # compare-fronts.py's _hv, its numpy path, verbatim
        P = [p for p in pts if not any(all(q[k] <= p[k] for k in range(3)) and q != p for q in pts)]
        rng = np.random.default_rng(1); S = np.asarray(lo) + rng.random((n, 3)) * (np.asarray(ref) - np.asarray(lo))
        hit = np.zeros(n, bool)
        for p in P: hit |= (S >= np.asarray(p)).all(axis=1)
        return hit.mean()
    runs = []
    for a in sys_args:
        path, _, g = a.partition('@'); R = db(path)
        ok = [d for d in R.values() if d.get('status') == 'ok' and d.get('speed') and d.get('total') and d.get('rss')]
        runs.append([a, ok, int(g) if g else None, max(d.get('gen', 0) for d in ok)])
    # Iteration 505: what each run's speed is - the workloads its selection measured (seed 71: apps, the seventh) and how
    # a gated design's two readings were joined (from seed 72: the slower, not their geometric mean). A run unlike the
    # first is marked; its speed, best Q, hypervolume and 32-bit speed do not compare - its size and memory do.
    def era(ok):
        sel = collections.Counter(tuple(sorted(k for k in (d.get('t') or {}) if k not in ('sieve', 'parse'))) for d in ok).most_common(1)
        sel = sel[0][0] if sel else ()
        two = [d for d in ok if d.get('speed1') and d.get('speed2')]
        gate = ('slower' if all(abs(d['speed'] - max(d['speed1'], d['speed2'])) < 1e-9 * d['speed'] for d in two) else 'mean') if two else '?'
        return sel, gate
    eras = [era(r[1]) for r in runs]
    G0 = min(r[3] for r in runs)
    s6 = {k: json.dumps(v, sort_keys=True) for k, v in E.express(E.canon(E.HUMAN['s6-cv8b'])).items()}   # 'on' = differs from s6
    out = []
    for name, ok, g, last in runs:
        G = g if g is not None else G0; ds = [d for d in ok if d.get('gen', 0) <= G]
        pts = {d['id']: (d['speed'], d['total'], d['rss']) for d in ds}
        fr = [i for i in pts if not any(all(pts[j][k] <= pts[i][k] for k in range(3)) and pts[j] != pts[i] for j in pts)]
        use = collections.Counter()
        exs = {d['id']: {k: json.dumps(v, sort_keys=True) for k, v in E.express(E.canon(d['genome'])).items()} for d in ds if d['id'] in set(fr)}
        for e in exs.values():
            for k, v in e.items():
                if v != s6.get(k): use[k] += 1
        q = min(pts[i][0] * pts[i][1] * pts[i][2] for i in fr)
        s32 = min((d['speed32'] for d in ds if d['id'] in set(fr) and d.get('speed32')), default=None)
        out.append(dict(name=name, G=G, n=len(ds), fr=fr, pts=pts, use={k: v / len(fr) for k, v in use.items()}, q=q, s32=s32))
    allp = [tuple(math.log(x) for x in o['pts'][i]) for o in out for i in o['fr']]
    lo = tuple(min(p[k] for p in allp) for k in range(3)); ref = tuple(max(p[k] for p in allp) + 0.05 for k in range(3))
    odd = [i for i in range(len(runs)) if eras[i][0] != eras[0][0] or (eras[i][1] != eras[0][1] and '?' not in (eras[i][1], eras[0][1]))]
    if odd:
        print('**Not like the first run** (marked \u2260): speed over %d workloads (%s), the gate\'s readings joined by %s - against it, the marked'
              ' runs\' fastest, best Q, hypervolume and 32-bit speed do not compare; their size and memory do.\n' % (len(eras[0][0]), ', '.join(eras[0][0]), eras[0][1]))
        for i in odd: runs[i][0] = out[i]['name'] = '\u2260 ' + runs[i][0] + ' (%d workloads, %s)' % (len(eras[i][0]), eras[i][1])
    print('| run | generation | designs to it | front | fastest | smallest | least memory KB | best Q | hypervolume | fastest at 32 bits |\n|---|---|---|---|---|---|---|---|---|---|')
    for o in out:
        P = [o['pts'][i] for i in o['fr']]
        print('| %s | %d | %d | %d | %.4f | %s | %.0f | %.5g | %.4f | %s |' % (o['name'], o['G'], o['n'], len(o['fr']), min(p[0] for p in P),
              format(min(p[1] for p in P), ','), min(p[2] for p in P), o['q'], hv([tuple(math.log(x) for x in p) for p in P], lo, ref),
              '%.4f' % o['s32'] if o['s32'] else '-'))
    print('\ngene usage on the fronts, how far apart - the mean difference in points over every built gene (two runs of one start; for scale, seeds 55 and 56 differed by up to 17 points in a gene):')
    for i in range(len(out)):
        for j in range(i + 1, len(out)):
            ks = set(out[i]['use']) | set(out[j]['use'])
            d = [abs(out[i]['use'].get(k, 0) - out[j]['use'].get(k, 0)) for k in ks]
            top = sorted(ks, key=lambda k: -abs(out[i]['use'].get(k, 0) - out[j]['use'].get(k, 0)))[:5]
            print('  %s - %s: mean %.1f points; the most: %s' % (out[i]['name'], out[j]['name'], 100 * sum(d) / len(d),
                  ', '.join('%s %+.0f' % (k, 100 * (out[j]['use'].get(k, 0) - out[i]['use'].get(k, 0))) for k in top)))
elif check == 'fail32':
    path = sys.argv[2]; sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
    c = collections.Counter(); n = ok = 0
    for l in open(path, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('speed32') is not None: ok += 1
        w = r.get('why32')
        if not w: continue
        n += 1
        try: g = E.canon(r['genome']); e = E.express(g)
        except Exception as x: c[(w, 'genome unreadable (%s)' % str(x)[:50])] += 1; continue
        k = None
        if 'corpus' in w and e.get('bfind') and not e.get('tos'): k = 'bfind without tos'
        elif 'compile' in w and e.get('tail'): k = 'tail, %s%s' % ('clang' if g.get('compiler') else 'GCC', ' with preserve_none' if e.get('tailpn') else '')
        c[(w, k or 'not a known cause - look')] += 1
    print('at 32 bits: %d designs measured, %d failed' % (ok, n))
    for (w, k), m in sorted(c.items(), key=lambda kv: -kv[1]): print('  %6d  %s - %s' % (m, w, k))
    known = sum(m for (w, k), m in c.items() if k.startswith(('bfind', 'tail')))
    print('the known causes: %d of %d (fixed by the after-seed-62 batch: from seed 63 on, any is a regression)' % (known, n))
elif check == 'generic':
    import glob, math
    rd = sys.argv[2]; cls = {}
    for f in sorted(glob.glob(os.path.join(rd, '*', 'out.json'))):
        name = os.path.basename(os.path.dirname(f))
        try: o = json.load(open(f))
        except (OSError, ValueError): continue
        m = str((o.get('env') or {}).get('machine', ''))
        c = 'ARMv7' if m.startswith('arm') else 'x86-32' if (o.get('cell') == 4 or name.endswith('32')) else 'x86-64'
        if c == 'x86-64' and c in cls and not name.endswith('64'): continue      # prebuilt64, prebuilt32's pair, first
        cls[c] = (name, {x['id']: x for x in o.get('designs', []) if x.get('speed_here') is not None})
    need = ('x86-64', 'x86-32', 'ARMv7')
    if not all(k in cls for k in need): print('generic: the classes measured - %s; all three needed' % (', '.join(sorted(cls)) or 'none')); sys.exit(0)
    common = set.intersection(*[set(cls[k][1]) for k in need])
    if not common: print('generic: no design measured on all three classes'); sys.exit(0)
    best = {k: min(cls[k][1][i]['speed_here'] for i in common) for k in need}
    rows = []
    for i in common:
        s = [cls[k][1][i]['speed_here'] for k in need]; gm = math.exp(sum(math.log(v) for v in s) / 3)
        veto = [k for k, v in zip(need, s) if v > 1.25 * best[k]]
        xs = [cls[k][1][i] for k in need]
        kind = 'asked' if any(x.get('asked') for x in xs) else 'rejected' if any(x.get('rejected') for x in xs) else 'front'
        rows.append((gm, i, s, veto, kind, xs[0].get('speed'), xs[0].get('total')))
    rows.sort()
    print('across the machine classes - %s: %d designs measured on all three, by the geometric mean of their speeds (each against s6 there); veto: more than 25%% behind the class\'s best of them'
          % ('; '.join('%s %s' % (k, cls[k][0]) for k in need), len(rows)))
    print('| design | kind | x86-64 | x86-32 | ARMv7 | mean | veto | laptop | bytes |')
    print('|---|---|---|---|---|---|---|---|---|')
    for gm, i, s, veto, kind, lap, tot in rows:
        print('| %s | %s | %.3f | %.3f | %.3f | **%.3f** | %s | %s | %s |' % (i, kind, s[0], s[1], s[2], gm, ', '.join(veto) or '-', '%.3f' % lap if lap else '-', '{:,}'.format(tot) if tot else '-'))
elif check == 'votes':
    args = sys.argv[2:]; ledger = None; seed = None; append = '--append' in args
    if '--ledger' in args: i = args.index('--ledger'); ledger = args[i + 1]; del args[i:i + 2]
    if '--seed' in args: i = args.index('--seed'); seed = int(args[i + 1]); del args[i:i + 2]
    path = [a for a in args if a != '--append'][0]
    if seed is None:
        m = re.search(r'seed(\d+)', os.path.basename(path)); seed = int(m.group(1)) if m else 0
    sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
    cols = None; tab = {}; gen = {}
    for l in open(path, errors='replace'):
        if l.startswith('| design | speed |'): cols = [c.strip() for c in l.strip().strip('|').split('|')]; continue
        if cols and re.match(r'\| [0-9a-f]{10} \|', l):
            c = [x.strip() for x in l.strip().strip('|').split('|')]; tab.setdefault(c[0], dict(zip(cols, c)))
        if l.startswith('{"'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id') and 'genome' in r: gen.setdefault(r['id'], r['genome'])
    def num(v):
        try: return float(str(v).replace(',', ''))
        except ValueError: return None
    ids = [i for i in tab if i in gen]; n = len(ids); k = max(1, n // 10)
    sp = {i: num(tab[i].get('re-measured', '')) or num(tab[i].get('speed', '')) or 9e9 for i in ids}
    by = {i: num(tab[i].get('binary + image', '')) or 9e9 for i in ids}
    mem = {i: num(tab[i].get('memory KB', '')) or 9e9 for i in ids}
    fast = set(sorted(ids, key=sp.get)[:k]); small = set(sorted(ids, key=by.get)[:k])
    bestq = set(sorted(ids, key=lambda i: sp[i] * by[i] * mem[i])[:k])
    ex = {i: E.express(E.canon(gen[i])) for i in ids}
    frozen = set(getattr(E, 'FROZEN', None) or ())
    SKIP = {'enc', 'opt', 'compiler', 'spec', 'folds', 'ops10'}          # what a design is, not a mechanism to drop
    # Iteration 487: only the genes the run's own code had - a gene added since (seed 69: jitmul, jitdoes, jitexec, jitcfa)
    # is on no design of that run, and four removal votes would count against what it never had the chance to be.
    # The run's commit: --at, else the results file's "asked at <hash>"; its evolve.py's quoted names are the genes then.
    at = None
    if '--at' in sys.argv: at = sys.argv[sys.argv.index('--at') + 1]
    else:
        m_ = re.search(r'asked at\s+([0-9a-f]{7,40})', open(path, errors='replace').read(4000)); at = m_.group(1) if m_ else None
    known = None
    if at:
        import subprocess
        src_ = subprocess.run(['git', 'show', at + ':lab/evolve/evolve.py'], capture_output=True, text=True,
                              cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).stdout
        known = set(re.findall(r"'(\w+)'", src_)) or None
    run = []
    fams = set(gen[i].get('enc') for i in ids)                      # Iteration 450: the front's encodings' genes only -
    for g in dict.fromkeys(x for f, fam in E.EXPRESSED.items() if f in fams for x in fam):   # skippad and fold, sod16's and
        if g in SKIP or g in frozen: continue                        # cpt16's, were voted on in CV8 fronts they cannot reach
        if known is not None and g not in known: continue           # 487: not in the run's code
        on = set(i for i in ids if ex[i].get(g)); share = 100.0 * len(on) / n if n else 0.0
        f, sm, q = len(on & fast), len(on & small), len(on & bestq)
        run.append((seed, g, share, f, sm, q, (share < 10) + (f == 0) + (sm == 0) + (q == 0)))
    rows = []
    if ledger and os.path.exists(ledger):
        for l in open(ledger):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) == 7 and c[0].isdigit():
                rows.append((int(c[0]), c[1], float(c[2].rstrip('%')), int(c[3]), int(c[4]), int(c[5]), int(c[6])))
    if ledger and append and seed not in set(r[0] for r in rows):
        with open(ledger, 'a') as fo:
            for r in run: fo.write('| %d | %s | %.0f%% | %d | %d | %d | %d |\n' % r)
    rows = [r for r in rows if r[0] != seed] + run
    last = sorted(set(r[0] for r in rows))[-3:]
    print('seed %d: %d front designs (tenths of %d) - the removal votes of each gene this run, of 4: share under 10%%, none in the fastest, smallest, best-Q tenth' % (seed, n, k))
    print('all four this run: %s' % (', '.join(g for _, g, _, _, _, _, v in run if v == 4) or 'none'))
    # Iteration 502 (the owner): a grace period - a gene's votes count from its second run with a workload that
    # measures what it does (results/seed63-rules.md, rule 12). Seed 70 voted four times against jitmul, jitdoes,
    # jitexec and jitcfa, which no workload paid for until the applications joined the selection (seed 71); jitrp
    # was enabled for seed 71. Their votes count from seed 72. A gene enabled later gets its line here.
    # 518 (the owner): jitexec's from seed 74 - until the after-seed-72 batch its JIT table cost 585 KB (a bug,
    # results/drafts/jit-genes-517.md), so seeds 70-72 could not weigh it; its first fair run is 73, its votes from 74
    GRACE = {'jitmul': 72, 'jitdoes': 72, 'jitexec': 74, 'jitcfa': 72, 'jitrp': 72,
             'jitfuse': 73}   # 508: enabled after seed 71 - its first run seed 72, its votes from seed 73
    tally = collections.OrderedDict()
    for r in rows:
        if r[0] in last and r[0] >= GRACE.get(r[1], 0): tally.setdefault(r[1], []).append(r)
    cand, near = [], []
    for g, rs in tally.items():
        votes = sum(r[6] for r in rs); keep = any(r[3] or r[4] or r[5] for r in rs)
        if len(rs) == 3 and not keep and votes >= 11: cand.append('%s (%d of 12)' % (g, votes))
        elif not keep and votes >= 6: near.append('%s (%d of %d)' % (g, votes, 4 * len(rs)))
    print('over the last %d runs in the ledger (%s): candidates - %s; no keep vote and half the votes or more - %s'
          % (len(last), ', '.join(map(str, last)), ', '.join(cand) or 'none', ', '.join(near) or 'none'))
elif check == 'rules':
    args = sys.argv[2:]; opts = {}
    for key in ('--db', '--ledger', '--seed'):
        if key in args: i = args.index(key); opts[key] = args[i + 1]; del args[i:i + 2]
    path = args[0]
    m = re.search(r'seed(\d+)', os.path.basename(path)); seed = int(opts.get('--seed') or (m.group(1) if m else 0))
    sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
    cols = None; tab = {}; gen = {}
    for l in open(path, errors='replace'):
        if l.startswith('| design | speed |'): cols = [c.strip() for c in l.strip().strip('|').split('|')]; continue
        if cols and re.match(r'\| [0-9a-f]{10} \|', l):
            c = [x.strip() for x in l.strip().strip('|').split('|')]; tab.setdefault(c[0], dict(zip(cols, c)))
        if l.startswith('{"'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id') and 'genome' in r: gen.setdefault(r['id'], r['genome'])
    def num(v):
        try: return float(str(v).replace(',', ''))
        except ValueError: return None
    ids = [i for i in tab if i in gen]; n = len(ids); k = max(1, n // 10)
    sp = {i: num(tab[i].get('re-measured', '')) or num(tab[i].get('speed', '')) or 9e9 for i in ids}
    by = {i: num(tab[i].get('binary + image', '')) or 9e9 for i in ids}
    mem = {i: num(tab[i].get('memory KB', '')) or 9e9 for i in ids}
    fast = set(sorted(ids, key=sp.get)[:k]); small = set(sorted(ids, key=by.get)[:k])
    bestq = set(sorted(ids, key=lambda i: sp[i] * by[i] * mem[i])[:k])
    cg = {i: E.canon(gen[i]) for i in ids}; ex = {i: E.express(cg[i]) for i in ids}
    out = []
    led = collections.defaultdict(list)
    if opts.get('--ledger') and os.path.exists(opts['--ledger']):
        for l in open(opts['--ledger']):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) == 7 and c[0].isdigit() and int(c[0]) != seed: led[c[1]].append((int(c[0]), int(c[3]), int(c[4]), int(c[5]), int(c[6])))
    def gene_line(g):
        on = set(i for i in ids if ex[i].get(g)); share = 100.0 * len(on) / n if n else 0.0
        f, sm_, q = len(on & fast), len(on & small), len(on & bestq); v = (share < 10) + (f == 0) + (sm_ == 0) + (q == 0)
        runs = sorted(led[g])[-2:] + [(seed, f, sm_, q, v)]
        keep = any(r[1] or r[2] or r[3] for r in runs); tv = sum(r[4] for r in runs)
        cand = len(runs) == 3 and not keep and tv >= 11
        return ('%.0f%% of the front; in the fastest, smallest, best-Q tenth %d, %d, %d; %d of 4 removal votes, over %d run(s) %d%s'
                % (share, f, sm_, q, v, len(runs), tv, ' - a candidate' if cand else ('; a keep vote' if keep else ''))), cand
    out.append((1, 'The verdict', "compare-fronts - process-seed.sh's verdict section", 'the 5% bar', 'SEE'))
    for g in ('jitret',):              # Iteration 504: jithelp and jitre retired - rule 2 watches jitret alone
        t, cand = gene_line(g); out.append((2, g, t, 'kept unless a candidate: 11 of 12 over three runs, no keep vote', 'ATTENTION' if cand else 'PASS'))
    rows = sorted(front_rows(path), key=lambda r: r['sp']); kk = max(1, len(rows) // 10)
    if rows:
        r = sorted(x['rem'] / x['sp'] for x in rows[:kk]); med = r[len(r) // 2]
        out.append((3, 'The fast gate', 'the fastest tenth re-measured / in-run: median %.3f (%d designs)' % (med, kk),
                    '0.98-1.05 works', 'PASS' if 0.98 <= med <= 1.05 else 'ATTENTION'))
    frz = getattr(E, 'FROZEN', None) or {}; bad = collections.Counter()
    for i in ids:
        for g, val in frz.items():
            if (ex[i].get(g) or 0) != val: bad['%s %s' % (g, 'off' if val else 'on')] += 1
    reach = known = other = None
    if opts.get('--db'):
        reach = known = other = 0
        for l in open(opts['--db'], errors='replace'):
            if 'reach limit' not in l and '"why32"' not in l: continue
            try: r = json.loads(l)
            except ValueError: continue
            if 'reach limit' in str(r.get('status', '')): reach += 1
            w = r.get('why32')
            if w:
                g = E.canon(r['genome']); e = E.express(g)
                if ('corpus' in w and e.get('bfind') and not e.get('tos')) or ('compile' in w and e.get('tail')): known += 1
                else: other += 1
    out.append((4, 'The freeze', 'front designs off a frozen value: %s; refused at the reach limit: %s'
                % (', '.join('%s %d' % kv for kv in sorted(bad.items())) or 'none', 'give --db' if reach is None else reach),
                'none and none', 'SEE' if reach is None and not bad else ('PASS' if not bad and not reach else 'ATTENTION')))
    out.append((5, '32-bit correctness', 'give --db' if known is None else 'failures of a known cause %d, of another %d' % (known, other),
                'none of a known cause', 'SEE' if known is None else ('PASS' if known == 0 and other == 0 else 'ATTENTION')))
    sm = min(by.values()) if by else None
    out.append((6, 'The small end', "the front's smallest %s bytes" % ('{:,}'.format(int(sm)) if sm else '-'), 'at most 14,535',
                'PASS' if sm and sm <= 14535 else 'ATTENTION'))
    on = [i for i in ids if ex[i].get('rtiplus')]                  # Iteration 448: and how many have the fuser I+ needs -
    eff = [i for i in on if E.overlay(cg[i])]                      # without it rtiplus is expressed and inert (447)
    share = 100.0 * len(eff) / n if n else 0.0
    out.append((7, 'I+ (rtiplus)', '%d designs with it, %d of them with the run-time fuser it needs - %.0f%% of the front working'
                % (len(on), len(eff), share), 'above 10%, working', 'PASS' if share > 10 else 'NOTED'))
    t, cand = gene_line('tail'); out.append((8, 'tail', t, 'kept unless a candidate', 'ATTENTION' if cand else 'PASS'))
    ov = [i for i in ids if E.rtimm2(cg[i]) and not ex[i].get('rtfuse') and (E.supers_in(cg[i]) or E.rt_tests(cg[i]))]
    out.append((9, 'The rtimm=2 / rtfuse overlap', 'front designs relying on it: %d' % len(ov), 'none: rtfuse to govern - proposed; some: no change',
                'PROPOSE' if not ov else 'PASS'))
    out.append((10, 'Programs past 4 MB', "the routine's run-tests and corpus", 'pass', 'SEE'))
    print('seed %d, %d front designs - results/seed63-rules.md\'s rules, measured (review-checks.py rules)' % (seed, n))
    print('| # | what | measured | rule | |'); print('|---|---|---|---|---|')
    for r in out: print('| %s | %s | %s | %s | **%s** |' % r)
else: sys.exit(__doc__)
