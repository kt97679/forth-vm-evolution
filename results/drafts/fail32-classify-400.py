# Iteration 400 (results/fail32-400.md): every 32-bit failure in a database, by why32, with bfind-without-tos counted
# and the gene values most enriched among the rest. python3 THIS DB, from the repository.
import json, sys, os
from collections import Counter, defaultdict
DB = sys.argv[1]
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
fail = defaultdict(list); ok = []
for l in open(DB):
    try: r = json.loads(l)
    except ValueError: continue
    if 'speed32' not in r and 'why32' not in r: continue
    g = r['genome']; g32 = dict(g, jit=0)
    if (g32.get('scale') or 0) > 2: g32['scale'] = 2
    g32 = E.canon(g32); ex = E.express(g32)
    row = {k: v for k, v in ex.items() if not isinstance(v, (list, dict))}; row['_id'] = r['id']
    row['_bfind_notos'] = bool(ex.get('bfind')) and not ex.get('tos')
    (fail[r['why32']] if r.get('why32') else ok).append(row)
print('measured at 32 bits:', len(ok), '| failures:', {k: len(v) for k, v in fail.items()})
for why, rows in fail.items():
    print('\n==', why, len(rows), '| bfind expressed without tos:', sum(r['_bfind_notos'] for r in rows), 'of', len(rows),
          '| among measured:', sum(r['_bfind_notos'] for r in ok))
    rest = [r for r in rows if not r['_bfind_notos']] if 'corpus' in why else rows
    keys = set().union(*[r.keys() for r in rest + ok]) - {'_id', '_bfind_notos'}
    sc = []
    for k in keys:
        for v in set(str(r.get(k)) for r in rest):
            pf = sum(str(r.get(k)) == v for r in rest) / max(1, len(rest)); po = sum(str(r.get(k)) == v for r in ok) / len(ok)
            sc.append((pf - po, k, v, pf, po))
    sc.sort(reverse=True)
    print('   the rest:', len(rest), '- most enriched gene values (share among them / among measured):')
    for d, k, v, pf, po in sc[:9]: print('     %-12s %-6s %5.1f%% / %5.1f%%' % (k, v, 100 * pf, 100 * po))
    print('   e.g.', [r['_id'] for r in rest[:6]])
