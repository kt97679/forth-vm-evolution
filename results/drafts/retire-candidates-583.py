#!/usr/bin/env python3
"""results/drafts/retire-candidates-583.py REPORT.md CANDIDATES.md [--msc DB] - consolidation's retirement checked against
the designs the final pick chooses from (Iteration 583). REPORT.md: retire-report-579.py's output (its RETIRE CANDIDATE
rows - no design on the pooled true front). CANDIDATES.md: final-set.py --candidates or the final set (one record a
line). The final set is chosen from the candidates, not only the front, so a value is retired only when no candidate -
at consolidation, no final-set design - expresses it either (evolve.express: a dormant gene counts for none).
--msc DB: a seed pack's db.jsonl - its alive msc=1 designs without the JIT, each with its nearest alive msc=0 design
(fewest expressed genes apart): the Tegra's check before msc is retired (results/drafts/retire-candidates-573.md, 4).
Seed 86 (583): of the 232 candidates, jitdoes=1 12, fsys=1 12, rtloop=2 1; no other candidate value."""
import collections, json, sys
a = sys.argv[1:]; db = None
if '--msc' in a: i = a.index('--msc'); db = a[i + 1]; del a[i:i + 2]
rep, cand = a
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
V = []
for l in open(rep):
    if 'RETIRE CANDIDATE' in l:
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        V.append((c[0], int(c[1]) if c[1].lstrip('-').isdigit() else c[1]))
C = [json.loads(l) for l in open(cand) if l.startswith('{')]
n = collections.Counter(); who = collections.defaultdict(list)
for r in C:
    e = E.express(E.canon(r['genome']))
    for k, v in V:
        if e.get(k) == v: n[(k, v)] += 1; who[(k, v)].append(r['id'])
print('%d designs in %s; the report\'s %d retire candidates:' % (len(C), cand, len(V)))
for k, v in V: print('  %s=%s: %d%s' % (k, v, n[(k, v)], (' - ' + ' '.join(who[(k, v)][:12])) if n[(k, v)] else ''))
if db:
    R = [json.loads(l) for l in open(db)]
    A = {r['id']: E.express(E.canon(r['genome'])) for r in R if r.get('status') == 'ok' and r.get('genome')}
    S = {r['id']: r for r in R if r.get('status') == 'ok'}
    one = [i for i, e in A.items() if e.get('msc') == 1 and not E.jit_on(E.canon(S[i]['genome']))]
    zero = [i for i, e in A.items() if e.get('msc') == 0 and not E.jit_on(E.canon(S[i]['genome']))]
    dist = lambda x, y: sum(1 for k in set(A[x]) | set(A[y]) if k != 'msc' and A[x].get(k) != A[y].get(k))
    print('\n--msc %s: %d alive msc=1 designs without the JIT; each with its nearest msc=0 one:' % (db, len(one)))
    for i in sorted(one, key=lambda i: S[i]['speed']):
        j = min(zero, key=lambda j: (dist(i, j), S[j]['speed']))
        print('  %s speed %.3f, %d bytes - %s speed %.3f, %d bytes, %d genes apart' % (i, S[i]['speed'], S[i]['total'], j, S[j]['speed'], S[j]['total'], dist(i, j)))
