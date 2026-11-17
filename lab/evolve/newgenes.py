#!/usr/bin/env python3
"""lab/evolve/newgenes.py DB RESULTS.md - step 3's genes in a run (Iteration 699; seed 92's draft,
results/drafts/newgenes-seed92.py, made a tool - each run of the series reports them).

For each gene (rtvar, rtconst, rtinline, and beside them jitvar, jitdoes, varslot, rtimm): its share of the run's
alive children (generation 1 on) and of the true front (the results file's front table), the enrichment, and where
on the front it sits (the fastest, smallest and leanest tenths). Then the pairs: two alive designs whose genomes are
as expressed the same but for that gene - the in-run speed ratio (on / off, below 1 the gene faster), at both widths,
the size difference (bytes, exact), and the per-workload ratios' medians. In-run speeds are the run's own single
measures, so a pair's ratio carries the run's noise; the medians over many pairs do not. Reads only: safe beside a run.
"""
import collections, json, math, os, re, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve'))

DB, RES = sys.argv[1], sys.argv[2]
m = re.search(r'seed(\d+)', os.path.basename(RES)); SEED = m.group(1) if m else '?'
sys.argv = ['x']
import evolve as E
GENES = ['rtvar', 'rtconst', 'rtinline', 'jitvar', 'jitdoes', 'varslot', 'rtimm']
R = {}
for l in open(DB, errors='replace'):
    try: r = json.loads(l)
    except ValueError: continue
    if r.get('status') == 'ok' and 'genome' in r: r['ex'] = E.express(E.canon(r['genome'])); R[r['id']] = r
front = []
for l in open(RES, errors='replace').read().split('## How the front came about')[0].split('\n'):
    f = [x.strip() for x in l.split('|')]
    if len(f) > 10 and re.fullmatch(r'[0-9a-f]{10}', f[1] or '') and f[1] in R: front.append(f[1])
F = [R[i] for i in front]
kids = [r for r in R.values() if r.get('gen', 0) >= 1]
on = lambda r, g: bool(r['ex'].get(g))   # as expressed - seed-facts.py's count
n = max(1, len(F) // 10)
tenths = {'fastest': sorted(F, key=lambda r: r['speed'])[:n], 'smallest': sorted(F, key=lambda r: r['total'])[:n],
          'leanest': sorted(F, key=lambda r: r.get('rss', 9e9))[:n], 'fastest32': sorted(F, key=lambda r: r.get('speed32', 9e9))[:n]}
print('seed %s: %d alive (%d children, generation 1 on), the true front %d (tenths of %d)' % (SEED, len(R), len(kids), len(F), n))
print()
print('| gene | children with it | the front with it | enrichment | fastest tenth | smallest tenth | leanest tenth | fastest tenth at 32 bits |')
print('|---|---|---|---|---|---|---|---|')
for g in GENES:
    a = sum(on(r, g) for r in kids) / max(1, len(kids)); b = sum(on(r, g) for r in F) / max(1, len(F))
    print('| %s | %.1f%% | %d (%.1f%%) | %s | %s |' % (g, 100 * a, sum(on(r, g) for r in F), 100 * b, '%.2f' % (b / a) if a else '-',
          ' | '.join(str(sum(on(r, g) for r in t)) for t in tenths.values())))
print()

def key(r, g):
    return json.dumps({k: v for k, v in r['ex'].items() if k != g}, sort_keys=True)
def ts(r, w=''):
    return r.get('t' + w) or {}
gm = lambda xs: math.exp(statistics.mean(math.log(x) for x in xs)) if xs else float('nan')
print('The pairs - the same expressed genome but for the gene, both alive (on / off; below 1 the gene faster; size on - off, bytes):')
print()
print('| gene | pairs | speed, geometric mean | at 32 bits | of them faster with it | binary + image + app, median | of which app | per workload (median on / off) |')
print('|---|---|---|---|---|---|---|---|')
for g in GENES:
    by = collections.defaultdict(lambda: [[], []])
    for r in R.values(): by[key(r, g)][on(r, g)].append(r)
    P = [(x, y) for k, (offs, ons) in by.items() for x in offs for y in ons if x['id'] != y['id']]
    if not P: print('| %s | 0 | | | | | | |' % g); continue
    sp = [y['speed'] / x['speed'] for x, y in P]
    s32 = [y['speed32'] / x['speed32'] for x, y in P if x.get('speed32') and y.get('speed32')]
    wl = collections.defaultdict(list)
    for x, y in P:
        tx, ty = ts(x), ts(y)
        for w in tx:
            if w in ty and tx[w] > 0: wl[w].append(ty[w] / tx[w])
    print('| %s | %d | %.3f | %s | %d of %d | %+d | %+d | %s |' % (g, len(P), gm(sp), '%.3f' % gm(s32) if s32 else '-',
          sum(v < 1 for v in sp), len(sp), statistics.median(y['total'] - x['total'] for x, y in P),
          statistics.median(y.get('app', 0) - x.get('app', 0) for x, y in P),
          ', '.join('%s %.3f' % (w, statistics.median(v)) for w, v in sorted(wl.items()))))
