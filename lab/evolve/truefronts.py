#!/usr/bin/env python3
"""truefronts.py [DB ...] - every run's true front, recomputed from its records (Iteration 547). GOALS.md: every figure
the article quotes comes from the runs' records, on the true fronts - and until seed 74 the reports showed the staircase
shortcut, about a third of each true front (results/drafts/front-recheck-528.md). A chain's experiment step: next-run.sh
passes this clone's run and the newest archived; this reads every archived run besides ($RUNS, else runs/, and
lab/evolve/runs/: archived-*/build/evolve/db*.jsonl) and measures nothing. Iteration 549: tools/clean-runs.sh keeps
four archived runs, so first every seed pack ($RUNS and its chains' packs/: forth-vm-evolution-seedN-*.tar.gz, never
removed) - its db.jsonl and report.md, the seed from its name, the newest pack of a seed; a database besides counts only
for a seed no pack gave. The true front is evolve.py's first_front,
by dominates() (Iteration 527) - with two widths when most of a run's designs have a 32-bit speed. A run is named by its
seed: the results file whose reported front it made - the share of that front its records hold as its own children
(generation 1 on; a carried design is a founder, generation 0, in the runs after) - else, for this clone's run, the
chain's line. stdout: a table - each run's records, its true front against the reported one, the extremes (fastest in
the run and at 32 bits, smallest, least memory), what its speed is over - then every true front's designs as JSON lines
(id, binary + image, speed, 32-bit speed, peak KB), for the progress table and the charts; stderr: progress."""
import collections, glob, io, json, os, re, sys, tarfile, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]
if any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
def say(*a): print(*a, file=sys.stderr, flush=True)
pats = [os.path.join(os.environ.get('RUNS') or os.path.join(ROOT, 'runs'), 'archived-*'), os.path.join(HERE, 'runs', 'archived-*')]
for a in args:                                      # the archives beside any it was given
    m = re.match(r'(.*/)archived-[^/]+/build/evolve/[^/]+$', a)
    if m: pats.append(m.group(1) + 'archived-*')
paths, seen = [], set()
for p in list(args) + sorted(f for d in set(pats) for f in glob.glob(os.path.join(d, 'build', 'evolve', 'db*.jsonl'))):
    q = os.path.realpath(p)
    if q not in seen and os.path.isfile(q): seen.add(q); paths.append(p)
def name(p):
    if p.endswith('.tar.gz'): return os.path.basename(p)[19:-7]
    m = re.search(r'(archived-[^/]+)', p); f = os.path.basename(p)
    return (m.group(1) if m else 'this run') + ('' if f == 'db.jsonl' else ' ' + f)
paths.sort(key=lambda p: (not name(p).startswith('archived'), name(p)))    # oldest archived first, this clone's run last
reported = {}
for f in glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md')):
    # Iteration 550: the front table's designs - from seed 74 the genomes below it list the re-measured ones off the
    # front too (seed 74: 261 for 238)
    ids = set(re.findall(r'^\| ([0-9a-f]{10}) \|', open(f, errors='replace').read().split('## How the front came about')[0], re.M))
    m = re.search(r'seed(\d+)\.md$', f)             # a variant's file (seed61b.md, say) names no run here
    if ids and m: reported[int(m.group(1))] = ids
line_seed = None
try: line_seed = int(re.search(r'\bseed (\d+)', open(os.path.join(os.environ['NEXT_RUN_CHAIN'], 'line')).read()).group(1))
except (KeyError, OSError, AttributeError, ValueError): pass
KEEP = ('status', 'speed', 'speed32', 'total', 'size', 'bin', 'rss', 'gen', 'speed1', 'speed2')
print('# Every run\'s true front (lab/evolve/truefronts.py, Iteration 547)\n')
print('The true front by dominates() over each run\'s records; "reported" the front its results file shows (the staircase')
print('until seed 74); "seed" the results file whose front the run made - the share of it among the run\'s own children.')
print('Speed: in the run, against the hand-made s6 of its commit, over the workloads named last - it compares only')
print('within one such column. Size: binary + image, bytes.\n')
def tar_lines(p, tail):
    tf = tarfile.open(p, 'r:gz')
    m = next((m for m in tf.getmembers() if m.name.endswith(tail)), None)
    return (io.TextIOWrapper(tf.extractfile(m), errors='replace') if m else None), tf
