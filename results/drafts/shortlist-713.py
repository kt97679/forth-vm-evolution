#!/usr/bin/env python3
"""results/drafts/shortlist-713.py LIST SESSIONS FPSHORT SIZES OUT OUTARM [POOLSIZES] - chain B's designs (the new-roles plan's step 2,
results/drafts/new-roles-plan-705.md): final-pick.py's shortlist (FPSHORT, --n 40), the ten holders, and each role's
leaders on its own lines, pooled as followup-roles.py pools (each source's geometric mean over its sessions; x86-64 the
laptop alone and dream, x86-32 likewise, ARMv7 the Tegra; the mean of the three):
  the fastest portable - the 5 best JIT-free means; ARMv7 - the 5 fastest JIT-free; the knee and small, fast on ARMv7 -
  followup-roles.py's role() contenders (any class 2 % better or 1 % smaller, none as much worse) and the pool's knee
  bee5d0daa2; least memory - the 5 fastest JIT-free at the holder's memory or less; x86-64, x86-32 and the best mean -
  the 5 best over every design; the smallest - the 5 best means among the JIT-free designs within 0.1 % of the smallest after the batch;
  the smallest JIT design - the 3 smallest JIT designs after the batch and those within 10 % of the holder's x86-64.
  And (713, the owner: "ensure we are not losing good designs") the near-ties - every design within NEAR (1.5 %) of a
  speed role's best, the sessions pooled by the geometric mean and by the median; and with POOLSIZES (sizes-713.py over
  the results files' small end: results/drafts/sizes-pool-713.json) every pool design off LIST smaller after the batch
  than all LIST's measured JIT-free designs, its record from its results file (219878ec89: fbuf=2's engine 16 B more).
SIZES: results/drafts/sizes-713.py's JSON (the batch's sizes at 8-byte cells - the size roles use them, and OUT's records
carry them: bin and total; image and the programs' code unchanged by the batch). Without a size for a chosen design it
prints the ids missing and writes nothing (sizes-713.py --ids, then again). OUT: one record a line (loadtest.py --ids,
xcheck.py --also @); OUTARM: its JIT-free designs and the JIT designs among the across-machines leaders (their JIT-off
builds there, as chain A's -arm list)."""
import glob, json, math, os, statistics, sys

lst, ses, fps, szf, out, outarm = sys.argv[1:7]
POOL = sys.argv[7] if len(sys.argv) > 7 else None      # 713: sizes-713.py's JSON over the results files' small end
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
SZ = json.load(open(szf))
EXTRA = {}                                               # pool designs off LIST smaller, after the batch, than all LIST's
if POOL:
    PS = json.load(open(POOL)); m0 = min(v['total'] for i, v in SZ.items() if 'total' in v and i in C and not v.get('jit'))
    ex = {i for i, v in PS.items() if 'total' in v and not v.get('jit') and v['total'] < m0 and i not in C}
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(lst)), 'evolve-amd-ryzen-7-pro-8840hs-seed9[2-6].md'))):
        for l in open(f):
            if l.startswith('{"') and '"genome"' in l:
                r = json.loads(l)
                if r['id'] in ex and r['id'] not in EXTRA: EXTRA[r['id']] = (r, os.path.basename(f))
    for i, (r, f) in EXTRA.items(): C[i] = r; SZ[i] = PS[i]
    print('shortlist-713: %d pool designs below %d B after the batch, off chain A\'s list: %s' % (len(EXTRA), m0, ' '.join(sorted(EXTRA))))
jit = {i: bool(E.express(E.canon(C[i]['genome'])).get('jit')) for i in C}
HOLD = dict(fastest='782f3ad7ff', arm='3eb59b271d', knee='11a56ff9e4', smallarm='ae99617f06', memory='fb0d57c8a2',
            smallest='d180351903', fast64='c7c35f9c97', fast32='ee34931cd7', allround='06b188f45b', smalljit='c6f1c1331b')
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
src = {k: {} for k in ('lap64', 'lap32', 'dream64', 'dream32', 'rage')}
for d in glob.glob(os.path.join(ses, 's[0-9]*')):
    p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
            if r.get('idle'): src['lap64'].setdefault(r['id'], []).append(r['idle'])
            if r.get('idle32'): src['lap32'].setdefault(r['id'], []).append(r['idle32'])
    for k, f in HOST.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            for x in json.load(open(p))['designs']:
                if x.get('id') in C and x.get('speed_here'): src[k].setdefault(x['id'], []).append(x['speed_here'])
