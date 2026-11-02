#!/usr/bin/env python3
"""results/drafts/build-hash-cmp-588.py MASTER.jsonl PATCHED.jsonl - build-hash-584.py's two runs compared (Iteration 588): every design
but s2-s5 the same engine and image bytes (or the same death) - PASS - and s2-s5 named, not compared."""
import json, sys
FR = {'s2-cpt16', 's3-cpt16f', 's4-cv8', 's5-cv8spec'}; key = lambda r: (r.get('engine'), r.get('image'), r.get('died'))
a = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1])}; b = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2])}
same = [i for i in a if i not in FR and i in b and key(a[i]) == key(b[i])]; diff = [i for i in a if i not in FR and i in b and key(a[i]) != key(b[i])]
miss = [i for i in a if i not in FR and i not in b]; fr = ['%s %s' % (i, 'same' if i in b and key(a[i]) == key(b[i]) else 'changed' if i in b else 'gone') for i in sorted(FR & set(a))]
print('cmp%s: %s - %d of %d the same, %d different %s, %d missing %s; s2-s5 (not compared): %s' % (b[next(iter(b))]['cell'] if b else '?', 'PASS' if not diff and not miss and same else 'FAIL', len(same), len(a) - len(FR & set(a)), len(diff), diff[:5], len(miss), miss[:5], ', '.join(fr)))
