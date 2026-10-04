#!/usr/bin/env python3
"""compare-fronts.py DB [DB ...] [--rounds N] - the fronts of several runs,
measured again in ONE session (Iteration 20).

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
"""
import json, math, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; rounds = 10
if '--rounds' in args: i = args.index('--rounds'); rounds = int(args[i + 1]); del args[i:i + 2]
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
    label = db.replace(home, '~', 1)
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
best = {}
for r_ in range(rounds):
    say('round %d of %d' % (r_ + 1, rounds))
    n = len(live); order = live[r_ % n:] + live[:r_ % n]
    for j, (i, eng, img, pw) in enumerate(order):
        for w in E.WORK_SEL + E.WORK_HELD:
            pair = [((eng, img, pw), 'd'), (E.REF, 'r')]
            for (e, im, p), side in (pair if (r_ + j) % 2 == 0 else pair[::-1]):
                key = (i, w, side); best[key] = min(best.get(key, 1 << 62), E.run_metric(e, im, p, w))
t = {i: {w: best[(i, w, 'd')] / best[(i, w, 'r')] for w in E.WORK_SEL + E.WORK_HELD} for i, *_ in live}
speed = {i: math.exp(sum(math.log(t[i][w]) for w in E.WORK_SEL) / len(E.WORK_SEL)) for i in t}

cal = speed.get(CAL)
print('# Fronts measured again in one session\n')
print('%d rounds, every design paired with hand-made s6 on the pinned core; designs built with this commit.\n' % rounds)
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
print('\nloop is held out, and moves with an image\'s size mod 8 (Iteration 13).')
shutil.rmtree(os.path.join(E.EV, 'cmp'), ignore_errors=True)
