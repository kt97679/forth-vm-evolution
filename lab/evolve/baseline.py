#!/usr/bin/env python3
"""lab/evolve/baseline.py DB --seed N [--ledger LEDGER] [--append] | --self-test - GOALS.md step 4, the random-search
baseline, set beside the method's runs (Iteration 573, prepared before seed 84 returned; the owner, Iteration 540).

The random run (`seed N HOURS widths noevolved random`: every child a fresh random genome, nothing learned in the loop)
reported as values, not a test - "what the article can say the evolutionary search itself contributed":
  1. Its true front's hypervolume in the fixed box and its four extremes from every alive design (hv.measure; as the
     series takes them since 556), at its last generation G.
  2. The series' runs (the ledger's newest series) at the same generation G - stopping.py's at(), each run's curve:
     the same number of children evaluated - and at their ends; each criterion's best, median and worst, and the random
     run's against the median (a ratio; the hypervolume larger is better, the rest smaller).
  3. The final front's check (the owner, 573: a random design on the final front joins the candidates): the pool -
     the series' results files and every confirmation run's (confirm.py's pool) - with the random run's true front
     added; the random designs on that union's true front, named.
  --append: a {"random": N, ...} line in the ledger - stopping.py's series() and confirm.py pass over it.
stdout: markdown. As the build user (it imports the evolver). --self-test: known answers on synthetic numbers.
"""
import json, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hv, stopping
import importlib.util
_s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)


def beside(run, others):
    """run: the random run's five numbers; others: the series' runs' five numbers each -> {criterion: (best, median,
    worst, the random run over the median)} - the hypervolume larger is better, the rest smaller."""
    out = {}
    for k in stopping.KEYS:
        v = [o[k] for o in others]
        best, worst = (max(v), min(v)) if k == 'hv' else (min(v), max(v))
        out[k] = (best, statistics.median(v), worst, run[k] / statistics.median(v))
    return out


def self_test():
    ok = True
    def check(c, what):
        nonlocal ok
        if not c: ok = False; print('baseline self-test: FAIL - %s' % what)
    S = [dict(hv=0.30, fastest=0.15, smallest=14000, memory=110, fastest32=0.17), dict(hv=0.34, fastest=0.14, smallest=14200, memory=108, fastest32=0.18),
         dict(hv=0.32, fastest=0.16, smallest=13900, memory=112, fastest32=0.16)]
    b = beside(dict(hv=0.16, fastest=0.32, smallest=16000, memory=120, fastest32=0.30), S)
    check(b['hv'][:3] == (0.34, 0.32, 0.30) and abs(b['hv'][3] - 0.5) < 1e-12, 'the hypervolume: best the largest, the ratio 0.5: %s' % (b['hv'],))
    check(b['fastest'][:3] == (0.14, 0.15, 0.16) and abs(b['fastest'][3] - 0.32 / 0.15) < 1e-12, 'the fastest: best the smallest: %s' % (b['fastest'],))
    run = dict(seed=1, hv=0.5, fastest=0.1, smallest=1, memory=1, fastest32=0.1, gens=100, curve=dict(hv=[[0, 0.1], [50, 0.3]], fastest=[[0, 0.9], [60, 0.2]]))
    a = stopping.at(run, 55)
    check(a['hv'] == 0.3 and a['fastest'] == 0.9 and a['smallest'] == 1, 'a series run at generation 55 by its curve: %s' % a)
    print('baseline self-test: best, median, worst and the ratio either way; a run at a generation - %s' % ('pass' if ok else 'FAIL'))
    return 0 if ok else 1


def main(a):
    opt = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    if a == ['--self-test']: return self_test()
    if opt('--seed') is None: sys.exit(__doc__)
    N = int(opt('--seed')); led = opt('--ledger') or stopping.LEDGER
    db = next(x for x in a if not x.startswith('--') and x not in (opt('--seed'), opt('--ledger')))
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS)); method, runs = stopping.series(led); runs = [r for r in runs if r['seed'] < N]
    R = hv.load(db, E); m = hv.measure(db, E, b, R=R); x = m['alive']; G = max((r.get('gen') or 0) for r in R.values())
    run = dict(hv=m['hv'], fastest=x['fastest'], smallest=x['smallest'], memory=x['memory'], fastest32=x['fastest32'])
    kids = [r for r in R.values() if (r.get('gen') or 0) >= 1]
    print('# The random-search baseline - seed %d beside the series, seeds %s (baseline.py; GOALS.md step 4)\n' % (N, ', '.join(str(r['seed']) for r in runs)))
    print('Seed %d: %d records, generations 0-%d, %d children (%d alive, %d random); its true front %d (%d inside the box). '
          'Values, not a test.\n' % (N, len(R), G, len(kids), sum(1 for r in kids if r.get('status') == 'ok'),
                                     sum(1 for r in kids if r.get('how') == 'random'), m['front'], m['inside']))
    for title, others in (('at generation %d - the same number of children' % G, [stopping.at(r, G) for r in runs]), ('at their ends', runs)):
        bs = beside(run, others)
        print('**The series %s** (%d runs):\n' % (title, len(others)))
        print('| criterion | seed %d, random | the series\' best | median | worst | random / median |' % N); print('|---|---|---|---|---|---|')
        for k in stopping.KEYS:
            print('| %s | %s | %s | %s | %s | %.3f |' % (stopping.NAME[k], stopping.fmt(k, run[k]), stopping.fmt(k, bs[k][0]), stopping.fmt(k, bs[k][1]),
                                                       stopping.fmt(k, bs[k][2]), bs[k][3]))
        print()
    pool = CF.pool_files([r for r in runs] + CF.confirmations(led, N))
    P = {}
    for f in pool: P.update(hv.load(f, E))
    T = hv.true_front(R, E)
    U = dict(P); U.update({i: R[i] for i in T if i not in P}); UF = hv.true_front(U, E)
    new = sorted(i for i in UF if i in T and i not in P)
    print('The final front (the pool of %d results files, %s, with seed %d\'s true front): %d designs; seed %d\'s on it: %s.' % (
        len(pool), ', '.join(os.path.basename(f).split('-')[-1].replace('.md', '') for f in pool), N, len(UF), N,
        '%d - %s - each joins the final set\'s candidates (573)' % (len(new), ', '.join(new)) if new else 'none'))
    if '--append' in a:
        if any(l.startswith('{') and json.loads(l).get('random') == N for l in open(led)): print('baseline.py: the ledger has seed %d already' % N)
        else:
            with open(led, 'a') as o:
                o.write(json.dumps(dict(random=N, gens=G, front=m['front'], hv=round(m['hv'], 6), fastest=round(run['fastest'], 6),
                                        smallest=run['smallest'], memory=run['memory'], fastest32=round(run['fastest32'], 6), final=new)) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
