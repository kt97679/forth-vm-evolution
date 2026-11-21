#!/usr/bin/env python3
"""results/drafts/designs-table-718.py - designs/README.md's table for the ten roles of results/relf-designs-718.md
(Iteration 718): each class the geometric mean over a chain's sessions, then of its machines (x86-64: the laptop alone
and dream at 8-byte cells; x86-32 the same at 4; ARMv7: the Tegra) - chain B's readings where it has all of a design's
classes (it measured all ten roles' candidates but small-jit's, with the JIT designs' JIT-off builds on the Tegra), else
chain C's; bytes and memory the record's (engine + image + the five programs' code at 8-byte cells; the laptop's peak).
Run from the repository's top; prints the table's rows."""
import glob, json, math, os, statistics

LAP = {'lap64': 'idle', 'lap32': 'idle32'}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
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
def cls(S, i):
    c = {}
    for k, ss in PARTS.items():
        if all(S[s].get(i) for s in ss):
            c[k] = math.exp(statistics.fmean(statistics.fmean(math.log(v) for v in S[s][i].values()) for s in ss))
    return c
B, C = load('results/chain-followup96-roles-b'), load('results/chain-followup96-roles-c')
WHAT = {'fastest-x86-64': 'fastest on x86-64', 'fastest-x86-32': 'fastest on x86-32',
        'best-all-round': 'best mean of x86-64, x86-32 and ARMv7', 'small-jit': 'smallest of the JIT designs',
        'portable-fastest': 'fastest without the JIT, by the mean', 'portable-arm': 'fastest on ARMv7',
        'portable-knee': 'fast without the JIT; small', 'portable-small': 'small, fast on ARMv7',
        'least-memory': 'least memory', 'smallest': 'smallest'}
roles = ['fastest-x86-64', 'fastest-x86-32', 'best-all-round', 'small-jit', 'portable-fastest', 'portable-arm',
         'portable-knee', 'portable-small', 'least-memory', 'smallest']
recs = [json.loads(l) for l in open('results/relf-designs-718.md') if l.startswith('{"')]
for n, r in zip(roles, recs):
    i = r['id']; cb, cc = cls(B, i), cls(C, i)
    c, src = (cb, 'B') if len(cb) == 3 else ((cc, 'C') if len(cc) >= len(cb) else (cb, 'B'))
    jit = bool(r['genome'].get('jit')) and r['genome'].get('compiler') == 1
    f = lambda k: ('%.3f' % c[k] + ('*' if k == 'ARMv7' and jit else '')) if k in c else '-'
    print('| `%s` | %s | %s | %s | %s | %s | {:,} | %s KB | %s |'.format(r['total'])
          % (n, i, WHAT[n], f('x86-64'), f('x86-32'), f('ARMv7'), r.get('rss'), 'yes' if jit else 'no') + '  <!-- chain %s -->' % src)