gm = lambda xs: math.exp(statistics.fmean(math.log(x) for x in xs))
S = {k: {i: gm(v) for i, v in d.items()} for k, d in src.items()}
CL = {}
for i in C:
    c = {}
    if i in S['lap64'] and i in S['dream64']: c['x86-64'] = gm([S['lap64'][i], S['dream64'][i]])
    if i in S['lap32'] and i in S['dream32']: c['x86-32'] = gm([S['lap32'][i], S['dream32'][i]])
    if i in S['rage']: c['ARMv7'] = S['rage'][i]
    if len(c) == 3: c['mean'] = gm(list(c.values()))
    CL[i] = c
tot = lambda i: SZ[i]['total'] if i in SZ and 'total' in SZ[i] else C[i]['total']
free = [i for i in C if not jit[i]]
pick = {}                                                 # id -> why (the first reason kept)
def add(i, why):
    if i not in pick: pick[i] = why
for l in open(fps):
    if l.startswith('{"'):
        r = json.loads(l); add(r['id'], 'final-pick.py --shortlist: ' + r['why'])
for role, i in HOLD.items(): add(i, 'a holder: ' + role)
def best(pool, k, n):
    return sorted((i for i in pool if k in CL[i]), key=lambda i: CL[i][k])[:n]
for i in best(free, 'mean', 5): add(i, 'the fastest portable: among the 5 best JIT-free means')
for i in best(free, 'ARMv7', 5): add(i, 'the fastest on ARMv7: among the 5 fastest JIT-free')
for i in best(C, 'x86-64', 5): add(i, 'the fastest on x86-64: among the 5 fastest')
for i in best(C, 'x86-32', 5): add(i, 'the fastest on x86-32: among the 5 fastest')
for i in best(C, 'mean', 5): add(i, 'best all-round: among the 5 best means')
# Iteration 713, the owner: "ensure we are not losing good designs" - the near-ties: every design within NEAR (1.5 %, about
# 2-3 SE of chain A's paired differences) of a speed role's best, the classes pooled by the geometric mean and again by
# the median (robust to one odd session: the Tegra's 3 sessions move a mean ~5 % on one 1.16 reading); 22 at 1.5 %,
# among them the median's best portable 25a6fc9a9e, off the 5 best means
NEAR = float(os.environ.get('NEAR', '0.015'))
def pooled(f):
    T = {k: {i: f(v) for i, v in d.items()} for k, d in src.items()}; R = {}
    for i in C:
        c = {}
        if i in T['lap64'] and i in T['dream64']: c['x86-64'] = gm([T['lap64'][i], T['dream64'][i]])
        if i in T['lap32'] and i in T['dream32']: c['x86-32'] = gm([T['lap32'][i], T['dream32'][i]])
        if i in T['rage']: c['ARMv7'] = T['rage'][i]
        if len(c) == 3: c['mean'] = gm(list(c.values()))
        R[i] = c
    return R
for how, CX in (('mean', CL), ('median', pooled(statistics.median))):
    for name, pool, k in (('the fastest portable', free, 'mean'), ('the fastest on ARMv7', free, 'ARMv7'),
                          ('the fastest on x86-64', list(C), 'x86-64'), ('the fastest on x86-32', list(C), 'x86-32'),
                          ('best all-round', list(C), 'mean')):
        P = [i for i in pool if k in CX[i]]; b = min(CX[i][k] for i in P)
        for i in sorted(P, key=lambda i: CX[i][k]):
            if CX[i][k] > b * (1 + NEAR): break
            add(i, '%s: within %.1f%% of the best (%+.2f%%, the sessions pooled by the %s)' % (name, NEAR * 100, (CX[i][k] / b - 1) * 100, how))
