#!/usr/bin/env python3
"""footprint.py DB [DB ...] [--sample K] [--fastest] [--sizes N,N,...] [--rounds R] [--calls-per-word C]

--fastest (Iteration 436, results/drafts/footprint-gate-435.md): the K fastest designs of the front, not K spread
over it - the held-out check after each run: do the fastest on small programs stay the fastest at 10,000 words?
- does the front's speed hold as a program's code footprint grows? (Iteration 371;
results/generalization.md, section 3)

Selection times small programs: their hot code fits the caches, the predictors see few
dispatch contexts, the dictionary is small. Here the newest run's front (of the DBs given - the
chain passes every run's database; the newest by its file's time) is sampled, K designs spread
from its fastest to its slowest by selection speed, and each is timed on programs of N words
made by footprint-gen.py: the full program, and its definitions alone (--defs-only: the words
and the table of their tokens, no run). The compile phase is the definitions' time; the run
phase, the full program's less it - calls scaled with N (C a word, at least 200,000), as time
per call is the measure.

Every design is built and passed through alive() first, and its checksums must equal hand-made
s6's on every program, or it is reported and not ranked. The rounds go over N and both variants,
s6 timed once in each - at 30,000 words it costs most of a round - first in even rounds, last in
odd, so drift falls on all alike; the median of the rounds, as compare-fronts.py. Each timing is
the child's own CPU time or cycles, pinned, as the evolver's (run_metric's cputime and METRIC).

Prints: s6's own time per word (compile) and per call (run) at each N; each design's ratios to
s6 at each N; and, at each N, the rank correlation (Spearman) between the selection's speed and
the run phase's - whether the selection's order holds as the footprint grows.
"""
import argparse, importlib.util, json, os, re, shutil, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('dbs', nargs='+')
ap.add_argument('--sample', type=int, default=12)
ap.add_argument('--fastest', action='store_true')   # Iteration 436
ap.add_argument('--sizes', default='100,1000,10000,30000')
ap.add_argument('--rounds', type=int, default=5)
ap.add_argument('--calls-per-word', type=int, default=40)
a = ap.parse_args()
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
spec = importlib.util.spec_from_file_location('fpgen', os.path.join(HERE, 'footprint-gen.py'))
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
SIZES = [int(x) for x in a.sizes.split(',') if x.strip()]

def load(db):                      # the front as compare-fronts.py takes it: the re-measure file, else the selection's
    R = {}
    for l in open(db):
        try: r = json.loads(l); R[r['id']] = r
        except (ValueError, KeyError, TypeError): pass
    base = os.path.basename(db)
    rmf = os.path.join(os.path.dirname(db), base.replace('db', 'remeasure', 1).replace('.jsonl', '.json'))
    if base.startswith('db') and base.endswith('.jsonl') and os.path.exists(rmf):   # a database's own, never the file itself
        rm = json.load(open(rmf)); ids = [i for i in rm if i in R]
        return R, {i: rm[i]['speed'] if isinstance(rm[i], dict) else rm[i] for i in ids}, 're-measured front'
    ids = E.fronts([i for i, r in R.items() if r.get('status') == 'ok'], R)[0]
    return R, {i: R[i]['speed'] for i in ids}, 'selection front'

def timed(eng, img, pw, path):
    """One run of a program file: (the metric, its kind, the checksum - the last number printed)."""
    r = E.sh(E.PIN + [E.CPUT, eng, img], cwd=pw, inp=('S" %s" INCLUDED\nBYE\n' % path).encode(), timeout=3600, cpu=1800)
    m = re.search(E.METRIC, r.stderr, re.M); kind = 'cycles' if b'CYCLES' in E.METRIC else 'ns'   # METRIC: CPUNS unless EVOLVE_METRIC=cycles
    if not m: m = re.search(rb'^CPUNS (\d+)', r.stderr, re.M); kind = 'ns'
    nums = [x for x in r.stdout.decode(errors='replace').split() if x.lstrip('-').isdigit()]
    return (int(m.group(1)) if m else None), kind, (nums[-1] if nums else None)

