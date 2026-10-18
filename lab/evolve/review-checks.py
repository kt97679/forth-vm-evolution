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
  screen DB RESULTS.md     the surrogate screen's audit: screened children measured anyway that reached the
                           final front, against the base rate; the tag-2 share screened and not
"""
import collections, json, re, sys
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
else: sys.exit(__doc__)
