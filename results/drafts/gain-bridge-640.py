#!/usr/bin/env python3
"""results/drafts/gain-bridge-640.py - seed 91's follow-up's gain against the best found before, the whole pool (Iteration 640).

followup-roles.py --gain compares the run's designs with the list's "found before" alone; seed 91's list took those from
followup-pick-seed90.json (seed 90's 7-design knee check) and the holders, so the pool's extremes that hold no role -
9f8811f7f4 (seed 88's follow-up's fastest at 32 bits on the laptop), 4dd4e3e7e2 (13,709 B, the owner's 611/621 trade) -
were not in it. Sizes are exact: the pool before seed 91 (results/portable-front-seed90.md) and every follow-up list.
Speeds on the laptop alone: each JIT-free design of an earlier follow-up (87-90) carried into seed 91's chain through the
designs both chains measured (bridges), paired by session within each chain: est = (D/B in chain N) * (B in chain 91).
The median over bridges, their range, against the run's best re-measured. No new readings - the recorded ones only."""
import glob, json, math, os, statistics

R = 'results'
gm = lambda v: math.exp(statistics.fmean(math.log(t) for t in v))
recs = lambda f: [json.loads(l) for l in open(f) if l.startswith('{')]


def laptop(n):
    """chain-followupN: key -> design -> {session: reading} for the laptop alone"""
    S = {'idle': {}, 'idle32': {}}
    for d in glob.glob('%s/chain-followup%d/s[0-9]*' % (R, n)):
        k = int(d.rsplit('s', 1)[1]); f = os.path.join(d, 'loadtest.md')
        if not os.path.exists(f): continue
        for l in open(f, errors='replace'):
            if l.startswith('{"'):
                r = json.loads(l)
                for key in S:
                    if r.get(key): S[key].setdefault(r['id'], {})[k] = r[key]
    return S


def ratio(S, a, b):
    d = [math.log(S[a][k] / S[b][k]) for k in S[a] if k in S.get(b, {})]
    return math.exp(statistics.fmean(d)) if d else None


L = {n: laptop(n) for n in (87, 88, 89, 90, 91)}
C91 = {r['id']: r for r in recs('%s/followup-seed91.md' % R)}
run = [i for i in C91 if str(C91[i].get('why', '')).startswith('the run')]
nojit = lambda r: not r.get('jit')
FB = {}                                              # found before: every JIT-free design of an earlier follow-up list
for n in (87, 88, 89, 90):
    for r in recs('%s/followup-seed%d.md' % (R, n)):
        if nojit(r): FB.setdefault(r['id'], r)
for i in C91:
    if i not in run: FB.setdefault(i, C91[i])
print('# Seed 91\'s follow-up against the best found before, the whole pool (results/drafts/gain-bridge-640.py)\n')
for key, w in (('idle32', '4-byte'), ('idle', '8-byte')):
    S91 = L[91][key]
    x = min((i for i in run if i in S91), key=lambda i: gm(S91[i].values()))
    xv = gm(S91[x].values())
    est = []
    for n in (87, 88, 89, 90):
        S = L[n][key]
        br = [b for b in S if b in S91 and b in FB and b not in run]
        for d in S:
            if d not in FB or d in S91: continue
            e = [ratio(S, d, b) * gm(S91[b].values()) for b in br if ratio(S, d, b)]
            if e: est.append((statistics.median(e), d, n, min(e), max(e), len(e)))
    direct = min((i for i in S91 if i in FB), key=lambda i: gm(S91[i].values()))
    dv = gm(S91[direct].values())
    print('the laptop alone, %s cells: the run\'s %s %.4f' % (w, x, xv))
    print('  re-measured here, found before: %s %.4f -> %+.2f%% (followup-roles.py --gain\'s comparison)' % (direct, dv, (xv / dv - 1) * 100))
    for v, d, n, lo, hi, k in sorted(est)[:4]:
        print('  bridged from chain-followup%d: %s %.4f (%d bridges, %.4f-%.4f) -> %+.2f%% (%+.2f%% to %+.2f%%)'
              % (n, d, v, k, lo, hi, (xv / v - 1) * 100, (xv / hi - 1) * 100, (xv / lo - 1) * 100))
pool = recs('%s/portable-front-seed90.md' % R) + list(FB.values())
y = min(pool, key=lambda r: r['total']); x = min(run, key=lambda i: C91[i]['total'])
print('binary + image (exact): the run\'s %s %s B, the pool\'s smallest %s %s B: %+.2f%% (the rule: 1%%)'
      % (x, format(C91[x]['total'], ','), y['id'], format(y['total'], ','), (C91[x]['total'] / y['total'] - 1) * 100))
