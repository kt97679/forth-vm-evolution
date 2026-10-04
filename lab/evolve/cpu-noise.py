#!/usr/bin/env python3
"""cpu-noise.py [--rounds N] [--cpus A,B] [--ids ID,...] [--work W,...] DB [DB ...]
- does a design's ratio to hand-made s6 depend on the CPU it is pinned to?

Iteration 23. Two sessions of `next-run.sh compare`, both calibrated (s6
against itself 0.991 and 0.996), disagreed on fib by up to 28% for single
designs - 8dd8a7a146 0.677, then 0.531 - while kernel, parse and corpus
moved 2-5%. The sessions were pinned to different logical CPUs: 8, then 2.
Address randomisation is not it on the development VM (one Intel CPU):
2-6% spread either way, the best of 15 unmoved.

Here, in ONE session: the designs whose fib moved most between those two
sessions, and hand-made s6, timed on each listed logical CPU and on its
SMT sibling (from /sys), interleaved round by round, every run paired with
s6 on the same CPU. If a design's ratio differs by CPU, the pinning is the
cause - by core, or by thread and what its sibling runs - and that says
what the measurement must fix. kernel is timed too, as the control that
moved little.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; opt = {'--rounds': '20', '--cpus': '2,8', '--work': 'fib,kernel',
       '--ids': '8dd8a7a146,312ad2edaa,550df563ee,29ad5ba726,6463752a82,1769ca2a48'}
for k in list(opt):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
rounds, works, want = int(opt['--rounds']), opt['--work'].split(','), opt['--ids'].split(',')
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)

def siblings(c):
    try: s = open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().strip()
    except OSError: return [c]
    out = []
    for part in s.split(','):
        a, _, b = part.partition('-'); out += list(range(int(a), int(b or a) + 1))
    return out
online = [c for c in range(os.cpu_count() or 1) if os.path.exists('/sys/devices/system/cpu/cpu%d' % c)]
cpus = []
for c in [int(x) for x in opt['--cpus'].split(',')]:
    if c not in online: continue
    for s in sorted(siblings(c), key=lambda s: s != c):
        if s not in cpus: cpus.append(s)
if not cpus: cpus = [0]

R = {}
for db in args:
    for l in open(db):
        try: r = json.loads(l); R.setdefault(r['id'], r)
        except ValueError: pass
designs = [('s6-cv8b', E.canon(E.HUMAN['s6-cv8b']))] + [(i, E.canon(R[i]['genome'])) for i in want if i in R]
say('designs: %s; missing from the databases: %s' % (', '.join(i for i, _ in designs), ', '.join(i for i in want if i not in R) or 'none'))
built = []
for k, (i, g) in enumerate(designs):
    d = os.path.join(E.EV, 'cpunoise', '%02d' % k)
    eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw); built.append((i, eng, img, pw))
ref = E.REF[:3]
T = {}                                   # (design, cpu, work, 'd'|'r') -> [ns, ...]
for r_ in range(rounds):
    say('round %d of %d' % (r_ + 1, rounds))
    for ci, c in enumerate(cpus):
        E.PIN[:] = ['taskset', '-c', str(c)]
        for j, (i, eng, img, pw) in enumerate(built):
            for w in works:
                pair = [((eng, img, pw), 'd'), (ref, 'r')]
                for (e, im, p), side in (pair if (r_ + ci + j) % 2 == 0 else pair[::-1]):
                    T.setdefault((i, c, w, side), []).append(E.run_metric(e, im, p, w))

print('# Does the CPU change a design\'s ratio?\n')
print('%d rounds; logical CPUs %s (each listed CPU with its SMT siblings: %s); every run paired with hand-made s6 on the same CPU;'
      ' a ratio is best design run over best s6 run, on that CPU. Load at the end: %s.\n'
      % (rounds, ', '.join(map(str, cpus)), '; '.join('%d: %s' % (c, siblings(c)) for c in cpus), open('/proc/loadavg').read().split()[:3]))
for w in works:
    print('## %s\n' % w)
    print('| design | ' + ' | '.join('cpu %d' % c for c in cpus) + ' | most / least |')
    print('|---|' + '---|' * (len(cpus) + 1))
    for i, *_ in built:
        q = [min(T[(i, c, w, 'd')]) / min(T[(i, c, w, 'r')]) for c in cpus]
        print('| %s | %s | %.3f |' % (i, ' | '.join('%.3f' % x for x in q), max(q) / min(q)))
    print('| s6 best, ms | %s | %.3f |' % (' | '.join('%.1f' % (min(T[('s6-cv8b', c, w, 'r')]) / 1e6) for c in cpus),
          max(min(T[('s6-cv8b', c, w, 'r')]) for c in cpus) / min(min(T[('s6-cv8b', c, w, 'r')]) for c in cpus)))
    sp = []
    for i, *_ in built:
        for c in cpus:
            t = sorted(T[(i, c, w, 'd')]); sp.append((t[len(t) // 2] - t[0]) / t[0])
    print('\nWithin one CPU, a design\'s median run is %.1f%% above its best (median over designs and CPUs), '
          'so a difference between CPUs well above that is the CPU.\n' % (100 * sorted(sp)[len(sp) // 2]))
