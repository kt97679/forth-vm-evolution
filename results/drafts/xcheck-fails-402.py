# Iteration 402 (results/xcheck32-402.md): a remote check's designs that failed to build there, against those measured -
# the gene values every failure shares that few of the measured have. python3 THIS OUT.json (its designs.json beside it).
import json, sys
O = json.load(open(sys.argv[1])); D = json.load(open(sys.argv[1].replace('out.json', 'designs.json')))
st = {x['id']: x for x in O['designs']}; G = {r['id']: r['genome'] for r in D}
bad = [i for i in G if st.get(i, {}).get('speed_here') is None and 'compile' in str(st.get(i, {}).get('why', ''))]
good = [i for i in G if st.get(i, {}).get('speed_here') is not None]
print('failed to build', len(bad), bad, '| measured', len(good))
for k in sorted(set().union(*[G[i].keys() for i in G])):
    if any(isinstance(G[i].get(k), (list, dict)) for i in G): continue
    bv = [str(G[i].get(k)) for i in bad]; gv = [str(G[i].get(k)) for i in good]
    for v in set(bv):
        if bv.count(v) == len(bv) and gv.count(v) <= 0.35 * max(1, len(gv)): print('   all failures %-10s = %-5s | measured with it: %d of %d' % (k, v, gv.count(v), len(gv)))