def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); rk = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): rk[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk
def spearman(x, y):
    if len(x) < 3: return None
    rx, ry = ranks(x), ranks(y); mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((p - mx) * (q - my) for p, q in zip(rx, ry))
    den = (sum((p - mx) ** 2 for p in rx) * sum((q - my) ** 2 for q in ry)) ** 0.5
    return num / den if den else None

E.setup()
db = max(a.dbs, key=os.path.getmtime)
R, sp, how = load(db)
order = sorted(sp, key=lambda i: sp[i])
k = max(1, min(a.sample, len(order)))
pick = sorted({order[round(j * (len(order) - 1) / max(1, k - 1))] for j in range(k)}, key=lambda i: sp[i])
if a.fastest: pick = order[:k]                        # Iteration 436: the fastest k, the held-out check's
print('# Footprint: does the front\'s speed hold as the code grows? (lab/evolve/footprint.py)\n')
print('Front: %s, %s (%d designs); sampled %d by selection speed' + (' - the fastest' if a.fastest else '') + ', fastest to slowest. Sizes %s; calls %d a word,'
      ' at least 200,000; %d rounds, medians.\n' % (db, how, len(order), len(pick), ', '.join(map(str, SIZES)), a.calls_per_word, a.rounds))
scratch = os.path.join(E.EV, 'footprint'); shutil.rmtree(scratch, ignore_errors=True); os.makedirs(scratch)
progs = {}
for n in SIZES:
    calls = max(200000, a.calls_per_word * n)
    for var in ('full', 'defs'):
        p = os.path.join(scratch, 'fp-%d-%s.fth' % (n, var))
        open(p, 'w').write(G.program(n, calls, 8, 1, var == 'defs')); progs[(n, var)] = (p, calls)
members = [('s6', E.REF)]; dead = []
for i in pick:
    d = os.path.join(scratch, i)
    try:
        eng, img = E.build(E.canon(R[i]['genome']), d); pw = E.private_work(d); E.alive(eng, img, pw)
        members.append((i, (eng, img, pw)))
    except Exception as e:
        dead.append('%s (%s)' % (i, str(e).strip().splitlines()[-1][:80] if str(e).strip() else type(e).__name__))
    print('built %s' % i, file=sys.stderr, flush=True)
T, CK, KIND = {}, {}, set()
for rnd in range(a.rounds):
    for n in SIZES:
        for var in ('full', 'defs'):
            seq = members if rnd % 2 == 0 else members[::-1]
            for name, (eng, img, pw) in seq:
                t, kind, ck = timed(eng, img, pw, progs[(n, var)][0])
                KIND.add(kind); CK.setdefault((name, n, var), set()).add(ck)
                if t is not None: T.setdefault((name, n, var), []).append(t)
    print('round %d of %d' % (rnd + 1, a.rounds), file=sys.stderr, flush=True)
med = lambda name, n, var: statistics.median(T[(name, n, var)]) if T.get((name, n, var)) else None
bad = sorted({name for (name, n, var), c in CK.items() if name != 's6' and c != CK.get(('s6', n, var))})
unit = '/'.join(sorted(KIND))
print('## s6, hand-made: its own time per word compiled and per call run (%s)\n' % unit)
print('| N | compile, per word | run, per call |\n|---|---|---|')
s6run = {}
for n in SIZES:
    dm, fm = med('s6', n, 'defs'), med('s6', n, 'full'); calls = progs[(n, 'full')][1]
    s6run[n] = (fm - dm) if dm is not None and fm is not None and fm > dm else None
    print('| %s | %s | %s |' % (format(n, ','), '%.0f' % (dm / n) if dm else '-', '%.1f' % (s6run[n] / calls) if s6run[n] else '-'))
print('\n## Each design against s6 - run phase / compile phase, at each N (below 1: faster than s6)\n')
print('| design | selection speed | ' + ' | '.join('N=%s run / compile' % format(n, ',') for n in SIZES) + ' |')
print('|---|---|' + '---|' * len(SIZES))
RR = {}
for name, _ in members[1:]:
    cells = []
    for n in SIZES:
        dm, fm, sd = med(name, n, 'defs'), med(name, n, 'full'), med('s6', n, 'defs')
        run = (fm - dm) if dm is not None and fm is not None and fm > dm else None
        rr = run / s6run[n] if run and s6run[n] else None; cr = dm / sd if dm and sd else None
        if rr is not None and name not in bad: RR[(name, n)] = rr
        cells.append('%s / %s' % ('%.3f' % rr if rr else '-', '%.3f' % cr if cr else '-'))
    print('| %s%s | %.3f | %s |' % (name, ' (checksum differs)' if name in bad else '', sp[name], ' | '.join(cells)))
print('\n## Does the selection\'s order hold? Spearman, selection speed against the run phase\'s ratio\n')
for n in SIZES:
    xs = [(sp[name], RR[(name, n)]) for name, _ in members[1:] if (name, n) in RR]
    rho = spearman([x for x, _ in xs], [y for _, y in xs])
    print('- N = %s: %s over %d designs' % (format(n, ','), '%.3f' % rho if rho is not None else '-', len(xs)))
if dead: print('\nNot measured - did not build or not alive: %s' % ', '.join(dead))
if bad: print('\nChecksums differing from s6\'s - not ranked: %s' % ', '.join(bad))
shutil.rmtree(scratch, ignore_errors=True)
