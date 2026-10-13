#!/usr/bin/env python3
"""progress-table.py - every run's extremes, from its results file (Iteration 253).

For each results/evolve-<machine>-seedN.md with machine-readable front records
(seed 19 on; the earlier files are prose, and counted size differently): the
iteration that recorded it, the front's size, the fastest design (speed against
the hand-made s6 of that commit, and as a speedup), the smallest design (binary
+ image) and the smallest engine binary on the front, and the least peak memory.

The speed is relative to s6 built from the same commit and measured on that
run's selection workloads - so a change that speeds up every design, s6
included, does not show, and the values before and after Iteration 151 (the
selection changed: bubble and ackermann in, parse held out) are not comparable.

    python3 lab/evolve/progress-table.py > results/progress-by-run.md
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = []
for f in glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md')):
    m = re.search(r'evolve-(.+)-seed(\d+)(\w*)\.md$', f)
    machine, seed, suffix = m.group(1), int(m.group(2)), m.group(3)
    text = open(f).read()
    it = re.findall(r'Iteration (\d+)', text.split('\n', 1)[0])
    recs = []
    for l in text.split('\n'):
        if l.startswith('{"bin"'):
            try: r = json.loads(l)
            except ValueError: continue
            if isinstance(r.get('speed'), (int, float)) and r.get('bin') and r.get('size'): recs.append(r)
    if not recs: continue
    fast = min(recs, key=lambda r: r['speed'])
    small = min(recs, key=lambda r: r['bin'] + r['size'])
    mem = min(recs, key=lambda r: r['rss'] if isinstance(r.get('rss'), (int, float)) else 1e9)
    rows.append((seed, suffix, machine, it[0] if it else '?', len(recs), fast, small, min(r['bin'] for r in recs), mem))
rows.sort(key=lambda r: (r[0], r[1]))
print('# Every run\'s extremes (lab/evolve/progress-table.py)\n')
print('Speed against the hand-made s6 of the same commit, on that run\'s selection; the selection changed at Iteration 151 (values either side are not comparable). Size: stripped engine + image, bytes.\n')
print('| seed | iteration | front | fastest | speed | x s6 | smallest | binary + image | smallest engine | least memory KB |')
print('|---|---|---|---|---|---|---|---|---|---|')
for seed, suffix, machine, it, n, fast, small, sbin, mem in rows:
    print('| %d%s | %s | %d | %s | %.3f | %.2f | %s | %s | %s | %s |' % (
        seed, suffix, it, n, fast['id'], fast['speed'], 1 / fast['speed'], small['id'],
        format(small['bin'] + small['size'], ','), format(sbin, ','), mem.get('rss')))
