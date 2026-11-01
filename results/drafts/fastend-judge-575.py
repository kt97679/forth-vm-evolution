#!/usr/bin/env python3
"""results/drafts/fastend-judge-575.py LOADTEST.md [--ids results/fastend-remeasure-575.md] [--db FILE] - seed 84's
fast-end gain judged on the re-measure (Iteration 575; the owner's decision, GOALS.md 575).

LOADTEST.md: loadtest.py --ids's output from the chain after seed 84 (its JSON lines: id, inrun, inrun32, idle, loaded,
idle32, loaded32). Prints, at each width and by each reading (idle, loaded):
  1. each group's median re-measured / in-run (the groups: fastend-ids-575.py's "why");
  2. seed 84's best bred design against the best of the rest (its re-timed founders and the pool), both re-measured -
     the gain stands when the bred one is ahead by the extreme's threshold (2%, GOALS.md step 1) in both readings;
  3. the stricter test again (confirm.py's: the pool and seed 84's bred designs against the pool's
     hypervolume, the bar 1%), every re-measured design's two speeds replaced by its idle reading on both sides. --db: seed 84's records - by default its results file's front (391 on
     its true front against the database's 389: close, not the same; the seed pack's db.jsonl when at hand).
The verdict line: STANDS - a second confirmation run (GOALS.md step 2); else GONE - seed 84 confirmed in effect, the
candidates re-measured in full (loadtest.py --ids results/candidates-final-seed84.md, dream and the Tegra by --also)
and the final pick. Run from the repository root."""
import json, statistics, sys
a = sys.argv[1:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
lt, idf, db = a[0], opt('--ids', 'results/fastend-remeasure-575.md'), opt('--db', 'results/evolve-amd-ryzen-7-pro-8840hs-seed84.md')
M = {}
for l in open(lt, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'): M[r['id']] = r
I = {r['id']: r for r in (json.loads(l) for l in open(idf) if l.startswith('{'))}
print('%d of %d designs re-measured; missing: %s' % (sum(1 for i in I if i in M), len(I), ' '.join(i for i in I if i not in M) or 'none'))
isbred = lambda i: I[i]['why'].endswith('bred, as fast as its best founder') or I[i]['why'].endswith('bred, fastest at 32 bits')
stands = True
for w, inr in (('', 'inrun'), ('32', 'inrun32')):
    print('\n%s bits' % ('64' if not w else '32'))
    for why in sorted(set(r['why'] for r in I.values())):
        for rd in ('idle', 'loaded'):
            q = [M[i][rd + w] / M[i][inr] for i in I if I[i]['why'] == why and i in M and M[i].get(rd + w) and M[i].get(inr)]
            if q: print('  %-46s %-6s re-measured / in-run median %.3f (%d)' % (why, rd, statistics.median(q), len(q)))
    for rd in ('idle', 'loaded'):
        ok = [i for i in I if i in M and M[i].get(rd + w)]
        b = [i for i in ok if isbred(i)]; o = [i for i in ok if not isbred(i)]
        if not b or not o: print('  %s: a side unmeasured - judge by hand' % rd); stands = stands and bool(w); continue
        bb, bo = min(b, key=lambda i: M[i][rd + w]), min(o, key=lambda i: M[i][rd + w])
        g = 1 - M[bb][rd + w] / M[bo][rd + w]
        print('  %s: the best bred %s %.4f, the best of the rest %s %.4f (%s) - %+.1f%%%s'
              % (rd, bb, M[bb][rd + w], bo, M[bo][rd + w], I[bo]['why'], 100 * g, '' if g >= 0.02 else ' - under 2%'))
        if not w: stands = stands and g >= 0.02          # the gain was the fastest at 64 bits; 32 bits reported
if db:
    sys.path.insert(0, 'lab/evolve'); import hv, stopping, confirm
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS)); _, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 84]
    fix = lambda r: dict(r, speed=M[r['id']]['idle'], speed32=M[r['id']]['idle32']) if r['id'] in M and M[r['id']].get('idle') and M[r['id']].get('idle32') else r
    P = {}
    for f in confirm.pool_files(runs): P.update({i: fix(r) for i, r in hv.load(f, E).items()})
    R = {i: fix(r) for i, r in hv.load(db, E).items()}; T = hv.true_front(R, E)
    bred = [i for i in T if not str(R[i].get('how', '')).startswith(confirm.CARRIED)]
    ph = confirm.front_hv(P, E, b)[1]; U = dict(P); U.update({i: R[i] for i in bred}); hb = confirm.front_hv(U, E, b)[1]
    print('\nthe stricter test on the idle re-measures: the pool %.5f, with seed 84\'s bred %.5f - %+.2f%% (the bar 1%%)' % (ph, hb, 100 * (hb / ph - 1)))
    stands = stands or hb >= ph * 1.01
print('\nverdict: %s' % ('STANDS - a second confirmation run (GOALS.md step 2, 575)' if stands else
                         'GONE - seed 84 confirmed in effect; the candidates re-measured in full, then the final pick (575)'))
