#!/usr/bin/env python3
"""compare-fronts.py DB [DB ...] [--rounds N] [--cpus A,B] - the fronts of
several runs, measured again in ONE session (Iteration 20).

Runs measured on different days carry their own calibrations: hand-made s6
against itself came out 0.986 inside seed 3 and 1.038 inside seed 4, so a
few per cent between their fronts says nothing. Here every design on every
run's front is built again - with today's converter and engine, so an older
run's design gets today's fixes (Iteration 13's restored words) - checked
through the gate, and measured in one session: the rounds go round-robin
over all the designs, every timed run paired with hand-made s6 as the
evolver pairs them, so drift falls on every design alike.

Hand-made s6 is measured as one of the designs: its ratio is the session's
calibration. Outside 0.98-1.02 the table says so, and ranks nothing that
close.

A run's front: the designs of its re-measure file (beside the database, `db`
-> `remeasure`, `.jsonl` -> `.json`: db.jsonl -> remeasure.json,
db-seed1.jsonl -> remeasure-seed1.json), else its selection front. Sizes are
today's images, the recorded size beside. Nothing is written but stdout and
the evolver's scratch directories.

The median of the rounds, not the best (Iteration 25: the best of N reported
rare lucky runs, a different draw every session). --cpus A,B times every
design on each of those CPUs in the same session, interleaved, and says
whether the rankings agree - the test that two sessions would agree.
"""
import json, math, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; rounds = 10; cpuarg = None
if '--rounds' in args: i = args.index('--rounds'); rounds = int(args[i + 1]); del args[i:i + 2]
if '--cpus' in args: i = args.index('--cpus'); cpuarg = args[i + 1]; del args[i:i + 2]
WIDTHS = '--widths' in args                # Iteration 352: and each design's interpreter at 4-byte cells
if WIDTHS:
    i = args.index('--widths')
    if args[i + 1] != '8,4': sys.exit('--widths: 8,4 only')
    del args[i:i + 2]
# Iteration 114: --frontier - of each run, its front thinned to one design per
# box of 1% speed, 64 bytes and the 8 KB memory tie, plus its three bests:
# what the stopping rule needs exactly, and the front of all runs at the
# resolution the comparison can tell apart anyway. A run's front had
# grown to ~150-180 designs under honest sizes, ~60% on it by memory alone -
# mostly a page or two - and the session to 660 designs, 2 hours at 6 rounds.
FRONTIER = '--frontier' in args
if FRONTIER: args.remove('--frontier')
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
dbs = [os.path.abspath(a) for a in args]
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.TWO_WIDTHS[0] = WIDTHS; E.setup_widths()   # Iteration 352: setup() itself without --widths
home = os.path.expanduser('~')
def say(*a): print(*a, file=sys.stderr, flush=True)

runs, rec = [], {}                  # [(label, [ids])]; id -> (genome, recorded size, recorded speed)
# Iteration 62: the databases here, labelled as a carry names its origin
# (evolve.py --carry: "carried from archived-.../db.jsonl: id")
HERE_DBS = set('/'.join(d.split('/')[-4:-3] + d.split('/')[-1:]) for d in dbs)
def carried_from(r):
    h = r.get('how', '')
    return h[len('carried from '):].split(':')[0] if h.startswith('carried from ') else None
