#!/usr/bin/env python3
"""results/drafts/chainB-714.py LIST SESSIONS OUT - chain B's readings judged beyond followup-roles.py (Iteration 714):
  1. each speed role's leader and the designs it does not separate from - within 2 SE of the leader, paired by session,
     pooled as followup-roles.py pools (each source's geometric mean over its sessions; x86-64 the laptop alone and dream
     at 8-byte cells, x86-32 likewise at 4, ARMv7 the Tegra; the mean of the three) - and the leader again by the median
     over sessions (the owner, 713: "ensure we are not losing good designs");
  2. the smallest role's contenders, each against each, by class;
  3. the stalls: readings more than 10 % off their design's median after the session's common shift;
  4. the laptop's machine line (the ticker, next-run.log in the last pack) by loadtest session.
LIST: results/followup-seed96-roles-b.md; SESSIONS: results/chain-followup96-roles-b; OUT: process-followup.sh's /tmp/followup.
JIT: the JIT expressed (followup-roles.py's test, 713)."""
import glob, json, math, os, re, statistics, sys

lst, ses, out = sys.argv[1:4]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
jit = {i for i in C if E.express(E.canon(C[i]['genome'])).get('jit')}
LAP = {'lap64': 'idle', 'lap32': 'idle32'}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
S = {s: {i: {} for i in C} for s in list(LAP) + list(HOST)}          # source -> id -> {session: reading}
for d in glob.glob(os.path.join(ses, 's[0-9]*')):
    k = int(d.rsplit('s', 1)[1]); p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
            for s, key in LAP.items():
                if r.get('id') in C and r.get(key): S[s][r['id']][k] = r[key]
    for s, f in HOST.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            for x in json.load(open(p))['designs']:
                if x.get('id') in C and x.get('speed_here'): S[s][x['id']][k] = x['speed_here']
PARTS = {'x86-64': ('lap64', 'dream64'), 'x86-32': ('lap32', 'dream32'), 'ARMv7': ('rage',)}
lg = lambda v: [math.log(x) for x in v]
def cls(i, f):
    c = {}
    for k, ss in PARTS.items():
        if all(S[s][i] for s in ss): c[k] = statistics.fmean(f(lg(S[s][i].values())) for s in ss)
    if len(c) == 3: c['mean'] = statistics.fmean(c.values())
    return c
CM = {i: cls(i, statistics.fmean) for i in C}
CD = {i: cls(i, statistics.median) for i in C}
def paired(s, a, b):
    d = [math.log(S[s][a][k] / S[s][b][k]) for k in S[s][a] if k in S[s][b]]
    return statistics.fmean(d), statistics.stdev(d) / math.sqrt(len(d))
def diff(k, a, b):
    ks = list(PARTS) if k == 'mean' else [k]
    xs = [[paired(s, a, b) for s in PARTS[q]] for q in ks]
    cs = [(sum(m for m, _ in x) / len(x), math.sqrt(sum(e * e for _, e in x)) / len(x)) for x in xs]
    return sum(m for m, _ in cs) / len(cs), math.sqrt(sum(e * e for _, e in cs)) / len(cs)
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
free = [i for i in C if i not in jit]
print('# chain B judged beyond followup-roles.py (results/drafts/chainB-714.py): %d designs, %d JIT' % (len(C), len(jit)))
print('\n## 1. Each speed role\'s leader and the designs within 2 SE of it (paired; the mean over sessions, then the median)')
for name, pool, k in (('fastest portable', free, 'mean'), ('fastest on ARMv7', free, 'ARMv7'),
                      ('fastest on x86-64', list(C), 'x86-64'), ('fastest on x86-32', list(C), 'x86-32'),
                      ('best all-round', list(C), 'mean')):
    P = [i for i in pool if k in CM[i]]; b = min(P, key=lambda i: CM[i][k]); bd = min(P, key=lambda i: CD[i][k])
    near = []
    for i in sorted(P, key=lambda i: CM[i][k]):
        if i == b: continue
        m, se = diff(k, i, b)
        if m < 2 * se: near.append('%s%s %s +/- %.2f%%' % (i, ' JIT' if i in jit else '', pct(m), se * 100))
    print('  %s: %s %.4f (by the median %s%s); not separated: %s' % (name, b, math.exp(CM[b][k]), bd,
          '' if bd == b else ' %.4f, %s %s' % (math.exp(CD[bd][k]), b, pct(CD[b][k] - CD[bd][k])), '; '.join(near) or 'none'))
