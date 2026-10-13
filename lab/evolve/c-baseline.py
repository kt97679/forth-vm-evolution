#!/usr/bin/env python3
"""c-baseline.py [--runs N] [IDS...] - the Forth designs against the same
benchmarks in C (bench/c/bench.c), Iteration 235.

The six benchmarks that are programs, not the system working on itself (the
kernel's cross-compile and the corpus have no C twin): fib, loop, sieve,
bubble, ackermann, parse - each the long version the evolver times (BENCH
repeated as evolve.py's LONG says), each in C doing the same work the same
number of times. CPU time from the evolver's own wrapper (build/cputime), the
median of N runs; each side's start-up - the engine loading its image and
the C program starting, measured with no work - subtracted, so what is
compared is the work. The C built -O2 (the baseline) and -O0 (code no
optimiser touched); the designs: hand-made s6 (the evolver's unit) and the
ids given - by default the fastest, the knee and the smallest of all runs.

The table: milliseconds, and each design as a multiple of C -O2's time. On
the development VM the timing noise is about 10%: a baseline to orient by;
the laptop measures it properly.
"""
import os, re, sys, subprocess, statistics, platform, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
args = sys.argv[1:]; sys.argv = [sys.argv[0]]
import evolve as E
E.setup()
RUNS = 5
if '--runs' in args: i = args.index('--runs'); RUNS = int(args[i + 1]); del args[i:i + 2]
IDS = args or ['28677d13b1', '0af26c8e89', 'add5ec8937']
WORKS = ['fib', 'loop', 'sieve', 'bubble', 'ackermann', 'parse']
PARSE = os.path.join(E.ROOT, 'bench', 'parse.fth')
D = os.path.join(E.O, 'c-baseline'); os.makedirs(D, exist_ok=True)

def cpu_ms(cmd, inp=None, cwd=None):
    r = subprocess.run([E.CPUT] + cmd, input=inp, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    m = re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    if not m or r.returncode: raise RuntimeError('%s: status %d %r' % (cmd[0], r.returncode, r.stderr[-200:]))
    return int(m.group(1)) / 1e6
def med(f): return statistics.median(f() for _ in range(RUNS))

src = os.path.join(E.ROOT, 'bench', 'c', 'bench.c'); cbin = {}
for opt in ('O2', 'O0'):
    cbin[opt] = os.path.join(D, 'bench-' + opt)
    if subprocess.run(['cc', '-' + opt, '-o', cbin[opt], src]).returncode: sys.exit('bench.c did not compile')
rows = {w: {} for w in WORKS}
for opt in ('O2', 'O0'):
    start = med(lambda: cpu_ms([cbin[opt], 'fib', '0']))
    for w in WORKS:
        rows[w]['C -' + opt] = max(0.001, med(lambda: cpu_ms([cbin[opt], w, str(E.LONG[w]), PARSE])) - start)
    print('C -%s: start-up %.2f ms' % (opt, start), flush=True)
designs = [('s6', E.canon(E.HUMAN['s6-cv8b']))] + [(i, E.canon(E.recorded_genome(i))) for i in IDS]
for name, g in designs:
    d = os.path.join(E.EV, 'cb-' + name); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); pw = E.private_work(d)
    start = med(lambda: cpu_ms([eng, img], b'BYE\n', pw))
    for w in WORKS:
        rows[w][name] = max(0.001, med(lambda: cpu_ms([eng, img], E.program(w), pw)) - start)
    print('%s: start-up %.2f ms' % (name, start), flush=True)
cols = ['C -O2', 'C -O0'] + [n for n, _ in designs]
out = ['| workload (long) | ' + ' | '.join(cols) + ' |', '|---|' + '---|' * len(cols)]
for w in WORKS:
    c = rows[w]['C -O2']
    out.append('| %s x%d | %s |' % (w, E.LONG[w], ' | '.join('%.1f' % rows[w][k] if k == 'C -O2' else '%.1f (%.1fx)' % (rows[w][k], rows[w][k] / c) for k in cols)))
g = {k: statistics.geometric_mean([rows[w][k] / rows[w]['C -O2'] for w in WORKS]) for k in cols[1:]}
out.append('| geometric mean, x C -O2 | 1 | ' + ' | '.join('%.1fx' % g[k] for k in cols[1:]) + ' |')
print('\n'.join(out))
host = re.sub(r'[^a-z0-9]+', '-', (platform.processor() or platform.machine()).lower()).strip('-')
open(os.path.join(E.ROOT, 'results', 'c-baseline-%s.md' % host), 'w').write(
    '# The Forth designs against the same benchmarks in C (lab/evolve/c-baseline.py)\n\n'
    'Milliseconds of CPU time, the median of %d runs, start-up subtracted; each design also as a multiple of C -O2. '
    'Host: %s. On the development VM timing is noisy (~10%%).\n\n' % (RUNS, platform.platform()) + '\n'.join(out) + '\n')
