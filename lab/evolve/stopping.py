#!/usr/bin/env python3
"""lab/evolve/stopping.py DB --seed N [--ledger LEDGER] [--append] | --self-test - GOALS.md's stopping rule, mechanical
(Iteration 554; prompts/21, item 9: the rule's arithmetic a script, the judgment the chat's - seed 75 was judged by its
hypervolume alone at first, and the gain its fastest made missed).

A run's numbers - its true front's fixed-box hypervolume and four extremes, from its own database (hv.py's measure(), the
box hv-bounds.json) - against the method's earlier runs in the ledger (results/stopping-series.md): the run gains when
its hypervolume beats the best earlier one by 1% or more, or an extreme beats the best earlier one by its threshold -
speed 2%, binary + image 1%, memory 4 KB, the 32-bit speed 2% - each criterion against its own best (the pooled
reading, as GOALS.md words the confirmation test: "the pooled true front"). Stop when, after at least three runs on the
method, the last two gain nothing - and no correctness issue is open, which is the chat's to say. The ledger: a
{"method": ...} line opens a series (a method change restarts the count), then a line a run; the earlier runs are the
newest series' runs before seed N; --append adds this run's line. stdout: the series, the verdict, the count, the bar.
A method line with "extremes": "alive" takes the four extremes from every alive design - the strict front's - and not
the true front's, whose tolerance dominance can lose the fastest to a chain (Iteration 556: seed 76's, 105 designs).
A method line with "matched": true (Iteration 562 - the owner's hours vary, so they are no part of the method) judges each
run at its last generation against each earlier run's numbers at that generation - the thresholds adjusted to the run's
length by the earlier run's own record: its "curve" - the four extremes (every alive design's) exact at every generation
where they moved, the hypervolume every 10 generations (a true front costs up to 34 s); between two hypervolume points
its earlier one. An earlier run shorter than this one is taken at its end. Both favour a gain: an error continues the
phase rather than ends it. --curve FILE computes the curve alone (minutes - process-run.sh does it, detached); --append
takes it from FILE when it is this seed's, else computes it. "the next run gains if" depends on how far the next run goes.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'results', 'stopping-series.md')
KEYS = ('hv', 'fastest', 'smallest', 'memory', 'fastest32')
NAME = dict(hv='the hypervolume', fastest='the fastest', smallest='the smallest', memory='the least memory',
            fastest32='the fastest at 32 bits')


def bar(runs):
    """What a run must reach to gain over these runs, criterion by criterion (GOALS.md's thresholds)."""
    return dict(hv=max(r['hv'] for r in runs) * 1.01, fastest=min(r['fastest'] for r in runs) * 0.98,
                smallest=min(r['smallest'] for r in runs) * 0.99, memory=min(r['memory'] for r in runs) - 4,
                fastest32=min(r['fastest32'] for r in runs) * 0.98)


def at(run, g):
    """A run's numbers at generation g (562): each criterion's last curve point at or before g (its first, when g is
    before them all); at or past its end, or with no curve or no g, its end."""
    c = run.get('curve')
    if not c or g is None or g >= run.get('gens', 10 ** 9): return run
    out = dict(run)
    for k in KEYS:
        pts = c.get(k) or []
        if pts: out[k] = ([v for x, v in pts if x <= g] or [pts[0][1]])[-1]
    return out


def curve(db, E, hv, R, gens):
    """A run's curve (562): the extremes over every alive design where they moved, generation by generation, and the
    hypervolume every 10 generations."""
    F = dict(fastest='speed', smallest='total', memory='rss', fastest32='speed32'); c = {k: [] for k in F}; best = {}
    A = sorted((r for r in R.values() if r.get('status') == 'ok' and all(r.get(f) for f in F.values())), key=lambda r: r.get('gen') or 0)
    for r in A:
        g = r.get('gen') or 0
        for k, f in F.items():
            if k not in best or r[f] < best[k]:
                best[k] = r[f]; v = round(r[f], 6) if k.startswith('fastest') else r[f]
                if c[k] and c[k][-1][0] == g: c[k][-1][1] = v
                else: c[k].append([g, v])
    c['hv'] = [[g, round(hv.measure(db, E, gen=g, R=R)['hv'], 6)] for g in range(10, gens, 10)]
    return c


def gains(run, earlier):
    """The criteria a run gains on over the earlier runs; None for a series' first run - nothing to beat. A run with its
    last generation ("gens") meets each earlier run at that generation (at())."""
    if not earlier: return None
    b = bar([at(k, run.get('gens')) for k in earlier])
    return [k for k in KEYS if (run[k] >= b[k] if k == 'hv' else run[k] <= b[k])]


def stop(runs):
    """GOALS.md: at least three runs on the method, the last two gaining nothing."""
    return len(runs) >= 3 and gains(runs[-1], runs[:-1]) == [] and gains(runs[-2], runs[:-2]) == []


def earliest(runs):
    """The seed after which the count can end at the earliest, if every run from the next on gains nothing."""
    if stop(runs): return runs[-1]['seed']
    k = 1 if len(runs) >= 2 and gains(runs[-1], runs[:-1]) == [] else 2
    while len(runs) + k < 3: k += 1
    return runs[-1]['seed'] + k


def series(path):
    """The ledger's newest series: its method line, and its runs in order."""
    method, runs = {}, []
    for l in open(path):
        if l.startswith('{'):
            r = json.loads(l)
            if 'method' in r: method, runs = r, []
            elif 'seed' in r: runs.append(r)
    return method, runs


def fmt(k, v):
    if k == 'hv': return '%.5f' % v
    if k in ('fastest', 'fastest32'): return '%.4f' % v
    if k == 'smallest': return '{:,}'.format(int(round(v)))
    return '%d KB' % round(v)


def report(run, method, runs):
    S = [r for r in runs if r['seed'] < run['seed']] + [run]
    out = ["the stopping rule (GOALS.md) on the method %s - each run against the best of the method's earlier runs, "
           "criterion by criterion%s" % (method.get('method', '(no method line)'), '; the extremes from every alive design' if method.get('extremes') == 'alive' else ''), '',
           '| seed | front | hypervolume | fastest | smallest | least memory | fastest at 32 bits | gains |',
           '|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(S):
        g = gains(r, S[:i])
        out.append('| %s | %s | %s | %s |' % ('%s (to %s)' % (r['seed'], r['gens']) if 'gens' in r else r['seed'], r.get('front', '-'), ' | '.join(fmt(k, r[k]) for k in KEYS),
                   'the first' if g is None else ', '.join(NAME[k] for k in g) if g else 'nothing'))
    g = gains(run, S[:-1]); out.append('')
    if g is None: out.append('verdict: seed %d opens the series - nothing earlier to gain on' % run['seed'])
    else:
        b = {k: (max if k == 'hv' else min)(at(r, run.get('gens'))[k] for r in S[:-1]) for k in KEYS}
        ch = lambda k: '%+d KB' % round(run[k] - b[k]) if k == 'memory' else '%+.1f%%' % (100 * (run[k] / b[k] - 1))
        out.append('verdict: seed %d%s %s - %s' % (run['seed'], ' (at its last generation, %d - the earlier runs there too)' % run['gens'] if method.get('matched') and 'gens' in run else '', 'GAINS, by %s' % ' and '.join(NAME[k] for k in g) if g else
                   'gains nothing', '; '.join('%s %s against %s (%s%s)' % (NAME[k], fmt(k, run[k]), fmt(k, b[k]), ch(k),
                   ', past its threshold' if k in g else '') for k in KEYS)))
    out.append('the count: %d run(s) on the method; %s' % (len(S), 'STOP - three runs or more, the last two gaining nothing '
               '(if no correctness issue is open)' if stop(S) else 'the earliest stop after seed %d, if every run until '
               'then gains nothing' % earliest(S)))
    if method.get('matched'):                   # 562: the bar moves with the next run's length
        out.append('the next run gains if, by its last generation: ' + '; '.join('%d - %s' % (G, ', '.join('%s %s' % (
            '>=' if k == 'hv' else '<=', fmt(k, nb[k])) for k in KEYS)) for G in (80, 100, 120, 140, 160)
            for nb in [bar([at(x, G) for x in S])]) + ' (hypervolume, fastest, smallest, memory, 32-bit)')
    else:
        nb = bar(S)
        out.append('the next run gains if: ' + ', '.join('%s %s %s' % (NAME[k], '>=' if k == 'hv' else '<=', fmt(k, nb[k])) for k in KEYS))
    return '\n'.join(out)


def self_test():
    a = dict(seed=1, hv=0.35, fastest=0.14, smallest=14000, memory=112, fastest32=0.17)
    def r(seed, **k): x = dict(a, seed=seed); x.update(k); return x
    b = r(2, fastest=0.1371)                   # 2.1% faster than a: a gain
    c = r(3, fastest=0.1350, hv=0.3534)        # 1.5% faster than b, 0.97% above a's hypervolume: nothing
    d = r(4, smallest=13870)                   # 0.93% smaller: nothing
    e = r(5, memory=108)                       # 4 KB less: a gain
    checks = [gains(a, []) is None, gains(b, [a]) == ['fastest'], gains(c, [a, b]) == [], gains(d, [a, b, c]) == [],
              gains(e, [a, b, c, d]) == ['memory'], gains(r(6, memory=109), [a]) == [], gains(r(7, hv=0.3536), [a]) == ['hv'],
              gains(r(8, fastest32=0.1665), [a]) == ['fastest32'], not stop([a, b]), not stop([a, b, c]), stop([a, b, c, d]),
              stop([a, r(2), r(3)]), not stop([a, b, c, d, e]), earliest([a, b]) == 4, earliest([a, r(2)]) == 3,
              earliest([a]) == 3, earliest([a, b, c]) == 4]
    k = r(9, hv=0.35, fastest=0.14, gens=160, curve=dict(hv=[[100, 0.33], [150, 0.345]], fastest=[[3, 0.2], [90, 0.145], [150, 0.141]],
          smallest=[[3, 14100]], memory=[[3, 112]], fastest32=[[3, 0.175]]))
    n = r(10, hv=0.336, fastest=0.1445, smallest=14100, memory=112, fastest32=0.175, gens=120)   # 562: a shorter run
    checks += [at(k, 120)['hv'] == 0.33, at(k, 155)['hv'] == 0.345, at(k, 160) is k, at(k, None) is k, at(a, 120) is a,
               at(k, 50)['hv'] == 0.33, at(k, 120)['fastest'] == 0.145, at(k, 2)['fastest'] == 0.2, gains(n, [k]) == ['hv'], gains(dict(n, gens=None), [k]) == [],
               gains(dict(n, gens=160), [k]) == [], gains(r(11, hv=0.3534, gens=200), [k]) == [], gains(r(12, hv=0.3536, gens=200), [k]) == ['hv']]
    ok = all(checks)
    print('stopping.py self-test: %d checks - the thresholds at their edges, the count, the earliest stop - %s'
          % (len(checks), 'pass' if ok else 'FAIL at %s' % [i for i, x in enumerate(checks) if not x]))
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--self-test']: sys.exit(self_test())
    opt = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    if opt('--seed') is None: sys.exit(__doc__)
    seed, led = int(opt('--seed')), opt('--ledger') or LEDGER
    db = next(x for x in a if not x.startswith('--') and x not in (opt('--seed'), opt('--ledger'), opt('--curve')))
    sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E, hv
    method, runs = series(led); R = hv.load(db, E); m = hv.measure(db, E, R=R)
    pick = lambda m: m['alive'] if method.get('extremes') == 'alive' else m      # 556: the series says whose extremes
    x = pick(m)
    run = dict(seed=seed, front=m['front'], hv=round(m['hv'], 6), fastest=round(x['fastest'], 6), smallest=x['smallest'],
               memory=x['memory'], fastest32=round(x['fastest32'], 6))
    if method.get('matched') or opt('--curve'):  # 562: its last generation; its curve for --append, or alone
        run['gens'] = max((r.get('gen') or 0) for r in R.values()); cf = opt('--curve')
        if opt('--curve') and '--append' not in a:
            json.dump(dict(seed=seed, gens=run['gens'], curve=curve(db, E, hv, R, run['gens'])), open(cf, 'w'))
            sys.exit(print('stopping: seed %d\'s curve, generations 0-%d, in %s' % (seed, run['gens'], cf)))
        if '--append' in a:
            k = json.load(open(cf)) if cf and os.path.exists(cf) else {}
            run['curve'] = k['curve'] if k.get('seed') == seed and k.get('gens') == run['gens'] else curve(db, E, hv, R, run['gens'])
    print(report(run, method, runs))
    if '--append' in a:
        if any(x['seed'] == seed for x in runs): print('the ledger has seed %d already - nothing appended' % seed)
        else:
            with open(led, 'a') as f: f.write(json.dumps(run) + '\n')
            print('appended to %s' % os.path.relpath(led))
