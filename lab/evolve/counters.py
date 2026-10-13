#!/usr/bin/env python3
"""counters.py [--runs N] [IDS...] - where the cycles go: hardware counters for the
designs on the selection workloads (Iteration 278; the laptop's - perf, real hardware).

The question, open since Iteration 243 (Ertl & Paysan): is an interpreted design
held back by mispredicted dispatch branches, or by the chain of dependent updates
to the instruction pointer - the question behind the deferred "IP-update loop form"
(Iteration 260), and gotodup's (copying the dispatch into more handlers predicts
better on some cores)? For each design and selection workload, `perf stat` counts
user-space cycles, instructions, branches and branch misses, the median of N runs:
instructions per cycle, and branch misses per thousand instructions. Low IPC with
few misses points at the dependency chain; many misses at prediction.

The designs: IDS, or from the newest run's front (evolve.newest_front) - the
fastest with the JIT, the fastest without it, the smallest - and hand-made s6.
Database paths, which next-run.sh's experiment passes, are not designs: ignored.

It needs perf and user-space counters - on Ubuntu, once: `sudo apt install
linux-tools-common linux-tools-$(uname -r)`; each boot: `sudo sysctl
kernel.perf_event_paranoid=2` (Ubuntu's default, 4, allows none). A counter perf
cannot read stops the tool: no figure from nothing. lab/evolve/RUNNING.md, "Between
runs", says when and how.

    sh lab/evolve/next-run.sh experiment counters.py       a pack to send back
"""
import os, platform, shutil, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
args = sys.argv[1:]; sys.argv = [sys.argv[0]]
RUNS = 5
if '--runs' in args: i = args.index('--runs'); RUNS = int(args[i + 1]); del args[i:i + 2]
IDS = [a for a in args if not a.endswith('.jsonl') and not os.path.exists(a)]
EVENTS = ['cycles:u', 'instructions:u', 'branches:u', 'branch-misses:u']

def parse(text):
    """perf stat -x, output -> {event: count}; exits on a counter it could not read."""
    vals = {}
    for line in text.splitlines():
        f = line.split(',')
        if len(f) < 3 or f[2] not in EVENTS: continue
        if not f[0].strip().isdigit():
            sys.exit('counters: perf could not read %s (%s) - user-space counters need '
                     '`sudo sysctl kernel.perf_event_paranoid=2`, and real hardware' % (f[2], f[0].strip() or 'empty'))
        vals[f[2]] = int(f[0])
    missing = [e for e in EVENTS if e not in vals]
    if missing: sys.exit('counters: perf gave no count for %s' % ', '.join(missing))
    return vals

if __name__ == '__main__':
    PERF = shutil.which('perf')
    if not PERF: sys.exit('counters: no perf - on Ubuntu: sudo apt install linux-tools-common linux-tools-$(uname -r)')
    import evolve as E
    E.setup()
    designs = [('s6', dict(E.HUMAN['s6-cv8b']))]
    if IDS: designs += [(i, E.recorded_genome(i)) for i in IDS]
    else:
        path, recs = E.newest_front()
        jit = [r for r in recs if r['genome'].get('jit')]; interp = [r for r in recs if not r['genome'].get('jit')]
        picks = ([min(jit, key=lambda r: r['speed'])] if jit else []) + ([min(interp, key=lambda r: r['speed'])] if interp else []) + [min(recs, key=lambda r: r['total'])]
        for r in picks:
            if r['id'] not in [d[0] for d in designs]: designs.append((r['id'], r['genome']))
    rows = []
    for name, g in designs:
        if g is None: sys.exit('counters: no recorded design %s' % name)
        d = os.path.join(E.EV, 'counters'); shutil.rmtree(d, ignore_errors=True)
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
        for wl in E.WORK_SEL:
            runs = []
            for _ in range(RUNS):
                r = subprocess.run([PERF, 'stat', '-x', ',', '-e', ','.join(EVENTS), '--', eng, img], input=E.program(wl),
                                   cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=600)
                if r.returncode: sys.exit('counters: %s on %s exited %d' % (name, wl, r.returncode))
                runs.append(parse(r.stderr.decode(errors='replace')))
            rows.append((name, wl, {e: statistics.median(x[e] for x in runs) for e in EVENTS}))
        shutil.rmtree(d, ignore_errors=True)
    print('# Hardware counters - designs on the selection workloads (lab/evolve/counters.py)\n')
    print('User-space counts, the median of %d runs. Host: %s, %s.\n' % (RUNS, platform.platform(), platform.processor() or platform.machine()))
    print('| design | workload | cycles (M) | instructions per cycle | branch misses per 1k instructions | misses per branch |')
    print('|---|---|---|---|---|---|')
    for name, wl, m in rows:
        c, i, b, bm = (m[e] for e in EVENTS)
        print('| %s | %s | %.1f | %.2f | %.2f | %.2f%% |' % (name, wl, c / 1e6, i / c, 1000.0 * bm / i, 100.0 * bm / b))