for db in dbs:
    R = {}
    for l in open(db):
        try: r = json.loads(l); R[r['id']] = r
        except ValueError: pass
    base = os.path.basename(db)
    rmf = os.path.join(os.path.dirname(db), base.replace('db', 'remeasure', 1).replace('.jsonl', '.json'))
    if os.path.exists(rmf):
        rm = json.load(open(rmf)); ids = [i for i in rm if i in R]; how = 're-measured front'
        sp = {i: rm[i]['speed'] if isinstance(rm[i], dict) else rm[i] for i in ids}
    else:
        ids = E.fronts([i for i, r in R.items() if r['status'] == 'ok'], R)[0]; how = 'selection front'
        sp = {i: R[i]['speed'] for i in ids}
    # a label that names the run's place, not a path whose tail two runs share
    # (Iteration 21: ".../build/evolve/db.jsonl" was this clone's AND seed 3's archive)
    label = ('this clone: ' + base) if '/archived-' not in db else db[db.index('archived-'):].replace('/build/evolve/', ': ')
    # Iteration 46: a design a run CARRIED from an earlier one counts for the run
    # that found it - whose database is here too - not twice, and not as new.
    # Iteration 62: only if that run IS here - next-run.sh compares the newest
    # few (COMPARE_LAST) - or it would not be measured at all: it stays here.
    nc = len(ids); ids = [i for i in ids if carried_from(R[i]) not in HERE_DBS]
    if len(ids) < nc: how += ', %d carried in and left to their own runs' % (nc - len(ids))
    if FRONTIER and ids:
        # one design per box - 1% of speed, 64 bytes, the 8 KB memory tie -
        # then the boxes' front; and always the run's fastest, smallest and
        # least memory, so the stopping rule's bests are exactly measured
        box = {}
        for i in ids:
            k = (int(math.log(sp[i]) / math.log(1.01) // 1), R[i]['total'] // 64, int(R[i].get('rss', 0) // 8))
            if k not in box or (sp[i], R[i]['total']) < (sp[box[k]], R[box[k]]['total']): box[k] = i
        ks = list(box)
        keep = {box[k] for k in ks if not any(o != k and o[0] <= k[0] and o[1] <= k[1] and o[2] <= k[2] for o in ks)}
        keep |= {min(ids, key=lambda i: sp[i]), min(ids, key=lambda i: R[i]['total']),
                 min(ids, key=lambda i: (R[i].get('rss', 0), sp[i]))}
        s32 = [i for i in ids if R[i].get('speed32')]            # Iteration 387 (review 386, 4d): and the 32-bit
        if s32: keep.add(min(s32, key=lambda i: R[i]['speed32']))   # fastest - the verdict at both widths reads it
        n0 = len(ids); ids = [i for i in ids if i in keep]
        how += ', %d of %d: one per box of 1%% speed, 64 bytes, 8 KB, and the bests' % (len(ids), n0)
    kept = sum(1 for i in ids if carried_from(R[i]))
    if kept: how += ', %d carried from a run not compared here, kept' % kept
    runs.append((label, ids)); say('%s: %d designs (%s)' % (label, len(ids), how))
    for i in ids: rec.setdefault(i, (E.canon(R[i]['genome']), R[i]['size'], sp[i]))
CAL = 's6-cv8b'
rec[CAL] = (E.canon(E.HUMAN['s6-cv8b']), None, 1.0)

live, size, dead, etext, rss, binsz, tot, memv = [], {}, {}, {}, {}, {}, {}, {}
for k, (i, (g, _, _)) in enumerate(sorted(rec.items())):
    d = os.path.join(E.EV, 'cmp', '%03d' % k)
    try:
        eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw)
        live.append((i, eng, img, pw)); size[i] = os.path.getsize(img)
        etext[i] = E.text_size(eng)                   # Iteration 73: the engine's machine code
        binsz[i] = E.bin_size(eng); tot[i] = binsz[i] + size[i]    # Iteration 75: binary + image
    except Exception as e:
        dead[i] = str(e)[:100]
    say('built %d of %d: %s %s' % (k + 1, len(rec), i, dead.get(i, 'ok')))
import statistics
have = [c for c in range(os.cpu_count() or 1) if os.path.exists('/sys/devices/system/cpu/cpu%d' % c)]
cpus = [c for c in map(int, cpuarg.split(','))] if cpuarg else []
cpus = [c for c in cpus if c in have] or [None]              # None: the CPU setup() pinned
pin0 = list(E.PIN)
times = {}                                                  # not `runs`: that is the list of runs above
for r_ in range(rounds):
    say('round %d of %d' % (r_ + 1, rounds))
    for ci, c in enumerate(cpus):
        E.PIN[:] = pin0 if c is None else ['taskset', '-c', str(c)]
        n = len(live); order = live[r_ % n:] + live[:r_ % n]
        for j, (i, eng, img, pw) in enumerate(order):
            for w in E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR):
                pair = [((eng, img, pw), 'd'), (E.REF, 'r')]
                for (e, im, p), side in (pair if (r_ + j + ci) % 2 == 0 else pair[::-1]):
                    times.setdefault((i, w, side, c), []).append(E.run_metric(e, im, p, w))
                    if side == 'd': memv.setdefault((i, w), []).append(E.RSS_LAST[0])   # Iteration 75: memory touched, KB
E.PIN[:] = pin0
med = statistics.median
T = {c: {i: {w: med(times[(i, w, 'd', c)]) / med(times[(i, w, 'r', c)]) for w in E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR)} for i, *_ in live} for c in cpus}
S = {c: {i: math.exp(sum(math.log(T[c][i][w]) for w in E.WORK_SEL) / len(E.WORK_SEL)) for i in T[c]} for c in cpus}
# Iteration 389 (the owner): the session's speed from every CPU measured - a design's per-CPU speeds, and each
# workload's ratio, combined by their geometric mean; until now the first CPU's alone, the second's half of the
# session feeding only the comparison of the two below (results/verdict-audit-388.md). One CPU: as before.
c0 = cpus[0]; _gm = lambda xs: math.exp(sum(math.log(x) for x in xs) / len(xs))
t = {i: {w: _gm([T[c][i][w] for c in cpus]) for w in T[c0][i]} for i in T[c0]}
speed = {i: _gm([S[c][i] for c in cpus]) for i in S[c0]}