print('\n## 1b. The ties above and the lean end - size, memory and every class, each against the first, paired')
for grp in (('d727605472', '5f7e66b12d', '782f3ad7ff'), ('9b15ba26f7', '262a51bc6c', 'df097ba2e2', 'c7c35f9c97'),
            ('ea782c6094', 'b5c79bff7e', '69cebcaed9', '11f956db93', 'b525180392', '163935642a', 'ee34931cd7'),
            ('fb0d57c8a2', '71005d8a0d', '16560cb51f', '2c841d55e3', '25f49a31d5')):
    for i in grp:
        if i not in C: continue
        ks = [k for k in ('x86-64', 'x86-32', 'ARMv7', 'mean') if k in CM[i] and k in CM[grp[0]]]
        print('  %s%s %s B %d KB  %s' % (i, ' JIT' if i in jit else '', format(C[i]['total'], ','), C[i]['rss'], ', '.join(
            '%s %.4f%s' % (k, math.exp(CM[i][k]), '' if i == grp[0] else ' (%s +/- %.2f%%)' % (pct(diff(k, i, grp[0])[0]), diff(k, i, grp[0])[1] * 100))
            for k in ks)))
print('\n## 2. The smallest - the JIT-free designs up to 21,700 B, each against the smallest, by class')
sm = sorted((i for i in free if C[i]['total'] <= 21700 and 'mean' in CM[i]), key=lambda i: (C[i]['total'], CM[i]['mean']))
for i in sm:
    print('  %s %s B %d KB  %s' % (i, format(C[i]['total'], ','), C[i]['rss'], ', '.join(
        '%s %.4f' % (k, math.exp(CM[i][k])) for k in ('x86-64', 'x86-32', 'ARMv7', 'mean'))))
for i in sm[1:]:
    print('    %s against %s: %s' % (i, sm[0], ', '.join('%s %s +/- %.2f%%' % ((k,) + (pct(diff(k, i, sm[0])[0]),) + (diff(k, i, sm[0])[1] * 100,))
                                                       for k in ('x86-64', 'x86-32', 'ARMv7'))))
print('\n## 3. Stalls - readings more than 10 % off their design\'s median after the session\'s common shift')
for s in S:
    ids = [i for i in C if S[s][i]]; ks = sorted(set().union(*(S[s][i] for i in ids)))
    med = {i: statistics.median(lg(S[s][i].values())) for i in ids}
    sh = {k: statistics.median(math.log(S[s][i][k]) - med[i] for i in ids if k in S[s][i]) for k in ks}
    dev = [(math.log(S[s][i][k]) - med[i] - sh[k], i, k) for i in ids for k in S[s][i]]
    far = [x for x in dev if abs(x[0]) > math.log(1.10)]
    w = max(dev, key=lambda x: abs(x[0]))
    print('  %-8s %5d readings, %3d off by more than 10 %%; the worst %.3f (%s, session %d); the shifts %.3f-%.3f'
          % (s, len(dev), len(far), math.exp(w[0]), w[1], w[2], math.exp(min(sh.values())), math.exp(max(sh.values()))))
print('\n## 4. The laptop\'s machine line by step (the ticker, every 5 minutes)')
nr = sorted(glob.glob(os.path.join(out, '*-loadtest-*', 'pack', 'next-run.log')))[-1]
rx = re.compile(r'progress (\S+) - lab/evolve/(\S+) running; the machine: load ([\d.]+), ([\d.]+) GB free, swap ([\d.]+) GB, ([\d.]+) GHz, (\d+) C, (\S+)')
step, rows, cur = 0, {}, None
for l in open(nr, errors='replace'):
    if 'this step DONE' in l: step += 1; continue
    m = rx.search(l)
    if m: rows.setdefault(step, []).append(m.groups())
for k, v in sorted(rows.items()):
    ld = [float(x[2]) for x in v]; fr = [float(x[3]) for x in v]; gh = [float(x[5]) for x in v]; tc = [int(x[6]) for x in v]
    print('  step %2d %-15s %s-%s: %2d ticks, load %.2f mean / %.2f peak, free %.1f-%.1f GB, swap %s GB, %.2f-%.2f GHz, %d-%d C, %s'
          % (k + 1, v[0][1], v[0][0][:5], v[-1][0][:5], len(v), statistics.fmean(ld), max(ld), min(fr), max(fr),
             '/'.join(sorted(set(x[4] for x in v))), min(gh), max(gh), min(tc), max(tc), '/'.join(sorted(set(x[7] for x in v)))))
