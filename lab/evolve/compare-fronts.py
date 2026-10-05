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
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
dbs = [os.path.abspath(a) for a in args]
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
home = os.path.expanduser('~')
def say(*a): print(*a, file=sys.stderr, flush=True)

runs, rec = [], {}                  # [(label, [ids])]; id -> (genome, recorded size, recorded speed)
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
    runs.append((label, ids)); say('%s: %d designs (%s)' % (label, len(ids), how))
    for i in ids: rec.setdefault(i, (E.canon(R[i]['genome']), R[i]['size'], sp[i]))
CAL = 's6-cv8b'
rec[CAL] = (E.canon(E.HUMAN['s6-cv8b']), None, 1.0)

live, size, dead = [], {}, {}
for k, (i, (g, _, _)) in enumerate(sorted(rec.items())):
    d = os.path.join(E.EV, 'cmp', '%03d' % k)
    try:
        eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw)
        live.append((i, eng, img, pw)); size[i] = os.path.getsize(img)
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
            for w in E.WORK_SEL + E.WORK_HELD:
                pair = [((eng, img, pw), 'd'), (E.REF, 'r')]
                for (e, im, p), side in (pair if (r_ + j + ci) % 2 == 0 else pair[::-1]):
                    times.setdefault((i, w, side, c), []).append(E.run_metric(e, im, p, w))
E.PIN[:] = pin0
med = statistics.median
T = {c: {i: {w: med(times[(i, w, 'd', c)]) / med(times[(i, w, 'r', c)]) for w in E.WORK_SEL + E.WORK_HELD} for i, *_ in live} for c in cpus}
S = {c: {i: math.exp(sum(math.log(T[c][i][w]) for w in E.WORK_SEL) / len(E.WORK_SEL)) for i in T[c]} for c in cpus}
c0 = cpus[0]; t, speed = T[c0], S[c0]

cal = speed.get(CAL)
print('# Fronts measured again in one session\n')
print('%d rounds, the median of them; every design paired with hand-made s6 on the same CPU (%s); designs built with this commit.\n'
      % (rounds, ', '.join('the pinned one' if c is None else 'cpu %d' % c for c in cpus)))
if cal is None: print('**No calibration: hand-made s6 did not build or pass the gate.**\n')
else:
    print('**Calibration: hand-made s6 against itself %.3f** (%s).%s\n' % (cal, ', '.join('%s %.3f' % (w, t[CAL][w]) for w in E.WORK_SEL + E.WORK_HELD),
          '' if 0.98 <= cal <= 1.02 else ' OUTSIDE 0.98-1.02: this session cannot rank designs a few per cent apart.'))
def front(ids):
    ids = [i for i in ids if i in speed]
    return [i for i in ids if not any(speed[j] <= speed[i] and size[j] <= size[i] and (speed[j], size[j]) != (speed[i], size[i]) for j in ids)]
allf = front([i for i in speed if i != CAL])
print('| run | design | speed now | recorded | size now | recorded | kernel | fib | parse | corpus | loop | on the front of all |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for label, ids in runs:
    for i in sorted(ids, key=lambda i: (size.get(i, 1 << 30), speed.get(i, 9))):
        g, rs, rp = rec[i]
        if i in dead: print('| %s | %s | %s | %.3f | | %s | | | | | | |' % (label, i, dead[i], rp, format(rs, ',')))
        else: print('| %s | %s | %.3f | %.3f | %s | %s | %s | %s |' % (label, i, speed[i], rp, format(size[i], ','), format(rs, ','),
                    ' | '.join('%.3f' % t[i][w] for w in E.WORK_SEL + E.WORK_HELD), 'yes' if i in allf else ''))
print('\nThe front of all runs together, by size: ' + ', '.join('%s %.3f at %s' % (i, speed[i], format(size[i], ','))
      for i in sorted(allf, key=lambda i: -size[i])))
if len(cpus) > 1:
    a, b = cpus[0], cpus[1]
    ids = sorted(i for i in S[a] if i != CAL)
    q = sorted(S[a][i] / S[b][i] for i in ids)
    ra = {i: k for k, i in enumerate(sorted(ids, key=lambda i: S[a][i]))}; rb = {i: k for k, i in enumerate(sorted(ids, key=lambda i: S[b][i]))}
    n = len(ids); rho = 1 - 6 * sum((ra[i] - rb[i]) ** 2 for i in ids) / (n * (n * n - 1)) if n > 1 else 1.0
    def front_on(c):
        return {i for i in ids if not any(S[c][j] <= S[c][i] and size[j] <= size[i] and (S[c][j], size[j]) != (S[c][i], size[i]) for j in ids)}
    fa, fb = front_on(a), front_on(b)
    print('\n## The same session on two CPUs\n')
    print('Calibration on cpu %d: %.3f; on cpu %d: %.3f.\n' % (a, S[a].get(CAL, float('nan')), b, S[b].get(CAL, float('nan'))))
    print('Speed on cpu %d over speed on cpu %d, per design: median %.3f, 10-90%% %.3f-%.3f, extremes %.3f-%.3f; '
          'rank agreement (Spearman) %.2f.\n' % (a, b, q[len(q) // 2], q[len(q) // 10], q[9 * len(q) // 10], q[0], q[-1], rho))
    print('The front of all runs on cpu %d: %s' % (a, ', '.join('%s %.3f at %s' % (i, S[a][i], format(size[i], ',')) for i in sorted(fa, key=lambda i: -size[i]))))
    print('\nThe front of all runs on cpu %d: %s' % (b, ', '.join('%s %.3f at %s' % (i, S[b][i], format(size[i], ',')) for i in sorted(fb, key=lambda i: -size[i]))))
    print('\nOn both fronts: %d of %d and %d.' % (len(fa & fb), len(fa), len(fb)))
    print('\n| design | speed cpu %d | speed cpu %d | ratio |' % (a, b))
    print('|---|---|---|---|')
    for i in sorted(ids, key=lambda i: S[a][i]): print('| %s | %.3f | %.3f | %.3f |' % (i, S[a][i], S[b][i], S[a][i] / S[b][i]))
print('\nloop is held out, and moves with an image\'s size mod 8 (Iteration 13).')
shutil.rmtree(os.path.join(E.EV, 'cmp'), ignore_errors=True)