cal = speed.get(CAL)
print('# Fronts measured again in one session\n')
print('%d rounds, the median of them; every design paired with hand-made s6 on the same CPU (%s); designs built with this commit.%s\n'
      % (rounds, ', '.join('the pinned one' if c is None else 'cpu %d' % c for c in cpus),
         " A design's speed is the geometric mean of its speeds on these CPUs, and the verdict reads it (Iteration 389)." if len(cpus) > 1 else ''))
if cal is None: print('**No calibration: hand-made s6 did not build or pass the gate.**\n')
else:
    print('**Calibration: hand-made s6 against itself %.3f** (%s).%s\n' % (cal, ', '.join('%s %.3f' % (w, t[CAL][w]) for w in E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR)),
          '' if 0.98 <= cal <= 1.02 else ' OUTSIDE 0.98-1.02: this session cannot rank designs a few per cent apart.'))
for (i, w), v in memv.items():                  # each workload's median, the most of them: the design's peak
    rss[i] = max(rss.get(i, 0), statistics.median(v))
def dominates(sj, si, j, i):
    # Iteration 75 (the owner): three objectives, equal - speed, binary + image, peak memory;
    # Iteration 77: memory within E.MEM_TOL KB a tie (evolve.py says why)
    mj, mi = rss.get(j, 0), rss.get(i, 0)
    return (sj <= si and tot[j] <= tot[i] and mj <= mi + E.MEM_TOL
            and (sj < si or tot[j] < tot[i] or mj < mi - E.MEM_TOL))
def front(ids):
    ids = [i for i in ids if i in speed]
    return [i for i in ids if not any(dominates(speed[j], speed[i], j, i) for j in ids)]
allf = front([i for i in speed if i != CAL])
print('| run | design | speed now | recorded | size now | recorded | binary | binary + image | memory KB | %s | on the front of all |'
      % ' | '.join(E.WORK_SEL + ['%s (held out)' % w for w in (E.WORK_HELD + E.WORK_FAR)]))   # from the lists: Iteration 42
print('|---|---|---|---|---|---|---|---|---|' + '---|' * len(E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR)) + '---|')
for label, ids in runs:
    for i in sorted(ids, key=lambda i: (size.get(i, 1 << 30), speed.get(i, 9))):
        g, rs, rp = rec[i]
        if i in dead: print('| %s | %s | %s | %.3f | | %s | | | |%s |' % (label, i, dead[i], rp, format(rs, ','), ' |' * len(E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR))))
        else: print('| %s | %s | %.3f | %.3f | %s | %s | %s | %s | %s | %s | %s |' % (label, i, speed[i], rp, format(size[i], ','), format(rs, ','),
                    format(binsz[i], ','), format(tot[i], ','), format(rss[i], ',') if rss.get(i) else '-',
                    ' | '.join('%.3f' % t[i][w] for w in E.WORK_SEL + (E.WORK_HELD + E.WORK_FAR)), 'yes' if i in allf else ''))
print('\nThe front of all runs together (speed, binary + image, peak memory), by binary + image: ' + ', '.join('%s %.3f at %s, %s KB' % (i, speed[i], format(tot[i], ','), format(rss.get(i, 0), ','))
      for i in sorted(allf, key=lambda i: -tot[i])))
