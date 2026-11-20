#!/usr/bin/env python3
# results/drafts/neartie-chainA-713.py REPO - designs off chain B's list within TOL (env, 0.015) of a speed role's best in chain A, pooled by the mean and by the median (Iteration 713: 22)
import glob, json, math, os, statistics, sys
ROOT = sys.argv[1]; os.chdir(ROOT)
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open('results/followup-seed96-roles.md') if l.startswith('{"'))}
SL = {json.loads(l)['id'] for l in open('results/followup-seed96-roles-b.md') if l.startswith('{"')}
jit = {i: bool(E.express(E.canon(C[i]['genome'])).get('jit')) for i in C}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
src = {k: {} for k in ('lap64', 'lap32', 'dream64', 'dream32', 'rage')}
for d in glob.glob('results/chain-followup96-roles/s[0-9]*'):
    s = int(d.rsplit('s', 1)[1]); p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
            for k, f in (('lap64', 'idle'), ('lap32', 'idle32')):
                if r.get(f): src[k].setdefault(r['id'], {})[s] = r[f]
    for k, f in HOST.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            for x in json.load(open(p))['designs']:
                if x.get('id') in C and x.get('speed_here'): src[k].setdefault(x['id'], {})[s] = x['speed_here']
gm = lambda xs: math.exp(statistics.fmean(math.log(x) for x in xs))
def classes(pool):
    S = {k: {i: pool(list(v.values())) for i, v in d.items()} for k, d in src.items()}
    CL = {}
    for i in C:
        c = {}
        if i in S['lap64'] and i in S['dream64']: c['x86-64'] = gm([S['lap64'][i], S['dream64'][i]])
        if i in S['lap32'] and i in S['dream32']: c['x86-32'] = gm([S['lap32'][i], S['dream32'][i]])
        if i in S['rage']: c['ARMv7'] = S['rage'][i]
        if len(c) == 3: c['mean'] = gm(list(c.values()))
        CL[i] = c
    return CL
free = [i for i in C if not jit[i]]
ROLES = [('fastest portable (mean, JIT-free)', free, 'mean'), ('fastest on ARMv7 (JIT-free)', free, 'ARMv7'),
         ('fastest on x86-64', list(C), 'x86-64'), ('fastest on x86-32', list(C), 'x86-32'), ('best all-round (mean)', list(C), 'mean')]
TOL = float(os.environ.get('TOL', '0.015'))
miss = {}
for name, pf in (('geometric mean', gm), ('median', statistics.median)):
    CL = classes(pf)
    print('## pooled by the %s - designs off the shortlist within %.1f %% of a role\'s best' % (name, TOL * 100))
    for role, pool, k in ROLES:
        P = sorted((i for i in pool if k in CL[i]), key=lambda i: CL[i][k]); b = CL[P[0]][k]
        near = [i for i in P if CL[i][k] <= b * (1 + TOL)]
        off = [i for i in near if i not in SL]
        print('  %-36s best %s %.4f%s; within: %d, off the shortlist %d%s' % (role, P[0], b, '' if P[0] in SL else ' (OFF)',
              len(near), len(off), (': ' + ', '.join('%s %+.2f%%' % (i, (CL[i][k] / b - 1) * 100) for i in off[:8])) if off else ''))
        for i in off: miss.setdefault(i, set()).add(role)
print('\n%d designs off the shortlist within %.1f %% of some role\'s best: %s' % (len(miss), TOL * 100, ' '.join(sorted(miss))))
json.dump({i: sorted(v) for i, v in miss.items()}, open('/tmp/neartie-chainA.json', 'w'), indent=0)
