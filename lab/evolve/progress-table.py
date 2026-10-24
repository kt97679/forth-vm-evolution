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
    # Iteration 505: what the speed is - the selection's workloads (from the records' times; seed 71 added apps) and the
    # fast gate's join of two readings (from seed 72 the slower, before it their geometric mean)
    import collections
    sel = collections.Counter(tuple(sorted(k for k in (r.get('t') or {}) if k not in ('sieve', 'parse'))) for r in recs).most_common(1)
    sel = sel[0][0] if sel and sel[0][0] else None
    two = [r for r in recs if r.get('speed1') and r.get('speed2')]
    gate = ('slower' if all(abs(r['speed'] - max(r['speed1'], r['speed2'])) < 1e-9 * r['speed'] for r in two) else 'mean') if two else ''
    era = ('%d' % len(sel) + (' +apps' if 'apps' in sel else '') if sel else '?') + ((', ' + gate) if gate else '')
    rows.append((seed, suffix, machine, it[0] if it else '?', len(recs), fast, small, min(r['bin'] for r in recs), mem, era))
rows.sort(key=lambda r: (r[0], r[1]))
print('# Every run\'s extremes (lab/evolve/progress-table.py)\n')
print('Speed against the hand-made s6 of the same commit, on that run\'s selection; the selection changed at Iteration 151 (values either side are not comparable). Size: stripped engine + image, bytes.\n')
print('The last column says what the speed is: the selection\'s workloads (from seed 71, apps the seventh) and how the fast\n'
      'gate joined a design\'s two readings (from seed 72 the slower; before, their geometric mean). **Bold**: a break - the\n'
      'speed columns do not compare across it; size and memory do.\n')
print('| seed | iteration | front | fastest | speed | x s6 | smallest | binary + image | smallest engine | least memory KB | speed over |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
prev = None
for seed, suffix, machine, it, n, fast, small, sbin, mem, era in rows:
    key = era.split(',')[0] + (',' + era.split(',')[1] if ',' in era else '')
    brk = prev is not None and era != '?' and prev != '?' and era != prev
    print('| %s | %s | %d | %s | %.3f | %.2f | %s | %s | %s | %s | %s |' % (
        ('**%d%s**' if brk else '%d%s') % (seed, suffix), it, n, fast['id'], fast['speed'], 1 / fast['speed'], small['id'],
        format(small['bin'] + small['size'], ','), format(sbin, ','), mem.get('rss'), ('**%s**' % era) if brk else era))
    if era != '?': prev = era
