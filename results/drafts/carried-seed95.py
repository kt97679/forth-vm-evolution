#!/usr/bin/env python3
"""results/drafts/carried-seed95.py PACK IDS (Iteration 703) - the carried designs re-read in seed 95: 2806f89619 at 32 bits
in generation 0 (0.1733, its kernel 0.363), seed 94's 104 KB designs (108-112 KB here), the least memory alive (108)."""
import json, sys

pack = sys.argv[1]
ids = set(sys.argv[2].split(','))
recs = {}
mem = []
for line in open(pack + '/db.jsonl'):
    try:
        r = json.loads(line)
    except Exception:
        continue
    i = r.get('id')
    if i in ids:
        recs.setdefault(i, []).append(r)
    if r.get('status') == 'ok' and r.get('rss') is not None:
        mem.append((r['rss'], i, r.get('gen'), r.get('total')))

for i in sorted(ids):
    for r in recs.get(i, []):
        t32 = r.get('t32') or {}
        print(i, 'gen', r.get('gen'), r.get('status'), 'speed %.4f' % r['speed'] if r.get('speed') else '-',
              'speed32 %.4f' % r['speed32'] if r.get('speed32') else '-',
              'k32 %.3f' % t32['kernel'] if 'kernel' in t32 else '', 'rss', r.get('rss'), 'total', r.get('total'),
              'how', str(r.get('how', ''))[:60])
mem.sort()
print('least memory:', mem[:8])
print('designs at <=104 KB:', sum(1 for m in mem if m[0] <= 104))
try:
    rm = json.load(open(pack + '/remeasure.json'))
    if isinstance(rm, dict):
        for i in sorted(ids):
            if i in rm:
                print('remeasure', i, str(rm[i])[:300])
        print('remeasure keys sample', list(rm)[:5])
    else:
        print('remeasure type', type(rm), str(rm[0])[:300])
except Exception as e:
    print('remeasure:', e)
