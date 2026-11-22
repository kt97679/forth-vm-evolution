#!/usr/bin/env python3
"""results/drafts/data-layout-cache-734.py BASE NEW NAME ... - the fixed data layout's caches (Iteration 734): each role's
engine and image as data-layout-734.py left them (build/evolve/dlay-NAME in each tree) run under cachegrind with its
cache simulation (--cache-sim=yes: the host's L1 and last level), the corpus and the kernel workload - instructions,
data reads and writes missed at L1 and at the last level, NEW against BASE. The timing is the laptop's; this shows the
layout moves no cache traffic the wrong way."""
import os, re, subprocess, sys
BASE, NEW, names = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, os.path.join(NEW, 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
def cg(d, w):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=yes', '--cachegrind-out-file=/dev/null',
                        os.path.join(d, 'engine'), os.path.join(d, 'image.img')], input=E.program(w), cwd=os.path.join(d, 'work'),
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=3600)
    v = {}
    for k, pat in (('I', rb'I\s+refs:\s+([\d,]+)'), ('D1', rb'D1  misses:\s+([\d,]+)'), ('LLd', rb'LLd misses:\s+([\d,]+)')):
        m = re.findall(pat, p.stderr); v[k] = int(m[-1].replace(b',', b'')) if m else 0
    return v
print('| role | workload | instructions new / base | L1 data misses base -> new | last-level data misses base -> new |')
print('|---|---|---:|---:|---:|')
for n in names:
    for w in ('corpus', 'kernel'):
        a, b = (cg(os.path.join(t, 'build', 'evolve', 'dlay-' + n), w) for t in (BASE, NEW))
        print('| %s | %s | %.4f | %d -> %d (%+.2f %%) | %d -> %d |' % (n, w, b['I'] / a['I'], a['D1'], b['D1'],
              100.0 * (b['D1'] - a['D1']) / max(1, a['D1']), a['LLd'], b['LLd']), flush=True)