# Iteration 75 (the owner: tell when three equal objectives do not work):
# the designs on the front only by memory - dominated on speed and binary +
# image together, kept by a page or a few fewer touched.
two = [i for i in allf if any(speed[j] <= speed[i] and tot[j] <= tot[i] and (speed[j], tot[j]) != (speed[i], tot[i]) for j in allf + [k for k in speed if k != CAL])]
print('\nMemory within %g KB counts as a tie (EVOLVE_MEM_TOL).' % E.MEM_TOL)
print('On the front by memory alone: %d of %d%s' % (len(two), len(allf), (' - ' + ', '.join('%s %.3f at %s, %s KB' % (i, speed[i], format(tot[i], ','), format(rss.get(i, 0), ',')) for i in sorted(two, key=lambda i: -tot[i]))) if two else ''))
# Iteration 188 (the owner: a small size increase for a big speed gain is
# a gain - do not lock such out). The rule judged a run by the front's
# extremes alone: a run that moved its middle (+1% size, -25% time) counted
# as small. Two front-wide measures beside them: the hypervolume (the share
# of objective space the front dominates, in log space - a 1% change counts
# the same on every axis; it grows when any part of the front improves) and
# the best Q (binary + image x run time x memory, the owner's - the knee). A
# run is small only if all five are: fastest under 5%, smallest under 2%,
# memory under 8 KB, hypervolume under 2%, best Q under 2%.
def _hv(pts, lo, ref, n=100000):
    import random as _r
    P = [p for p in pts if not any(all(q[k] <= p[k] for k in range(3)) and q != p for q in pts)]
    try:
        import numpy as np
        rng = np.random.default_rng(1); S = np.asarray(lo) + rng.random((n, 3)) * (np.asarray(ref) - np.asarray(lo))
        hit = np.zeros(n, bool)
        for p in P: hit |= (S >= np.asarray(p)).all(axis=1)
        return hit.mean()
    except ImportError:
        rnd = _r.Random(1); n = 20000; hit = 0
        for _ in range(n):
            x = [lo[k] + rnd.random() * (ref[k] - lo[k]) for k in range(3)]
            hit += any(all(p[k] <= x[k] for k in range(3)) for p in P)
        return hit / n
_ok = [i for i in speed if i != CAL and rss.get(i)]
_lp = {i: (math.log(speed[i]), math.log(tot[i]), math.log(rss[i])) for i in _ok}
_q = lambda i: speed[i] * tot[i] * rss[i]
VERDICT64 = {}
if len(_lp) > 1 and len(runs) > 1:
    _lo = tuple(min(v[k] for v in _lp.values()) for k in range(3)); _ref = tuple(max(v[k] for v in _lp.values()) + 0.05 for k in range(3))
    print('\n## Judging the runs (Iteration 188)\n')
    print('Each run against all the others: its extremes, and two front-wide measures - the hypervolume in log space and the best Q '
          '(binary + image x run time x memory). A run is small only if all five are: fastest under 5%, smallest under 2%, '
          'memory under 8 KB, hypervolume under 2%, best Q under 2%. A positive figure is the run AHEAD of all the others '
          '(Iteration 387: read backwards at 384).\n')
    print('| run | fastest | smallest | memory | hypervolume | best Q | verdict |')
    print('|---|---|---|---|---|---|---|')
    for label, ids in runs:
        mine = [i for i in ids if i in _lp]; rest = [i for l2, ids2 in runs if l2 != label for i in ids2 if i in _lp]
        if not mine or not rest: continue
        fg = min(speed[i] for i in rest) / min(speed[i] for i in mine) - 1
        sg = min(tot[i] for i in rest) / min(tot[i] for i in mine) - 1
        mg = min(rss[i] for i in rest) - min(rss[i] for i in mine)
        h0 = _hv([_lp[i] for i in rest], _lo, _ref); h1 = _hv([_lp[i] for i in rest + mine], _lo, _ref)
        hg = h1 / h0 - 1 if h0 else float('nan')
        qg = min(map(_q, rest)) / min(map(_q, mine)) - 1
        small = fg < .05 and sg < .02 and mg < 8 and hg < .02 and qg < .02
        VERDICT64[label] = small                    # Iteration 375: the 32-bit section's verdict builds on it
        print('| %s | %+.1f%% | %+.2f%% | %+d KB | %+.1f%% | %+.1f%% | %s |' % (label, 100 * fg, 100 * sg, mg, 100 * hg, 100 * qg, ('small' if small else 'not small') if label.startswith('this clone') else '(an earlier run: what it still holds)'))
    _qb = min(_ok, key=_q)
    _rel = ' - Q %.3f of s6\'s' % (_q(_qb) / (speed[CAL] * tot[CAL] * rss[CAL])) if CAL in speed and rss.get(CAL) and CAL in tot else ''
    print('\nThe Q-best design of all runs (the knee): %s, speed %.3f at %s bytes, %s KB%s - %s.'
          % (_qb, speed[_qb], format(tot[_qb], ','), format(rss[_qb], ','), _rel, next(l for l, ids in runs if _qb in ids)))
