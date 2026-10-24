#!/usr/bin/env python3
"""contention.py [--sample N] [--rounds R] [--workers K] DB [DB ...] - does the fast end's ratio to s6 depend on
co-runners? (Iteration 514; results/drafts/ask-noise-answers-513.md)

Every run's fastest tenth comes out 7-10% slower when re-measured after the run (rule 3). Not noise: one in-run reading's
is ~1% (seed 70: 1,130 gated designs read twice) and the gate's second readings are only 0.07% slower than the lucky
first ones; and every reading is already paired with s6, back to back, alternating. What differs is the context - in
the run, three other workers measure and build beside each design; the re-measure runs alone. The pair cancels load
that slows a design and s6 alike, not load that slows them differently.

So here, for the N fastest of the first database's front: the design measured exactly as the run measures it
(measure(): R rounds, paired with s6), alone and beside K co-runners - each looping hand-made s6 or a front design over
the selection workloads on a core of its own, as the run's workers - in the order alone, loaded, loaded, alone
(drift cancels), each condition the geometric mean of its two. If the loaded ratio matches the in-run speed and the
alone one is the 7-10% slower, the offset is contention: the search then optimises the speed beside co-runners, not
the speed a user sees alone - the owner's choice which. stdout: the report; stderr: progress.
"""
import json, math, os, random, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; opt = {'--sample': '16', '--rounds': '3', '--workers': '3'}
for k in list(opt):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
N, ROUNDS, K = int(opt['--sample']), int(opt['--rounds']), int(opt['--workers'])
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)

R = {}
for l in open(args[0]):
    try: r = json.loads(l)
    except ValueError: continue
    if r.get('id'): R[r['id']] = r
ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss')]
front = sorted(E.first_front(ok, R), key=lambda i: R[i]['speed'])[:N]
say('contention.py: %d designs, the fastest of a front of %d; %d co-runners; %d rounds' % (len(front), len(E.first_front(ok, R)), K, ROUNDS))

# the cores: the measured one (setup's quiet core), the co-runners on others - not it or its SMT sibling
cpus = sorted(os.sched_getaffinity(0))
mine = int(E.PIN[-1]) if E.PIN else None
def sib(c):
    try: return {int(x) for x in open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().replace('-', ',').split(',') if x.strip()}
    except (OSError, ValueError): return {c}
busy = sib(mine) if mine is not None else set()
others = [c for c in cpus if c not in busy]
if len(others) < K: say('only %d cores beside the measured one: the co-runners share them' % len(others))
prog = os.path.join(E.EV, 'contention-prog')
os.makedirs(prog, exist_ok=True)
for w in E.WORK_SEL: open(os.path.join(prog, w + '.fth'), 'wb').write(E.program(w, single=True))
hog = os.path.join(prog, 'hog.sh')
open(hog, 'w').write('while true; do for w in %s; do "$1" "$2" < %s/$w.fth > /dev/null 2>&1; done; done\n' % (' '.join(E.WORK_SEL), prog))

def ratio(eng, img, pw):
    t, _ = E.measure(eng, img, pw, E.WORK_SEL, ROUNDS)
    return math.exp(sum(math.log(t[w]) for w in E.WORK_SEL) / len(E.WORK_SEL))

built = {}                                 # co-runner engines: s6 and the front's other designs, as the run's workers mix them
def corunner_engines():
    out = [(E.REF[0], E.REF[1])]
    for i in front:
        if i in built: out.append(built[i][:2])
    return out
def start(k):
    eng = corunner_engines(); hs = []
    for n in range(k):
        e, im = random.Random(n).choice(eng)
        pin = ['taskset', '-c', str(others[n % len(others)])] if others and shutil.which('taskset') else []
        hs.append(subprocess.Popen(pin + ['sh', hog, e, im], cwd=E.REF[2] if len(E.REF) > 2 else None,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True))
    time.sleep(1.0)
    return hs
def stop(hs):
    for h in hs:
        try: os.killpg(h.pid, 9)
        except OSError: pass
    for h in hs: h.wait()

rows = []
for n, i in enumerate(front):
    d = os.path.join(E.EV, 'contention-' + i); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(R[i]['genome']), d); pw = E.private_work(d); built[i] = (eng, img, pw)
        a1 = ratio(eng, img, pw)
        hs = start(K); l1 = ratio(eng, img, pw); l2 = ratio(eng, img, pw); stop(hs)
        a2 = ratio(eng, img, pw)
        alone, loaded = math.sqrt(a1 * a2), math.sqrt(l1 * l2)
        rows.append((i, R[i]['speed'], alone, loaded))
        say('  %s in the run %.4f | alone %.4f | beside %d %.4f | loaded/alone %.3f' % (i, R[i]['speed'], alone, K, loaded, loaded / alone))
    except Exception as e:
        say('  %s: %s' % (i, str(e)[:120]))
for i, (eng, img, pw) in built.items(): shutil.rmtree(os.path.dirname(eng), ignore_errors=True)

def med(xs):
    xs = sorted(xs); m = len(xs)
    return (xs[m // 2] + xs[(m - 1) // 2]) / 2 if m else float('nan')
print('# Contention: the fast end measured alone and beside co-runners (lab/evolve/contention.py)\n')
print('The %d fastest of %s\'s front, each measured as the run measures it (%d rounds, paired with hand-made s6), alone '
      'and beside %d co-runners on other cores, in the order alone, loaded, loaded, alone. A speed is design/s6 - lower '
      'is faster.\n' % (len(rows), args[0], ROUNDS, K))
print('| design | in the run | alone | beside %d | loaded / alone | alone / in the run | loaded / in the run |' % K)
print('|---|---|---|---|---|---|---|')
for i, s, a, l in rows:
    print('| %s | %.4f | %.4f | %.4f | %.3f | %.3f | %.3f |' % (i, s, a, l, l / a, a / s, l / s))
if rows:
    la, ar, lr = med([l / a for _, _, a, l in rows]), med([a / s for _, s, a, _ in rows]), med([l / s for _, s, _, l in rows])
    print('\n**Medians**: loaded / alone %.3f; alone / in the run %.3f (rule 3\'s figure, measured here); loaded / in the run %.3f.\n' % (la, ar, lr))
    if abs(lr - 1) < abs(ar - 1) / 2 and abs(la - 1) > 0.02:
        print('**Reading**: the co-runners account for the offset - beside them the speeds are the run\'s; alone they are '
              '%.1f%% slower. The search optimises the speed beside co-runners.' % (100 * (1 / la - 1)))
    elif abs(la - 1) <= 0.02:
        print('**Reading**: co-runners change the ratio by %.1f%% at most in the median - not the cause; the offset is '
              'elsewhere (the rounds, the moment, the selection).' % (100 * abs(la - 1)))
    else:
        print('**Reading**: co-runners move the ratio (%.3f) but do not account for the whole offset (loaded / in the run '
              '%.3f) - part of it is contention, part elsewhere.' % (la, lr))
