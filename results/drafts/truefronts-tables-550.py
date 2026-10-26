#!/usr/bin/env python3
"""results/drafts/truefronts-tables-550.py TRUEFRONTS.md [CHART.json] - truefronts.py's output turned into what seed
75's processing needs (Iteration 550): the progress table on the true fronts (stdout, markdown - a row a seed, the speed
column's breaks in bold as results/progress-by-run.md has them), and the charts' data (CHART.json): the fastest design
of each run against s6, and every run's size-speed staircase - thinned to 15% steps in speed or 2.5 KB in size, at most
twelve series grouped by what the speed is over - ready for the chat's chart tool."""
import json, re, sys
src = open(sys.argv[1]).read()
rows = {}
for l in src.split('\n'):
    f = [x.strip() for x in l.split('|')]
    if len(f) < 12 or not f[2] or f[1] in ('run', '---') or f[1].startswith('-'): continue
    m = re.match(r'(\d+|\?)', f[2])
    if not m: continue
    rows[f[1]] = dict(run=f[1], seed=int(m.group(1)) if m.group(1) != '?' else None, share=f[2], records=f[3], front=f[5],
                      reported=f[6], fastest=f[7], w32=f[8], smallest=f[9], mem=f[10], era=f[11])
fronts = {}
for l in src.split('\n'):
    if l.startswith('{"run"'):
        o = json.loads(l); fronts[o['run']] = o
runs = sorted(rows.values(), key=lambda r: (r['seed'] is None, r['seed'] or 0, r['run']))
import glob, os                      # "reported" from the results files' front tables: truefronts.py counts their genomes,
for r in runs:                       # which from seed 74 list the re-measured designs off the front too (261 for 238)
    for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'evolve-*-seed%s.md' % r['seed'])):
        r['reported'] = str(len(set(re.findall(r'^\| ([0-9a-f]{10}) \|', open(f).read().split('## How the front came about')[0], re.M))))
print('# Every run\'s extremes on its true front (results/drafts/truefronts-tables-550.py, from truefronts.py)\n')
print('Speed: in the run, against the hand-made s6 of its commit, over what the last column names - it compares only within')
print('one such column; **bold**, a break. Size: binary + image, bytes. "reported": the front its results file showed\n(the staircase until seed 74).\n')
print('| seed | true front | reported | fastest | x s6 | at 32 bits | smallest | least memory KB | speed over |')
print('|---|---|---|---|---|---|---|---|---|')
prev = None
for r in runs:
    sp = re.search(r'([0-9.]+)$', r['fastest']); x = '%.2f' % (1 / float(sp.group(1))) if sp and float(sp.group(1)) else '-'
    b = r['era'] != prev and prev is not None; prev = r['era']
    s = r['seed'] if r['seed'] is not None else r['run']
    print('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % ('**%s**' % s if b else s, r['front'], r['reported'], r['fastest'], x, r['w32'], r['smallest'], r['mem'], '**%s**' % r['era'] if b else r['era']))
if len(sys.argv) > 2:
    eras = []
    for r in runs:
        if r['run'] in fronts and r['seed'] is not None:
            if not eras or eras[-1][0] != r['era']: eras.append((r['era'], []))
            eras[-1][1].append(r)
    per = max(1, -(-sum(len(e[1]) for e in eras) // max(1, 12 - len(eras) + 1)))
    series, fast = [], []
    for era, rs in eras:
        fast.append({'name': era, 'points': [{'x': r['seed'], 'y': round(1 / min(p[2] for p in fronts[r['run']]['front']), 2)} for r in rs]})
        for k in range(0, len(rs), per):
            pts = []
            for r in rs[k:k + per]:
                st, best = [], 9e9
                for i, t, s, s32, m in sorted(fronts[r['run']]['front'], key=lambda p: (p[1], p[2])):
                    if s < best: st.append((t, round(1 / s, 2))); best = s
                keep = st[:1]
                for t, y in st[1:-1]:
                    if y >= keep[-1][1] * 1.15 or t >= keep[-1][0] + 2500: keep.append((t, y))
                if st and st[-1] != keep[-1]: keep.append(st[-1])
                pts += [{'x': t, 'y': y} for t, y in keep]
            g = rs[k:k + per]
            series.append({'name': 'seeds %d-%d, %s' % (g[0]['seed'], g[-1]['seed'], era) if len(g) > 1 else 'seed %d, %s' % (g[0]['seed'], era), 'points': pts})
    json.dump({'fastest_by_seed': fast, 'size_speed': series[:12]}, open(sys.argv[2], 'w'), separators=(',', ':'))
    print('\n%s: %d eras, %d staircase series, %d points' % (sys.argv[2], len(eras), len(series[:12]), sum(len(s['points']) for s in series[:12])), file=sys.stderr)
