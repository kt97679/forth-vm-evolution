#!/usr/bin/env python3
"""hotwords.py ID [ID ...] [--db FILE ...] [--write FILE] - every word's share
of the selection workloads' dispatches, for the gene factor (Iteration 267).

Builds each design with the call map and the profiler, as hotsites.py does -
with the JIT off, so that a word the JIT would translate still shows what it
costs in the interpreter - runs the selection workloads, and charges every
dispatched instruction to the word whose body holds it: a word's SELF cost,
as tools/attribute.py counts it. Code compiled at run time (the benchmarks'
own words) is in no body and counts only in the total. A word's weight is its
mean share over the workloads; over the designs, the largest - a word hot in
any of them is hot. Every word of every design is listed, those never run at
0, so a word missing from the file is one no reference design has.

--write keeps the table (lab/evolve/hotwords-v1.json): the converter
(layout.py --factor --factor-hot FILE) leaves the code of every word missing
from it, or at FACTOR_HOT of the dispatches or more, as it is.
"""
import bisect, collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; dbs, out = [], None
while '--db' in args: i = args.index('--db'); dbs.append(args[i + 1]); del args[i:i + 2]
if '--write' in args: i = args.index('--write'); out = args[i + 1]; del args[i:i + 2]
if not args: sys.exit(__doc__)
recs = {}
for db in dbs or sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
missing = [x for x in args if x not in recs]
if missing: sys.exit('hotwords: no recorded design %s' % ' '.join(missing))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
table = {}
for ident in args:
    g = E.canon(recs[ident]['genome']); d = os.path.join(E.EV, 'hotwords'); shutil.rmtree(d, ignore_errors=True)
    g2 = dict(g, tail=0, msc=0, jit=0)            # the interpreter's view, as hotsites.py profiles
    cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(g2, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    W = sorted((int(f[1]), int(f[2]), ' '.join(f[4:])) for f in (l.rstrip('\n').split(' ') for l in open(cm)) if f[0] == 'W' and f[3] == 'code')
    at = [w[0] for w in W]
    share = collections.Counter({w[2]: 0.0 for w in W})
    pw = E.private_work(d)
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        ipc, tot = collections.Counter(), 0
        for f in (l.split() for l in open(pf)):
            if f[0] == 'I': ipc[int(f[1])] += int(f[2]); tot += int(f[2])
        assert tot, 'hotwords: %s ran nothing on %s' % (ident, wl)
        for a, n in ipc.items():
            i = bisect.bisect_right(at, a) - 1
            if i >= 0 and W[i][0] <= a < W[i][1]: share[W[i][2]] += n / tot / len(E.WORK_SEL)
    for name, v in share.items(): table[name] = max(table.get(name, 0.0), v)
    top = share.most_common(8)
    print('%s: %d code words, %d run; the hottest %s' % (ident, len(W), sum(1 for v in share.values() if v > 0),
          ', '.join('%s %.1f%%' % (n, 100 * v) for n, v in top)))
    shutil.rmtree(d, ignore_errors=True); os.path.exists(cm) and os.remove(cm)
cold = sorted(table.values())
for t in (1e-5, 1e-4, 1e-3):
    print('below %g of the dispatches: %d of %d words' % (t, sum(1 for v in cold if v < t), len(cold)))
if out:
    json.dump({n: round(v, 8) for n, v in sorted(table.items())}, open(out, 'w'), indent=0, sort_keys=True)
    print('wrote %s: %d words from %s' % (out, len(table), ' '.join(args)))