def role(inc, keys, name, T=0.02, B=0.01):
    for i in sorted(free, key=tot):
        if i == inc or not all(k in CL[i] for k in keys): continue
        r = {k: CL[i][k] / CL[inc][k] - 1 for k in keys}; r['bytes'] = tot(i) / tot(inc) - 1
        th = dict({k: T for k in keys}, bytes=B)
        if any(r[k] <= -th[k] for k in r) and all(r[k] < th[k] for k in r):
            add(i, '%s: beats the holder by the rule (%s)' % (name, ', '.join('%s %+.1f%%' % (k, v * 100) for k, v in r.items())))
role(HOLD['knee'], ('x86-64', 'x86-32'), 'the knee'); add('bee5d0daa2', 'the knee: the pool\'s')
role(HOLD['smallarm'], ('ARMv7',), 'small, fast on ARMv7')
lean = [i for i in free if C[i]['rss'] <= C[HOLD['memory']]['rss'] and 'x86-64' in CL[i]]
for i in sorted(lean, key=lambda i: CL[i]['x86-64'])[:5]: add(i, 'least memory: at the holder\'s %d KB, among the 5 fastest' % C[HOLD['memory']]['rss'])
for i, (r, f) in sorted(EXTRA.items(), key=lambda x: tot(x[0])):
    add(i, 'the smallest: %d B after the batch (%d before), below every design chain A measured - off its list, from %s '
        '(713: sizes-pool-713.json)' % (tot(i), r['total'], f))
fs = [i for i in free if i in SZ and 'total' in SZ[i] and 'mean' in CL[i]]; m = min(tot(i) for i in fs)
for i in sorted((i for i in fs if tot(i) <= m * 1.001 and 'mean' in CL[i]), key=lambda i: CL[i]['mean'])[:5]:
    add(i, 'the smallest: among the 5 best means within 0.1%% of %d B after the batch' % m)
js = [i for i in C if jit[i] and i in SZ and 'total' in SZ[i]]
for i in sorted(js, key=tot)[:3]: add(i, 'the smallest JIT design: among the 3 smallest after the batch')
h = HOLD['smalljit']
for i in js:
    if tot(i) < tot(h) and 'x86-64' in CL[i] and CL[i]['x86-64'] <= CL[h]['x86-64'] * 1.10:
        add(i, 'the smallest JIT design: smaller than the holder after the batch, within 10% of its x86-64')
miss = [i for i in pick if i not in SZ or 'total' not in SZ[i]]
print('shortlist-713: %d designs (%d JIT-free, %d JIT)' % (len(pick), sum(not jit[i] for i in pick), sum(jit[i] for i in pick)))
if miss: sys.exit('shortlist-713: no size after the batch for %d: --ids %s' % (len(miss), ','.join(miss)))
arm = [i for i in pick if not jit[i] or pick[i].startswith(('final-pick.py --shortlist: across machines', 'best all-round', 'a holder: allround'))]
head = ('# Chain B - the new roles\' shortlist (Iteration 713; results/drafts/shortlist-713.py)\n\n'
        'From chain A\'s readings (results/chain-followup96-roles: the laptop 5 sessions, dream 8 a width, the Tegra 3): '
        'final-pick.py\'s shortlist (40), the ten holders, each role\'s leaders (the docstring). The sizes are master\'s after '
        'the after-seed-96 batch (bin and total at 8-byte cells, results/drafts/sizes-713.py); memory as chain A\'s records. '
        'Read by measure-ids.py --ids, loadtest.py --ids and xcheck.py --also @FILE - one record a line.\n\n')
for f, ids, what in ((out, list(pick), 'every design'), (outarm, arm, 'the Tegra\'s: the JIT-free and the JIT designs leading across machines (their JIT-off builds)')):
    with open(f, 'w') as o:
        o.write(head + '%s - %d designs.\n\n' % (what, len(ids)))
        for i in ids:
            r = dict(C[i], why=pick[i], bin=SZ[i]['bin'], total=SZ[i]['total'], before_batch=SZ[i]['before'])
            o.write(json.dumps(r, sort_keys=True) + '\n')
    print('shortlist-713: %s - %d' % (f, len(ids)))
for i in pick: print('  %s %s %6d B  %s' % (i, 'JIT ' if jit[i] else 'free', tot(i), pick[i][:110]))
