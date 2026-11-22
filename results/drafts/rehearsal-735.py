#!/usr/bin/env python3
"""results/drafts/rehearsal-735.py [NAME ...] - the new genes rehearsed together before the series' first seed (Iteration
735; results/rehearsal-693.md and 696's method). The genes since the last run: jitdead (710), jitfew (713), hashk (729),
chainorder (732), numfirst (733), on the engine with the fixed data layout (734). Each role (designs/NAME/record.json,
default all ten) evaluated by the lab (evolve.evaluate, 3 rounds, both widths) as recorded - the new genes off - and with
every new gene it can express on, in two interleaved pairs (off, on, off, on); the medians of each side's two. Prints
each role's genes expressed, the statuses, speed on / off at 64 and 32 bits (lower is faster), the size's parts and
memory. JSON of every record to REHEARSAL_OUT if set. Run from the top of a built tree as the build user, python3 -B."""
import json, os, statistics, sys
ROOT = os.getcwd(); sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve'))
names = sys.argv[1:]; sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
NEW = ('jitdead', 'jitfew', 'hashk', 'chainorder', 'numfirst')
DS = os.path.join(ROOT, 'designs'); names = names or sorted(x for x in os.listdir(DS) if os.path.exists(os.path.join(DS, x, 'record.json')))
def med(rs, k):
    v = [r[k] for r in rs if r.get(k) is not None]
    return statistics.median(v) if v else None
print('# The new genes rehearsed together (results/drafts/rehearsal-735.py): evolve.evaluate, 3 rounds, both widths, two interleaved pairs\n')
print('| role | genes on | statuses | speed on / off (64) | (32) | engine | image | the apps\' code | total | memory KB (64) |')
print('|---|---|---|---:|---:|---|---|---|---|---|')
allrec = {}
for n in names:
    g = json.load(open(os.path.join(DS, n, 'record.json')))['genome']
    g0 = E.canon(dict(g)); g1 = E.canon(dict(g, **{k: 1 for k in NEW}))
    on = [k for k in NEW if E.express(g1).get(k)]
    R = {0: [], 1: []}
    for _ in range(2):
        for v, gg in ((0, g0), (1, g1)):
            R[v].append(E.evaluate(gg, 3))
    allrec[n] = R
    st = ' / '.join(','.join(sorted(set(r['status'] for r in R[v]))) for v in (0, 1))
    f = lambda k, v: med(R[v], k)
    def pair(k):
        a, b = f(k, 0), f(k, 1)
        return '%s -> %s' % (format(int(a), ',') if a is not None else '-', format(int(b), ',') if b is not None else '-')
    ratio = lambda k: '%.3f' % (f(k, 1) / f(k, 0)) if f(k, 0) and f(k, 1) else '-'
    print('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (n, ', '.join(on) or 'none', st, ratio('speed'), ratio('speed32'),
          pair('bin'), pair('size'), pair('app'), pair('total'), pair('rss')), flush=True)
if os.environ.get('REHEARSAL_OUT'): json.dump(allrec, open(os.environ['REHEARSAL_OUT'], 'w'))
