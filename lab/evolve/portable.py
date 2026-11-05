#!/usr/bin/env python3
"""lab/evolve/portable.py DB --seed N [--ledger LEDGER] [--append] - the portable run beside the portable designs found
before it (Iteration 602; results/drafts/portable-plan-602.md, the owner: "let's find best portable design and see if it
would be better than what we already found"). The run: `seed N nojit HOURS widths` - every design without the JIT.

  1. The run's true front, its hypervolume in the fixed box and its four extremes from every alive design (hv.measure,
     as the series since 556) - and a check: no alive design of the run expresses the JIT.
  2. What was found before it: the pool's portable designs - confirm.py's pool (the series' results files and every
     confirmation run's) without the JIT, and the final set's 7 portable designs (in-run numbers) - measured the same way
     (its true front: results/portable-front-seed86.md) - and (Iteration 613) every earlier portable run's designs, the
     ledger's {"portable": K} lines with K < N (confirm.py's pool passes over them): seed 87's in seed 88's pool, its
     results file's front and its ledger line's extremes (from every alive design - the file holds the front only).
  3. The verdict, by the stopping rule's own effect sizes (GOALS.md), fixed before the run: BETTER when the run's
     hypervolume beats the portable pool's by 1% or more, or an extreme does by its threshold - speed 2%, binary + image
     1%, memory 4 KB, the 32-bit speed 2%; else NOT BETTER. In-run numbers against in-run numbers, as the series is
     judged - the decisive comparison is the re-measure after (the plan's follow-up chain), so the run's designs on the
     union's true front are named: they join the portable candidates either way.
--append: a {"portable": N, ...} line in the ledger (default results/stopping-series.md) - stopping.py's series() and
confirm.py read only their own lines and pass over it. --front OUT --seed N (613; no DB): what was found before seed N
written to OUT - the true front of that pool, and the final set's portable designs whether on it or not, in-run numbers,
one record a line (results/portable-front-seed87.md: before seed 88). As the build user (it imports the evolver)."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
a = sys.argv[1:]
if not a or '--seed' not in a: sys.exit(__doc__)
N = int(a[a.index('--seed') + 1]); led = a[a.index('--ledger') + 1] if '--ledger' in a else os.path.join(HERE, '..', '..', 'results', 'stopping-series.md')
app = '--append' in a; out = a[a.index('--front') + 1] if '--front' in a else None
db = None if a[0].startswith('--') else a[0]
if not db and not out: sys.exit(__doc__)
sys.argv = ['x']; import evolve as E
import hv, stopping
_s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)
jit = lambda r: bool(E.express(E.canon(r['genome'])).get('jit'))
R = hv.load(db, E) if db else {}
bad = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('genome') and jit(r) and not str(r.get('how', '')).startswith('hand-made')]
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < N]
P = {}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, N)): P.update(hv.load(f, E))
LP = [x for x in (json.loads(l) for l in open(stopping.LEDGER) if l.startswith('{"portable"')) if x['portable'] < N]
PR = sorted(x['portable'] for x in LP)
for f in CF.pool_files([{'seed': k} for k in PR]): P.update(hv.load(f, E))       # 613: the earlier portable runs
Q = {i: r for i, r in P.items() if r.get('genome') and not jit(r)}
FS = os.path.join(HERE, '..', '..', 'results', 'final-set-chainsBCD-seed86.md')   # the final set's portable designs too, in-run:
FSP = []
for l in open(FS):                                     # fb0d57c8a2 (104 KB) is seed 76's, outside the series' pool
    if l.startswith('{'):
        x = json.loads(l)
        if not jit(x): Q.setdefault(x['id'], dict(x, speed=x.get('inrun') or x['speed'], speed32=x.get('inrun32') or x['speed32'])); FSP.append(x['id'])
if out:                                                # 613: what was found before seed N, as a file
    F = list(dict.fromkeys(list(hv.true_front(Q, E)) + [i for i in FSP if i in Q]))
    with open(out, 'w') as o:
        o.write('# The portable designs found before seed %d (lab/evolve/portable.py --front, Iteration 613): every design without\n'
                '# the JIT on the true front of confirm.py\'s pool (the series and confirmation runs), the earlier portable runs\'\n'
                '# (seeds %s) and the final set\'s portable designs - those kept whether on it or not. In-run numbers, one record a\n'
                '# line: %d designs.\n\n' % (N, ', '.join(map(str, PR)) or 'none', len(F)))
        for i in sorted(F, key=lambda i: (Q[i]['speed'], i)): o.write(json.dumps(Q[i], sort_keys=True) + '\n')
    print('portable.py --front: %d designs found before seed %d (pool %d without the JIT; portable runs %s) -> %s' % (len(F), N, len(Q), PR or 'none', out))
    sys.exit(0)
b = json.load(open(hv.BOUNDS))
run, pool = hv.measure(None, E, b, R={i: r for i, r in R.items() if not (r.get('genome') and jit(r))}), hv.measure(None, E, b, R=Q)
for x in LP:   # 613: an earlier portable run's extremes from every alive design (its ledger line); its results file holds only
    q = pool['alive']   # its front - seed 87's fastest at 32 bits 0.2888 there, 0.2947 on its front
    for k in ('fastest', 'smallest', 'memory', 'fastest32'): q[k] = min(q[k], x[k])
U = dict(Q); U.update({i: r for i, r in R.items() if not (r.get('genome') and jit(r))})
on = [i for i in hv.true_front(U, E) if i in R and i not in Q]
print('# The portable run, seed %d, beside the portable designs found before it (lab/evolve/portable.py)\n' % N)
print('The run: %d records, alive designs with the JIT expressed: %d%s.' % (len(R), len(bad), ' - NOT a portable run' if bad else ''))
print('Before it: confirm.py\'s pool and the earlier portable runs\' (seeds %s), %d designs, and the final set\'s portable ones - %d without the JIT.\n' % (', '.join(map(str, PR)) or 'none', len(P), len(Q)))
print('| | true front | inside the box | hypervolume | fastest | smallest | least memory KB | fastest at 32 bits |')
print('|---|---|---|---|---|---|---|---|')
for n, m in (('the portable run', run), ('the portable pool', pool)):
    x = m['alive']
    print('| %s | %d | %d | %.6f | %.4f | %s | %d | %.4f |' % (n, m['front'], m['inside'], m['hv'], x['fastest'], format(x['smallest'], ','), x['memory'], x['fastest32']))
r, p = run['alive'], pool['alive']
gain = [w for w, ok in (('hypervolume +%.1f%%' % ((run['hv'] / pool['hv'] - 1) * 100), run['hv'] >= pool['hv'] * 1.01),
                        ('fastest %.4f against %.4f' % (r['fastest'], p['fastest']), r['fastest'] <= p['fastest'] * 0.98),
                        ('smallest %d against %d' % (r['smallest'], p['smallest']), r['smallest'] <= p['smallest'] * 0.99),
                        ('least memory %d against %d KB' % (r['memory'], p['memory']), r['memory'] <= p['memory'] - 4),
                        ('fastest at 32 bits %.4f against %.4f' % (r['fastest32'], p['fastest32']), r['fastest32'] <= p['fastest32'] * 0.98)) if ok]
verdict = 'BETTER - ' + '; '.join(gain) if gain else 'NOT BETTER - no criterion by its threshold (hypervolume %+.1f%%)' % ((run['hv'] / pool['hv'] - 1) * 100)
print('\nverdict (in-run, the stopping rule\'s thresholds): %s' % verdict)
print('The run\'s designs on the union\'s true front: %d - the portable candidates for the re-measure; the fastest ten: %s' % (
      len(on), ', '.join('%s %.4f' % (i, R[i]['speed']) for i in sorted(on, key=lambda i: R[i]['speed'])[:10])))
if app:
    if any(l.startswith('{') and json.loads(l).get('portable') == N for l in open(led)): print('portable.py: the ledger has seed %d already' % N)
    else:
        open(led, 'a').write(json.dumps(dict(portable=N, front=run['front'], hv=round(run['hv'], 6), fastest=r['fastest'], smallest=r['smallest'],
                             memory=r['memory'], fastest32=r['fastest32'], pool=dict(hv=round(pool['hv'], 6), **p), on_union=len(on),
                             verdict=verdict.split(' - ')[0])) + '\n')
        print('portable.py: appended to %s' % led)
