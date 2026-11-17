#!/usr/bin/env python3
"""results/drafts/memory-noise-702.py [REPO] - the least memory's noise between sessions (Iteration 702): every design
with a memory reading (rss, KB) in two or more of results/'s markdown files, the spread of its readings. A file often
repeats another's record, so the share that differ is a floor. At 702: 2,769 designs, 416 differ - 334 by 4 KB (one
page), 46 by 8 - and the stopping series' least memory 112/108 KB back and forth since seed 74, 104 at seed 94: the
owner moved the threshold to 8 KB from seed 95 (stopping.py's mem_kb). Run with python3 -I."""
import collections, glob, json, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
seen = collections.defaultdict(dict)
for f in sorted(set(glob.glob(os.path.join(root, 'results', '**', '*.md'), recursive=True))):
    for l in open(f, errors='replace'):
        i = l.find('{"')
        if i < 0 or '"rss"' not in l or '"id"' not in l: continue
        try: r = json.loads(l[i:].strip())
        except ValueError: continue
        if r.get('status', 'ok') == 'ok' and isinstance(r.get('rss'), int) and r.get('id'): seen[r['id']][f] = r['rss']
multi = {i: v for i, v in seen.items() if len(v) >= 2}
d = collections.Counter(max(v.values()) - min(v.values()) for v in multi.values())
print('designs with readings in two or more files: %d; their readings differ in %d - by KB: %s'
      % (len(multi), sum(n for k, n in d.items() if k), ', '.join('%d: %d' % kv for kv in sorted(d.items()) if kv[0])))
led = os.path.join(root, 'results', 'stopping-series.md')
print('the stopping series\' least memory, seed by seed:', '; '.join('%d %d' % (r['seed'], r['memory']) for r in
      (json.loads(l) for l in open(led) if l.startswith('{"seed"'))))
