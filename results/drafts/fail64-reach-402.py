# Iteration 402 (results/fail32-400.md, "At 64 bits"): a database's outcomes by status, and the gene values most
# enriched among its reach-limit deaths against the designs that lived. python3 THIS DB.
import json, re, sys
from collections import Counter
st = Counter(); rl, ok = [], []
for l in open(sys.argv[1]):
    try: r = json.loads(l)
    except ValueError: continue
    s = str(r.get('status')); st[re.sub(r'\d+', 'N', s)[:100]] += 1
    if s.startswith('died: reach limit'): rl.append(r['genome'])
    elif s == 'ok': ok.append(r['genome'])
for k, c in st.most_common(): print('%6d  %s' % (c, k))
if rl:
    sc = []
    for k in [k for k in rl[0] if not isinstance(rl[0][k], (list, dict))]:
        for v in set(str(g.get(k)) for g in rl):
            pf = sum(str(g.get(k)) == v for g in rl) / len(rl); po = sum(str(g.get(k)) == v for g in ok) / len(ok)
            sc.append((pf - po, k, v, pf, po))
    for d, k, v, pf, po in sorted(sc, reverse=True)[:8]: print('   %-10s %-6s %5.1f%% / %5.1f%%' % (k, v, 100 * pf, 100 * po))
