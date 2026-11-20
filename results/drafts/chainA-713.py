#!/usr/bin/env python3
"""results/drafts/chainA-713.py LIST SESSIONS - chain A's predictions (results/predictions.md, Iteration 705) scored on the
laptop's readings: (2) the in-run fastest tenth's median re-measured (alone, 8-byte cells) / in-run; (3) the best new design
against c7c35f9c97 and (4) the best JIT-free one against 782f3ad7ff, the laptop alone at 8-byte cells, paired by session
(the geometric mean over the sessions; the SE of the paired log differences). LIST: results/followup-seed96-roles.md;
SESSIONS: results/chain-followup96-roles. JIT: the JIT expressed (followup-roles.py's test, 713)."""
import glob, json, math, os, statistics, sys

lst, ses = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
hold = {i for i in C if str(C[i].get('why', '')).startswith('a holder')}
jit = {i for i in C if E.express(E.canon(C[i]['genome'])).get('jit')}
S = []                                                   # per session: id -> loadtest line
for d in sorted(glob.glob(os.path.join(ses, 's[0-9]*')), key=lambda d: int(d.rsplit('s', 1)[1])):
    p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        S.append({r['id']: r for r in (json.loads(l) for l in open(p) if l.startswith('{"'))})
print('%d designs (%d holders, %d JIT); the laptop %d sessions' % (len(C), len(hold), len(jit), len(S)))
gm = lambda xs: math.exp(statistics.fmean(math.log(x) for x in xs))
def mean(i, k='idle'): return gm([s[i][k] for s in S if i in s and s[i].get(k)])
def pair(x, y, k='idle'):
    d = [math.log(s[x][k] / s[y][k]) for s in S if x in s and y in s and s[x].get(k) and s[y].get(k)]
    return math.exp(statistics.fmean(d)) - 1, statistics.stdev(d) / math.sqrt(len(d)), len(d)
inrun = {i: S[0][i]['inrun'] for i in C if i in S[0] and S[0][i].get('inrun')}
top = sorted((i for i in inrun if i not in hold), key=inrun.get)[:len(inrun) // 10]
r = [mean(i) / inrun[i] for i in top]
print('(2) the in-run fastest tenth (%d, holders out): median re-measured / in-run %.3f (quartiles %.3f-%.3f); at 32 bits %.3f'
      % (len(top), statistics.median(r), *statistics.quantiles(r, n=4)[::2],
         statistics.median(mean(i, 'idle32') / S[0][i]['inrun32'] for i in top if S[0][i].get('inrun32'))))
for n, (h, pool) in (('3', ('c7c35f9c97', [i for i in C if i not in hold])),
                     ('4', ('782f3ad7ff', [i for i in C if i not in hold and i not in jit]))):
    best = sorted(pool, key=mean)[:5]
    print('(%s) against %s (%.4f, the laptop alone, 8-byte cells):' % (n, h, mean(h)))
    for i in best:
        g, se, k = pair(i, h)
        print('    %s%s %.4f  %+.2f%% +/- %.2f%% (%d sessions)' % (i, ' JIT' if i in jit else '', mean(i), 100 * g, 100 * se, k))
