#!/usr/bin/env python3
"""results/drafts/body-size-drift-576.py DB.jsonl - seed 85's new death, "image did not convert (AssertionError: body size
drift at WORD)" (Iteration 576; results/drafts/body-size-drift-576.md): the deaths counted, the gene values every one of
them shares beside their share among the living, and the designs with those values by how they ended."""
import collections, json, sys
R = []
for l in open(sys.argv[1]):
    try: R.append(json.loads(l))
    except ValueError: pass
D = [r for r in R if 'body size drift' in r.get('status', '')]; A = [r for r in R if r.get('status') == 'ok']
print('%d drift deaths, %d alive, %d records' % (len(D), len(A), len(R)))
shared = []
for k in sorted(set().union(*[set(r['genome']) for r in D])):
    for v, n in collections.Counter(json.dumps(r['genome'].get(k)) for r in D).items():
        fa = sum(1 for r in A if json.dumps(r['genome'].get(k)) == v) / len(A)
        if n == len(D) and fa < 0.6: shared.append((k, v)); print('  every one: %s=%s (the living %.2f)' % (k, v, fa))
C = [r for r in R if r.get('genome') and all(json.dumps(r['genome'].get(k)) == v for k, v in shared)]
print('with all of them: %d - %s' % (len(C), collections.Counter('drift' if 'body size drift' in r.get('status', '') else r.get('status', '')[:45] for r in C).most_common(5)))
