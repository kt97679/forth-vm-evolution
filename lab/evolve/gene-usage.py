#!/usr/bin/env python3
"""gene-usage.py FILE [FILE ...] [--vs FILE [FILE ...]] - the genes a front uses (Iteration 375).

Each FILE is a run's database (db*.jsonl: its front as compare-fronts.py takes it - the re-measure
file beside it, else the selection front) or a seed report (results/evolve-*-seedN.md: its front's
records). Every design is expressed (evolve.py's express(canon(g)) - what is built), and **a gene
absent from an expression counts as off**: express() leaves a gene at its default out, so reading
only the values present calls a rare value universal (Iteration 372: compiler=1 looked universal;
GCC built 541 of the 722 designs).

Prints, for the FILEs' fronts together: the genes on in every design, on in none, and each gene's
share. With --vs, a second group beside the first, the genes ordered by how far their shares
differ - for a run against others (seed 58, from scratch and without the tag2 requirement, against
the carried runs: did it come back to their region?), or before and after a change.
"""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
if not args or args[0] in ('-h', '--help'): sys.exit(__doc__)
A, B = (args[:args.index('--vs')], args[args.index('--vs') + 1:]) if '--vs' in args else (args, [])
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E

def front(path):
    R = {}
    for l in open(path):
        try: r = json.loads(l); R[r['id']] = r
        except (ValueError, KeyError, TypeError): pass
    base = os.path.basename(path)
    if not (base.startswith('db') and base.endswith('.jsonl')):
        return [r for r in R.values() if 'genome' in r]                     # a seed report: its front's records
    rmf = os.path.join(os.path.dirname(path), base.replace('db', 'remeasure', 1).replace('.jsonl', '.json'))
    ids = [i for i in json.load(open(rmf)) if i in R] if os.path.exists(rmf) else \
          E.fronts([i for i, r in R.items() if r.get('status') == 'ok'], R)[0]
    return [R[i] for i in ids]

OFF = (0, False, None, '', [], 'O2')       # opt's default is O2: an -O2 design has opt off
def usage(paths):
    X = [E.express(E.canon(r['genome'])) for p in paths for r in front(p)]
    keys = {k for x in X for k in x}
    on = {k: sum(1 for x in X if k in x and x[k] not in OFF) for k in keys}
    vals = {k: collections.Counter(json.dumps(x.get(k, 'off'), sort_keys=True)[:24] for x in X) for k in keys}
    return len(X), on, vals

n, on, vals = usage(A)
if not B:
    print('%d front designs (%s), an absent gene counted as off\n' % (n, ', '.join(os.path.basename(p) for p in A)))
    print('on in every design: %s' % (', '.join(sorted(k for k in on if on[k] == n)) or '-'))
    print('on in none: %s\n' % (', '.join(sorted(k for k in on if on[k] == 0)) or '-'))
    print('| gene | on | share | values |\n|---|---|---|---|')
    for k in sorted(on, key=lambda k: (-on[k], k)):
        print('| %s | %d | %.0f%% | %s |' % (k, on[k], 100 * on[k] / n, ', '.join('%s %d' % kv for kv in vals[k].most_common(4))))
else:
    m, on2, vals2 = usage(B)
    keys = set(on) | set(on2)
    print('Group 1: %d front designs (%s); group 2: %d (%s) - an absent gene counted as off\n'
          % (n, ', '.join(os.path.basename(p) for p in A), m, ', '.join(os.path.basename(p) for p in B)))
    print('| gene | group 1 on | group 2 on | difference |\n|---|---|---|---|')
    sh = lambda o, k, t: o.get(k, 0) / t if t else 0
    for k in sorted(keys, key=lambda k: (-abs(sh(on, k, n) - sh(on2, k, m)), k)):
        print('| %s | %.0f%% | %.0f%% | %+.0f |' % (k, 100 * sh(on, k, n), 100 * sh(on2, k, m), 100 * (sh(on, k, n) - sh(on2, k, m))))
