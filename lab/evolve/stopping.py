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


def gains(run, earlier):
    """The criteria a run gains on over the earlier runs; None for a series' first run - nothing to beat."""
    if not earlier: return None
    b = bar(earlier)
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
           "criterion by criterion" % method.get('method', '(no method line)'), '',
           '| seed | front | hypervolume | fastest | smallest | least memory | fastest at 32 bits | gains |',
           '|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(S):
        g = gains(r, S[:i])
        out.append('| %s | %s | %s | %s |' % (r['seed'], r.get('front', '-'), ' | '.join(fmt(k, r[k]) for k in KEYS),
                   'the first' if g is None else ', '.join(NAME[k] for k in g) if g else 'nothing'))
    g = gains(run, S[:-1]); out.append('')
    if g is None: out.append('verdict: seed %d opens the series - nothing earlier to gain on' % run['seed'])
    else:
        b = {k: (max if k == 'hv' else min)(r[k] for r in S[:-1]) for k in KEYS}
        ch = lambda k: '%+d KB' % round(run[k] - b[k]) if k == 'memory' else '%+.1f%%' % (100 * (run[k] / b[k] - 1))
        out.append('verdict: seed %d %s - %s' % (run['seed'], 'GAINS, by %s' % ' and '.join(NAME[k] for k in g) if g else
                   'gains nothing', '; '.join('%s %s against %s (%s%s)' % (NAME[k], fmt(k, run[k]), fmt(k, b[k]), ch(k),
                   ', past its threshold' if k in g else '') for k in KEYS)))
    out.append('the count: %d run(s) on the method; %s' % (len(S), 'STOP - three runs or more, the last two gaining nothing '
               '(if no correctness issue is open)' if stop(S) else 'the earliest stop after seed %d, if every run until '
               'then gains nothing' % earliest(S)))
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
    db = next(x for x in a if not x.startswith('--') and x not in (opt('--seed'), opt('--ledger')))
    sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E, hv
    m = hv.measure(db, E)
    run = dict(seed=seed, front=m['front'], hv=round(m['hv'], 6), fastest=round(m['fastest'], 6), smallest=m['smallest'],
               memory=m['memory'], fastest32=round(m['fastest32'], 6))
    method, runs = series(led)
    print(report(run, method, runs))
    if '--append' in a:
        if any(x['seed'] == seed for x in runs): print('the ledger has seed %d already - nothing appended' % seed)
        else:
            with open(led, 'a') as f: f.write(json.dumps(run) + '\n')
            print('appended to %s' % os.path.relpath(led))