if WIDTHS:                                    # Iteration 352: the speed32 objective's own measure, across the runs
    r32 = max(1, rounds // 2); sp32 = {}
    for k, i in enumerate(sorted(speed)):
        sp32[i] = E.eval32(rec[i][0], r32).get('speed32'); say('32 bits: %d of %d %s %s' % (k + 1, len(speed), i, sp32[i]))
    print('\n## At 32 bits (Iteration 352)\n')
    print("Each design's interpreter as a 32-bit x86 engine at 4-byte cells (its JIT off, its call scale at most 2), "
          "%d round(s), against hand-made s6 at 32 bits%s; a run's fastest there against all the others' (a positive figure: the run ahead). "
          "A run is small at both widths only if its five 64-bit measures are small and its fastest at 32 bits "
          "is under 5%% too (Iteration 375: a new objective's gain counts, as Iteration 188's rule meant).\n"
          % (r32, (' (itself %.3f)' % sp32[CAL]) if sp32.get(CAL) else ''))
    print('| run | fastest at 32 bits | against the others | its 64-bit fastest, at 32 bits | no 32-bit build | verdict at both widths |')
    print('|---|---|---|---|---|---|')
    for label, ids in runs:
        mine = [i for i in ids if sp32.get(i)]; rest = [i for l2, ids2 in runs if l2 != label for i in ids2 if sp32.get(i)]
        if not mine: print('| %s | - | - | - | %d | - |' % (label, len(ids))); continue
        f32 = min(mine, key=lambda i: sp32[i]); g32 = (min(sp32[i] for i in rest) / sp32[f32] - 1) if rest else 0.0
        f64 = min((i for i in ids if i in speed), key=lambda i: speed[i], default=None)
        v = ('-' if label not in VERDICT64 or not rest else ('small' if VERDICT64[label] and g32 < .05 else 'not small')) \
            if label.startswith('this clone') else '(an earlier run)'     # as the 64-bit table: the new run is judged
        print('| %s | %.3f (%s) | %+.1f%% | %s | %d | %s |' % (label, sp32[f32], f32, 100 * g32,
              ('%.3f (%s)' % (sp32[f64], f64)) if f64 and sp32.get(f64) else '-', sum(1 for i in ids if not sp32.get(i)), v))
if len(cpus) > 1:
    a, b = cpus[0], cpus[1]
    ids = sorted(i for i in S[a] if i != CAL)
    q = sorted(S[a][i] / S[b][i] for i in ids)
    ra = {i: k for k, i in enumerate(sorted(ids, key=lambda i: S[a][i]))}; rb = {i: k for k, i in enumerate(sorted(ids, key=lambda i: S[b][i]))}
    n = len(ids); rho = 1 - 6 * sum((ra[i] - rb[i]) ** 2 for i in ids) / (n * (n * n - 1)) if n > 1 else 1.0
    def front_on(c):
        return {i for i in ids if not any(dominates(S[c][j], S[c][i], j, i) for j in ids)}
    fa, fb = front_on(a), front_on(b)
    print('\n## The same session on two CPUs\n')
    print('Calibration on cpu %d: %.3f; on cpu %d: %.3f.\n' % (a, S[a].get(CAL, float('nan')), b, S[b].get(CAL, float('nan'))))
    print('Speed on cpu %d over speed on cpu %d, per design: median %.3f, 10-90%% %.3f-%.3f, extremes %.3f-%.3f; '
          'rank agreement (Spearman) %.2f.\n' % (a, b, q[len(q) // 2], q[len(q) // 10], q[9 * len(q) // 10], q[0], q[-1], rho))
    print('The front of all runs on cpu %d: %s' % (a, ', '.join('%s %.3f at %s' % (i, S[a][i], format(tot[i], ',')) for i in sorted(fa, key=lambda i: -tot[i]))))
    print('\nThe front of all runs on cpu %d: %s' % (b, ', '.join('%s %.3f at %s' % (i, S[b][i], format(tot[i], ',')) for i in sorted(fb, key=lambda i: -tot[i]))))
    print('\nOn both fronts: %d of %d and %d.' % (len(fa & fb), len(fa), len(fb)))
    print('\n| design | speed cpu %d | speed cpu %d | ratio |' % (a, b))
    print('|---|---|---|---|')
    for i in sorted(ids, key=lambda i: S[a][i]): print('| %s | %.3f | %.3f | %.3f |' % (i, S[a][i], S[b][i], S[a][i] / S[b][i]))
print('\n%s is held out (Iteration 41: loop was, until the owner put it in the selection). loop moves with an image\'s'
      ' size mod 8 - the NOOPs before (LOOP) in run-time code (Iteration 13) - except where rtloop compiles its opcodes.'
      % ', '.join((E.WORK_HELD + E.WORK_FAR)))
shutil.rmtree(os.path.join(E.EV, 'cmp'), ignore_errors=True)
