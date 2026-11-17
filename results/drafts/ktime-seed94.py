#!/usr/bin/env python3
"""results/drafts/ktime-seed94.py CPUTIME ROUNDS DIR ... - the 32-bit kernel workload (extend.4, then cross32.4) timed
on design builds kept by lab/evolve/design.py --keep DIR --width 4, alternating, by tools/cputime.c's CPUNS; the ratio to
the last DIR (Iteration 700: 2806f89619 against its parent 202caee13c, 21 rounds - 1.019)."""
import os, re, statistics as st, subprocess, sys

IN = b'S" extend.4" INCLUDED\nS" cross32.4" INCLUDED\n'
CPUT, rounds, dirs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
cpu, out = {d: [] for d in dirs}, {}
for _ in range(rounds):
    for d in dirs:
        p = subprocess.run(['taskset', '-c', '1', CPUT, os.path.join(d, 'engine'), os.path.join(d, 'image.img')],
                           cwd=os.path.join(d, 'work'), input=IN, capture_output=True, timeout=240)
        cpu[d].append(int(re.search(rb'^CPUNS (\d+)', p.stderr, re.M).group(1)) / 1e9)
        out[d] = (p.returncode, len(p.stdout))
base = st.median(cpu[dirs[-1]])
for d in dirs:
    m = st.median(cpu[d])
    print('%-24s median cpu %.5f s (min %.5f max %.5f)  exit/out %s  ratio to the last %.3f'
          % (os.path.basename(d), m, min(cpu[d]), max(cpu[d]), out[d], m / base))
