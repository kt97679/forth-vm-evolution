#!/usr/bin/env python3
"""lab/evolve/carry-check.py [DB...] [--all] [--sample N] - the confirmation run's founders pre-flighted, before its run
(Iteration 562; results/drafts/confirmation-pool-559.md, steps 2-4). The pool evolve.py --carry makes of the databases
(carry_pool: each one's strict front, and the designs carry-named.txt names): its size database by database, where each
named design was found, and the hours its generation 0 costs (about a second a design). Then a sample built with this
tree and run on the corpus against s6 - each database's four extremes, every named design, the rest spread by speed, N
in all (default 40) - so a genome the code has moved under (the JIT's hole fix, the lifted freezes) is caught before the
run, not in it. --all: every archived database beside the first archived one given (an experiment step gets only the
newest four), and the run's own. Markdown on stdout; exit 1 on a design that differs or dies. As the build user, in a
built tree; an experiment step: `then experiment carry-check.py --all`.
"""
import collections, glob, os, shutil, sys
a = sys.argv[1:]
N = int(a[a.index('--sample') + 1]) if '--sample' in a else 40
dbs = [x for x in a if x.endswith('.jsonl')]
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
if '--all' in a:
    arch = [x for x in dbs if '/archived-' in x]
    if arch: dbs = sorted(set(dbs) | set(glob.glob(arch[0].split('/archived-')[0] + '/archived-*/build/evolve/db*.jsonl')))
if not dbs: sys.exit(__doc__)
named = dict(l.split(None, 1) for l in open(E.NAMED) if l.strip() and not l.startswith('#')) if os.path.exists(E.NAMED) else {}
pool = E.carry_pool(dbs, named=named)
lab = lambda how: how.split(' from ', 1)[1].rsplit(': ', 1)[0]
by = collections.defaultdict(list)
for x in pool: by[lab(x[1])].append(x)
print('# The confirmation run\'s founders, pre-flighted (carry-check.py)\n')
print('%d designs from %d databases - generation 0 about %.1f hours of the run at a second a design.\n' % (len(pool), len(dbs), len(pool) / 3600.0))
print('| database | new designs in the pool |\n|---|---|')
for k in sorted(by): print('| %s | %d |' % (k, len(by[k])))
ids = {x[2]['id']: x for x in pool}
print('\n**The named designs**: ' + '; '.join('%s %s' % (i, 'named, carried' if i in ids and ids[i][1].startswith('named') else
      'on a front' if i in ids else 'in no database given, or already carried as another') for i in sorted(named)) + '.\n')
pick, seen = [], set()
def add(x):
    if x[2]['id'] not in seen: seen.add(x[2]['id']); pick.append(x)
for k in sorted(by):                   # each database's four extremes
    for f in ('speed', 'total', 'rss', 'speed32'):
        c = [x for x in by[k] if x[2].get(f)]
        if c: add(min(c, key=lambda x: E.ov(x[2], f)))
for x in pool:
    if x[1].startswith('named'): add(x)
rest = sorted((x for x in pool if x[2]['id'] not in seen), key=lambda x: x[2]['speed'])
k = max(1, len(rest) // max(1, N - len(pick)))
for x in rest[::k]:
    if len(pick) >= N: break
    add(x)
E.setup(); E.run_metric(*E.REF, 'corpus'); ref = E.OUT_LAST[0]; bad = 0
print('The sample - %d designs, each built here and run on the corpus:\n\n| design | from | its speed there | here |\n|---|---|---|---|' % len(pick))
for g, how, r in pick:
    d = os.path.join(E.EV, 'carry-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(g, d); E.run_metric(eng, img, E.private_work(d), 'corpus')
        here = 'right - as s6' if E.OUT_LAST[0] == ref else 'DIFFERS from s6'
    except Exception as x:
        here = 'DIES here: %s' % str(x)[:80]
    shutil.rmtree(d, ignore_errors=True); bad += not here.startswith('right')
    print('| %s | %s | %.4f | %s |' % (r['id'], how.split(': ')[0], r['speed'], here), flush=True)
print('\ncarry-check: %d of %d sampled compute right here; %d open' % (len(pick) - bad, len(pick), bad))
sys.exit(1 if bad else 0)
