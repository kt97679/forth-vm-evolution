#!/usr/bin/env python3
"""lucky.py [--step S] [--sweeps K] [--ids ID,...] DB [DB ...] - is the lucky
fib run a place on the stack?

Iteration 26. With address randomisation on, about one fib run in 40 is
34-38% faster for some designs (8dd8a7a146: 14.9 ms against a median of
23.9; never with randomisation off, never for s6 - Iteration 25,
results/run-spread-amd-ryzen-7-pro-8840hs.md). With it off every run lands
in one place. What randomisation moves between runs: the code, the heap
and the mappings - by whole pages - and the stack, by less than a page as
well. The stack is cheap to test: with randomisation off, the size of the
environment moves the initial stack by its own length and moves nothing
else (the classic measurement-bias effect). So: randomisation off, fib
timed with the environment padded by 0, S, 2S, ... bytes, a full page of
stack offsets, every design at every offset, K times over; and with
randomisation on, as many runs again, for the rate of lucky runs.

An offset that is fast every sweep is a place on the stack the engine could
choose for itself at start, every run. None means the luck lies in the
pages - the code's, the heap's - and not in the stack.

Iteration 27, on the laptop: no offset repeated - and the premise was
wrong. Fast runs come with randomisation off too, at the same rate as on
(0.4-2.3% of runs for some designs, never s6's): not a place at all.
results/lucky-amd-ryzen-7-pro-8840hs.md.
"""
import json, os, re, shutil, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; opt = {'--step': '16', '--sweeps': '2', '--ids': '8dd8a7a146,312ad2edaa,29ad5ba726'}
for k in list(opt):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
step, sweeps, want = int(opt['--step']), int(opt['--sweeps']), opt['--ids'].split(',')
pads = list(range(0, 4096, step))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)
R = {}
for db in args:
    for l in open(db):
        try: r = json.loads(l); R.setdefault(r['id'], r)
        except ValueError: pass
designs = [('s6-cv8b', E.canon(E.HUMAN['s6-cv8b']))] + [(i, E.canon(R[i]['genome'])) for i in want if i in R]
say('designs %s; missing %s' % (', '.join(i for i, _ in designs), ', '.join(i for i in want if i not in R) or 'none'))
built = []
for k, (i, g) in enumerate(designs):
    d = os.path.join(E.EV, 'lucky', '%02d' % k)
    eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw); built.append((i, eng, img, pw))
arch = os.uname().machine
def timed(eng, img, pw, pad, aslr):
    cmd = list(E.PIN) + ([] if aslr else ['setarch', arch, '-R']) + [E.CPUT, eng, img]
    r = E.sh(cmd, cwd=pw, inp=E.program('fib'), timeout=240, cpu=10, env=dict(os.environ, LUCKY_PAD='x' * pad))
    m = re.search(E.METRIC, r.stderr, re.M) or re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    if not m: raise RuntimeError('no time: %r' % r.stderr[-200:])
    return int(m.group(1)) / 1e6
off = {(i, s): {} for i, *_ in built for s in range(sweeps)}
for s in range(sweeps):
    for n, p in enumerate(pads if s % 2 == 0 else pads[::-1]):
        if n % 32 == 0: say('sweep %d of %d: offset %d' % (s + 1, sweeps, p))
        for i, eng, img, pw in (built if n % 2 == 0 else built[::-1]):
            off[(i, s)][p] = timed(eng, img, pw, p, False)
on = {i: [] for i, *_ in built}
for n in range(len(pads)):
    if n % 32 == 0: say('randomisation on: run %d of %d' % (n + 1, len(pads)))
    for i, eng, img, pw in built: on[i].append(timed(eng, img, pw, 0, True))

print('# Is the lucky fib run a place on the stack?\n')
print('Randomisation off: fib with the environment padded 0-%d bytes in steps of %d (%d stack offsets), %d sweeps; '
      'randomisation on: %d runs. Pinned: %s. Load at the end: %s.\n' % (pads[-1], step, len(pads), sweeps, len(pads),
      ' '.join(E.PIN) or 'no', ' '.join(open('/proc/loadavg').read().split()[:3])))
print('| design | median, off | lucky offsets (all sweeps under 0.85 of the median) | under 0.85 in some sweep | median, on | lucky runs, on |')
print('|---|---|---|---|---|---|')
for i, *_ in built:
    allt = [t for s in range(sweeps) for t in off[(i, s)].values()]; m = st.median(allt)
    every = [p for p in pads if all(off[(i, s)][p] < 0.85 * m for s in range(sweeps))]
    some = [p for p in pads if any(off[(i, s)][p] < 0.85 * m for s in range(sweeps))]
    mo = st.median(on[i]); lucky_on = [t for t in on[i] if t < 0.85 * mo]
    print('| %s | %.1f ms | %s | %d | %.1f ms | %d of %d (%s) |' % (i, m, ', '.join(map(str, every[:12])) + (' ...' if len(every) > 12 else '') or 'none',
          len(some), mo, len(lucky_on), len(on[i]), ', '.join('%.1f' % t for t in sorted(lucky_on)[:6]) or '-'))
print('\n## The offsets, sweep by sweep\n')
print('One character an offset, from 0 bytes on: `#` under 0.80 of the design\'s median, `+` under 0.90, `.` within, `o` over 1.10.\n')
print('```')
for i, *_ in built:
    m = st.median([t for s in range(sweeps) for t in off[(i, s)].values()])
    for s in range(sweeps):
        row = ''.join('#' if off[(i, s)][p] < 0.8 * m else '+' if off[(i, s)][p] < 0.9 * m else 'o' if off[(i, s)][p] > 1.1 * m else '.' for p in pads)
        print('%-10s sweep %d  %s' % (i, s + 1, row))
print('```')
print('\n## Randomisation on, every run, ms, sorted\n')
print('```')
for i, *_ in built: print('%-10s %s' % (i, ' '.join('%.1f' % t for t in sorted(on[i]))))
print('```')
