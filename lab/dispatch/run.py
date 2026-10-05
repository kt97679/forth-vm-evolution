#!/usr/bin/env python3
"""run.py - build lab/dispatch/dispatch.c and time every variant.

    lab/dispatch/run.py [ROUNDS]

Builds dispatch.c twice - with the compiler's defaults, and with
-fcf-protection=none, which drops the endbr64 marker Ubuntu's compiler
puts at every indirect-jump target (Linux does not enforce it for user
programs, so it is decode overhead on every dispatch) - and with clang
too, if there is one. Every variant must print the same answer as the
switch baseline before anything is timed. Then each configuration is run
ROUNDS times, interleaved, through tools/cputime; the median is kept
(the minimum until Iteration 29).
With hardware counters (see tools/cputime.c) it reports cycles and
instructions per cycle as well; otherwise CPU time.
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CPUT = os.path.join(ROOT, 'build', 'cputime')
SRC = os.path.join(HERE, 'dispatch.c')
VARIANTS = ['switch', 'token', 'direct', 'itc', 'tail', 'native', 'native2']
PROGRAMS = ['fib', 'loop', 'sieve']
ROUNDS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CPU = os.environ.get('BENCH_CPU') or '0'
PIN = ['taskset', '-c', CPU] if shutil.which('taskset') else []

if not os.access(CPUT, os.X_OK):
    subprocess.run(['cc', '-O2', '-o', CPUT, os.path.join(ROOT, 'tools', 'cputime.c')], check=True)

builds = [('gcc', ['cc', '-O2']), ('gcc, no endbr64', ['cc', '-O2', '-fcf-protection=none'])]
if shutil.which('clang'):
    builds.append(('clang, no endbr64', ['clang', '-O2', '-fcf-protection=none']))
bins = []
for name, cc in builds:
    out = os.path.join('/tmp', 'dispatch-' + re.sub(r'\W+', '-', name))
    r = subprocess.run(cc + ['-o', out, SRC], capture_output=True, text=True)
    if r.returncode:
        print('%s: did not build\n%s' % (name, r.stderr)); continue
    bins.append((name, out))

def answer(b, v, p, s):
    return subprocess.run([b, v, p] + (['-s'] if s else []), capture_output=True, text=True).stdout.strip()
for name, b in bins:
    for p in PROGRAMS:
        want = answer(b, 'switch', p, False)
        for v in VARIANTS:
            for s in (False, True):
                got = answer(b, v, p, s)
                if got != want:
                    sys.exit('%s: %s %s%s gave %s, switch gave %s' % (name, v, p, ' -s' if s else '', got, want))
print('every variant agrees on every program, in every build (%d builds)' % len(bins))

configs = [(n, b, v, p, s) for n, b in bins for p in PROGRAMS for v in VARIANTS for s in (False, True)]
best = {}
for r in range(ROUNDS):
    print('round %d of %d ...' % (r + 1, ROUNDS), flush=True)
    for c in configs:
        n, b, v, p, s = c
        out = subprocess.run(PIN + [CPUT, b, v, p] + (['-s'] if s else []), capture_output=True)
        for k in ('CPUNS', 'CYCLES', 'INSTR'):
            m = re.search(rb'^%s (\d+)' % k.encode(), out.stderr, re.M)
            if m:
                best.setdefault(c, {}).setdefault(k, []).append(int(m.group(1)))
import statistics       # Iteration 29: the median of the rounds, as the evolver since Iteration 25 - the best is luck
best = {c: {k: statistics.median(v) for k, v in d.items()} for c, d in best.items()}

cyc = all('CYCLES' in best[c] for c in configs)
for n, b in bins:
    print('\n%s - %s, median of %d; ratio to switch without superinstructions' % (
        n, 'Mcycles and instructions per cycle' if cyc else 'CPU ms', ROUNDS))
    print('    %-18s' % 'variant' + ''.join('%26s' % p for p in PROGRAMS))
    for v in VARIANTS:
        for s in (False, True):
            row = '    %-18s' % (v + (' + super' if s else ''))
            for p in PROGRAMS:
                x, base = best[(n, b, v, p, s)], best[(n, b, 'switch', p, False)]
                if cyc:
                    val, ref = x['CYCLES'], base['CYCLES']
                    row += '%26s' % ('%.1f  %.3f  ipc %.2f' % (val / 1e6, val / ref, x['INSTR'] / val))
                else:
                    val, ref = x['CPUNS'], base['CPUNS']
                    row += '%26s' % ('%.1f  %.3f' % (val / 1e6, val / ref))
            print(row)
