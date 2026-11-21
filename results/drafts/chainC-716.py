#!/usr/bin/env python3
"""results/drafts/chainC-716.py - chain C's open pairs, paired by session as followup-roles.py pools (each class the mean
of its sources: x86-64 the laptop alone and dream at 8-byte cells, x86-32 the same at 4, ARMv7 the Tegra), in chain B, in
chain C, and the two chains pooled by inverse variance (Iteration 716): the smallest's three options against each other,
the fastest portable's tie, the x86-32 ties, the x86-64 near one. Run from the repository's top."""
import glob, json, math, os, statistics

CH = {'B': ('results/followup-seed96-roles-b.md', 'results/chain-followup96-roles-b'),
      'C': ('results/followup-seed96-roles-c.md', 'results/chain-followup96-roles-c')}
LAP = {'lap64': 'idle', 'lap32': 'idle32'}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json',
        'rage': 'rage.lan-prebuiltarm.out.json'}
PARTS = {'x86-64': ('lap64', 'dream64'), 'x86-32': ('lap32', 'dream32'), 'ARMv7': ('rage',)}

def load(ses):
    S = {s: {} for s in list(LAP) + list(HOST)}
    for d in glob.glob(os.path.join(ses, 's[0-9]*')):
        k = int(d.rsplit('s', 1)[1]); p = os.path.join(d, 'loadtest.md')
        if os.path.exists(p):
            for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
                for s, key in LAP.items():
                    if r.get(key): S[s].setdefault(r['id'], {})[k] = r[key]
        for s, f in HOST.items():
            p = os.path.join(d, f)
            if os.path.exists(p):
                for x in json.load(open(p))['designs']:
                    if x.get('speed_here'): S[s].setdefault(x['id'], {})[k] = x['speed_here']
    return S

def cls(S, k, a, b):                       # (mean log ratio, SE) of a against b in class k, or None
    xs = []
    for s in PARTS[k]:
        d = [math.log(S[s][a][j] / S[s][b][j]) for j in S[s].get(a, {}) if j in S[s].get(b, {})]
        if len(d) < 2: return None
        xs.append((statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))))
    return sum(m for m, _ in xs) / len(xs), math.sqrt(sum(e * e for _, e in xs)) / len(xs)

def mean3(S, a, b):
    cs = [cls(S, k, a, b) for k in PARTS]
    if None in cs: return None
    return sum(m for m, _ in cs) / 3, math.sqrt(sum(e * e for _, e in cs)) / 3

def pool(xs):
    xs = [x for x in xs if x]
    if not xs: return None
    w = [1 / (e * e) for _, e in xs]
    return sum(m * v for (m, _), v in zip(xs, w)) / sum(w), 1 / math.sqrt(sum(w))

f = lambda x: '-' if not x else '%+.2f%% +/- %.2f%%' % ((math.exp(x[0]) - 1) * 100, x[1] * 100)
S = {c: load(ses) for c, (_, ses) in CH.items()}
size = {}
for c, (lst, _) in CH.items():
    for r in (json.loads(l) for l in open(lst) if l.startswith('{"')): size[r['id']] = (r['total'], r.get('rss'))
PAIRS = [('the smallest: 90273721a1 (21,679 B) against 219878ec89 (21,673 B)', '90273721a1', '219878ec89', list(PARTS)),
         ('the smallest: 3456fc28b2 (21,666 B) against 219878ec89', '3456fc28b2', '219878ec89', list(PARTS)),
         ('the smallest: 90273721a1 against 3456fc28b2', '90273721a1', '3456fc28b2', list(PARTS)),
         ('fastest portable: 5f7e66b12d against d727605472', '5f7e66b12d', 'd727605472', list(PARTS) + ['mean']),
         ('fastest on x86-32: 69cebcaed9 against ea782c6094', '69cebcaed9', 'ea782c6094', ['x86-32', 'x86-64']),
         ('fastest on x86-32: 11f956db93 against ea782c6094', '11f956db93', 'ea782c6094', ['x86-32', 'x86-64']),
         ('fastest on x86-32: 11f956db93 against 69cebcaed9', '11f956db93', '69cebcaed9', ['x86-32', 'x86-64']),
         ('fastest on x86-32: 163935642a against ea782c6094', '163935642a', 'ea782c6094', ['x86-32', 'x86-64']),
         ('fastest on x86-32: b525180392 against ea782c6094', 'b525180392', 'ea782c6094', ['x86-32', 'x86-64']),
         ('fastest on x86-64: 262a51bc6c against 9b15ba26f7', '262a51bc6c', '9b15ba26f7', ['x86-64', 'x86-32']),
         ('fastest on x86-64: df097ba2e2 against 9b15ba26f7', 'df097ba2e2', '9b15ba26f7', ['x86-64', 'x86-32']),
         ('smallest JIT: 13a2b38e1b against 15eda54ebd', '13a2b38e1b', '15eda54ebd', ['x86-64', 'x86-32']),
         ('smallest JIT: fa38596098 against 15eda54ebd', 'fa38596098', '15eda54ebd', ['x86-64', 'x86-32'])]
print('# Chain C\'s open pairs - chain B, chain C, pooled (results/drafts/chainC-716.py)')
for name, a, b, ks in PAIRS:
    print('\n%s - %s B %s KB, %s B %s KB' % (name, '{:,}'.format(size[a][0]), size[a][1], '{:,}'.format(size[b][0]), size[b][1]))
    for k in ks:
        g = (lambda s: mean3(s, a, b)) if k == 'mean' else (lambda s: cls(s, k, a, b))
        xb, xc = g(S['B']), g(S['C'])
        print('  %-7s B %-20s C %-20s pooled %s' % (k, f(xb), f(xc), f(pool([xb, xc]))))
print('\nBy source - 262a51bc6c against 9b15ba26f7 (the chains\' disagreement on x86-64):')
for c in CH:
    xs = []
    for s in PARTS['x86-64']:
        d = [math.log(S[c][s]['262a51bc6c'][j] / S[c][s]['9b15ba26f7'][j]) for j in S[c][s]['262a51bc6c'] if j in S[c][s]['9b15ba26f7']]
        xs.append('%s %s n%d' % (s, f((statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d)))), len(d)))
    print('  %s: %s' % (c, ', '.join(xs)))
