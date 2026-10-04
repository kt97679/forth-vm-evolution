#!/usr/bin/env python3
"""run-spread.py [--runs N] [--cpus A,B] [--ids ID,...] DB [DB ...] - every
run kept: how a design's runs spread, whether address randomisation spreads
them, and which estimator - the best run or the median - two halves of one
session agree on.

Iteration 24. cpu-noise.py (Iteration 23's experiment) found fib's best-run
ratio moving a design 7-20% between four CPUs of one session - between the
two threads of ONE core too - while kernel's agreed within 2.4%, though
both spread wide run to run (median 11% and 8.5% above the best). The
evolver ranks by the best of N runs: right when noise only adds time, wrong
if a design's speed depends on where each run lands in memory - address
randomisation draws a new placement every run, and the best of 20 is then
the luckiest placement drawn, a different one each session.

Here every run is kept: fib timed N times per design on two CPUs of two
cores, with randomisation on and off (setarch -R), every run paired with
hand-made s6 on the same CPU; kernel on the first CPU as the control. The
first and second halves of the runs stand for two sessions: an estimator
whose halves agree is one two sessions will agree on.
"""
import json, os, re, shutil, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; opt = {'--runs': '40', '--cpus': '2,8',
       '--ids': '8dd8a7a146,312ad2edaa,550df563ee,29ad5ba726,6463752a82,1769ca2a48'}
for k in list(opt):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
runs, want = int(opt['--runs']) // 2 * 2, opt['--ids'].split(',')
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)
have = [c for c in range(os.cpu_count() or 1) if os.path.exists('/sys/devices/system/cpu/cpu%d' % c)]
cpus = [c for c in map(int, opt['--cpus'].split(',')) if c in have] or have[:1]
taskset = shutil.which('taskset') is not None
R = {}
for db in args:
    for l in open(db):
        try: r = json.loads(l); R.setdefault(r['id'], r)
        except ValueError: pass
designs = [('s6-cv8b', E.canon(E.HUMAN['s6-cv8b']))] + [(i, E.canon(R[i]['genome'])) for i in want if i in R]
say('designs %s; missing %s; cpus %s' % (', '.join(i for i, _ in designs), ', '.join(i for i in want if i not in R) or 'none', cpus))
built = []
for k, (i, g) in enumerate(designs):
    d = os.path.join(E.EV, 'spread', '%02d' % k)
    eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw); built.append((i, eng, img, pw))
ref = E.REF[:3]
def timed(eng, img, pw, w, cpu, aslr):
    cmd = (['taskset', '-c', str(cpu)] if taskset else []) + ([] if aslr else ['setarch', os.uname().machine, '-R']) + [E.CPUT, eng, img]
    r = E.sh(cmd, cwd=pw, inp=E.program(w), timeout=240, cpu=10)
    m = re.search(E.METRIC, r.stderr, re.M) or re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    if not m: raise RuntimeError('no time from %s: %r' % (cmd, r.stderr[-200:]))
    return int(m.group(1))
T = {}          # (design, work, cpu, aslr) -> [(design ns, s6 ns), ...] in the order run
cells = [('fib', c, a) for c in cpus for a in (True, False)] + [('kernel', cpus[0], True)]
for k in range(runs):
    say('run %d of %d' % (k + 1, runs))
    for ci, (w, c, a) in enumerate(cells if k % 2 == 0 else cells[::-1]):
        if w == 'kernel' and k % 2: continue                       # the control: half as many
        for j, (i, eng, img, pw) in enumerate(built):
            pair = [(eng, img, pw), ref]
            if (k + ci + j) % 2: pair = pair[::-1]
            t = [timed(e, im, p, w, c, a) for e, im, p in pair]
            T.setdefault((i, w, c, a), []).append(tuple(t) if (k + ci + j) % 2 == 0 else tuple(t[::-1]))

def est(xs, how): return min(xs) if how == 'best' else st.median(xs)
def ratio(pairs, how): return est([d for d, _ in pairs], how) / est([r for _, r in pairs], how)
print('# How a design\'s runs spread, and which estimator reproduces\n')
print('%d runs a cell (kernel %d), each paired with hand-made s6 on the same CPU; CPUs %s; randomisation on, and off with '
      '`setarch -R`. Halves: the first and second half of the runs, in the order made. Load at the end: %s.\n'
      % (runs, runs // 2, ', '.join(map(str, cpus)), ' '.join(open('/proc/loadavg').read().split()[:3])))
summary = []
for w, c, a in cells:
    print('## %s, cpu %s, randomisation %s\n' % (w, c, 'on' if a else 'off'))
    print('| design | best run, ms | median, ms | spread median/best | ratio by best | ratio by median | halves agree, best | halves agree, median |')
    print('|---|---|---|---|---|---|---|---|')
    for i, *_ in built:
        p = T[(i, w, c, a)]; h = len(p) // 2; d = sorted(x for x, _ in p)
        hb = ratio(p[:h], 'best') / ratio(p[h:], 'best'); hm = ratio(p[:h], 'median') / ratio(p[h:], 'median')
        summary.append((w, c, a, i, hb, hm))
        print('| %s | %.1f | %.1f | %.3f | %.3f | %.3f | %.3f | %.3f |' % (i, d[0] / 1e6, st.median(d) / 1e6, st.median(d) / d[0],
              ratio(p, 'best'), ratio(p, 'median'), hb, hm))
    print()
print('## Which estimator reproduces\n')
print('Halves disagree by, over the designs (median, worst):\n')
print('| cell | best run | median run |')
print('|---|---|---|')
for w, c, a in cells:
    s = [(abs(hb - 1), abs(hm - 1)) for (w2, c2, a2, _, hb, hm) in summary if (w2, c2, a2) == (w, c, a)]
    print('| %s, cpu %s, randomisation %s | %.1f%%, %.1f%% | %.1f%%, %.1f%% |' % (w, c, 'on' if a else 'off',
          100 * st.median(x for x, _ in s), 100 * max(x for x, _ in s), 100 * st.median(y for _, y in s), 100 * max(y for _, y in s)))
if len(cpus) > 1:
    print('\nAcross the CPUs (fib, cpu %d over cpu %d), per design: by best run / by median:\n' % (cpus[0], cpus[1]))
    for a in (True, False):
        print('- randomisation %s: %s' % ('on' if a else 'off', ', '.join('%s %.3f / %.3f' % (i, ratio(T[(i, 'fib', cpus[0], a)], 'best') / ratio(T[(i, 'fib', cpus[1], a)], 'best'),
              ratio(T[(i, 'fib', cpus[0], a)], 'median') / ratio(T[(i, 'fib', cpus[1], a)], 'median')) for i, *_ in built)))
print('\n## Every fib run, ms, sorted\n')
print('```')
for w, c, a in cells:
    if w != 'fib': continue
    for i, *_ in built:
        print('%-10s cpu %s %-3s %s' % (i, c, 'on' if a else 'off', ' '.join('%.1f' % (x / 1e6) for x in sorted(x for x, _ in T[(i, w, c, a)]))))
print('```')