packs = {}
for d in set(pats):
    base = os.path.dirname(d.rstrip('*').rstrip('/'))
    for f in glob.glob(os.path.join(base, 'forth-vm-evolution-seed*-*.tar.gz')) + glob.glob(os.path.join(base, 'chain-*', 'packs', 'forth-vm-evolution-seed*-*.tar.gz')):
        m = re.search(r'forth-vm-evolution-seed(\d+)-.*-(\d{8}-\d{6})\.tar\.gz$', f)
        if m and (int(m.group(1)) not in packs or m.group(2) > packs[int(m.group(1))][1]): packs[int(m.group(1))] = (f, m.group(2))
print('| run | seed (share) | records | alive | true front | reported | fastest | at 32 bits | smallest | least KB | speed over |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
out = []
done = set()
for p in [packs[k][0] for k in sorted(packs)] + paths:
    t0 = time.time(); R = {}; tf = None
    if p.endswith('.tar.gz'):
        try: src, tf = tar_lines(p, '/db.jsonl')
        except (OSError, tarfile.TarError) as x: say('truefronts: %s - %s' % (p, x)); continue
        if src is None: print('| %s | %s (pack) | - | - | - | - | - | - | - | - | no db.jsonl in the pack |' % (os.path.basename(p)[:44], re.search(r'seed(\d+)', p).group(1))); continue
    else: src = open(p, errors='replace')
    for l in src:
        if not l.startswith('{'): continue
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id'):                             # the last record of a design is its word, as the evolver reads it
            d = {k: r[k] for k in KEEP if k in r}; d['tk'] = tuple(sorted(k for k in (r.get('t') or {}) if k not in ('sieve', 'parse'))); R[r['id']] = d
    if tf: tf.close()
    own = {i for i, r in R.items() if (r.get('gen') or 0) > 0}
    sc = {s: len(ids & own) / len(ids) for s, ids in reported.items()}
    best = max(sc, key=sc.get) if sc else None
    seed = best if best is not None and sc[best] >= 0.3 else (line_seed if name(p).startswith('this run') else None)
    share = '%.0f%%' % (100 * sc[best]) if seed is not None and seed == best else ('the line' if seed is not None else '-')
    if p.endswith('.tar.gz'): seed, share = int(re.search(r'seed(\d+)', p).group(1)), 'pack'
    elif seed in done: say('truefronts: %s - seed %s, read from its pack already' % (name(p), seed)); continue
    done.add(seed)
    ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss')]
    if not ok:
        print('| %s | %s (%s) | %d | 0 | - | - | - | - | - | - | no records with speed and size |' % (name(p), seed if seed is not None else '?', share, len(R))); continue
    E.TWO_WIDTHS[0] = sum(1 for i in ok if R[i].get('speed32')) * 2 > len(ok)
    alive = len(ok)
    if E.TWO_WIDTHS[0]: ok = [i for i in ok if R[i].get('speed32')]
    fr = E.first_front(ok, R)
    f, s, m = min(fr, key=lambda i: R[i]['speed']), min(fr, key=lambda i: E.ov(R[i], 'total')), min(fr, key=lambda i: R[i]['rss'])
    w = [i for i in fr if R[i].get('speed32')]; f32 = min(w, key=lambda i: R[i]['speed32']) if w else None
    sel = collections.Counter(R[i]['tk'] for i in fr).most_common(1)[0][0]
    two = [R[i] for i in fr if R[i].get('speed1') and R[i].get('speed2')]
    gate = ('slower' if all(abs(r['speed'] - max(r['speed1'], r['speed2'])) < 1e-9 * r['speed'] for r in two) else 'mean') if two else ''
    era = ('%d' % len(sel) + (' +apps' if 'apps' in sel else '') if sel else '?') + ((', ' + gate) if gate else '') + (', two widths' if E.TWO_WIDTHS[0] else '')
    print('| %s | %s (%s) | %d | %d | %d | %s | %s %.3f | %s | %s %s | %s | %s |' % (name(p), seed if seed is not None else '?', share, len(R), alive, len(fr),
          len(reported[seed]) if seed in reported else '-', f, R[f]['speed'], '%s %.3f' % (f32, R[f32]['speed32']) if f32 else '-',
          s, '{:,}'.format(E.ov(R[s], 'total')), R[m]['rss'], era))
    out.append(json.dumps({'run': name(p), 'seed': seed, 'front': [[i, E.ov(R[i], 'total'), round(R[i]['speed'], 5),
               round(R[i]['speed32'], 5) if R[i].get('speed32') else None, R[i]['rss']] for i in sorted(fr, key=lambda i: E.ov(R[i], 'total'))]}, separators=(',', ':')))
    say('truefronts: %s - %d records, the true front %d (%.0f s)' % (name(p), len(R), len(fr), time.time() - t0))
print('\nThe true fronts, a JSON line a run - [id, binary + image, speed, 32-bit speed, peak KB], by size:\n\n```')
for o in out: print(o)
print('```')
