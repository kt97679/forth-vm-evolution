#!/usr/bin/env python3
"""agree.py RESULTS.md... - do these runs agree with each other?

The one check this project has learned to insist on. Every wrong number
here was believed because it came from a single run: a loop benchmark
that swung 21% on the same machine, a packed-scheme result that reversed
between two boxes, a conclusion about calls that lasted exactly one
architecture.

For each stage and workload it compares the ratios across runs and asks
whether they sit inside their combined error bars. A row marked NO means
the stated uncertainty is too small - the measurement is missing a
source of variation, and no amount of averaging inside one run will
find it.
"""
import re
import sys

CELL = re.compile(r'^\|\s*`?([a-z0-9-]+)`?\s*\|(.+)\|\s*$')
NUM = re.compile(r'([\d.]+)\s*(?:±|\+/-)\s*([\d.]+)|([\d.]+)|--')


# Student's t at 95%, by degrees of freedom. A standard error computed
# from N layout variants has N-1 df, and at N=3 that is 2 - where a
# 2-sigma rule is more than twice too tight. Using 2.0 regardless made
# an ARM run with LAYOUTS=3 report a disagreement that was nothing but
# small-sample arithmetic.
T95 = {1: 12.71, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447,
       7: 2.365, 8: 2.306, 9: 2.262}


def tmul(nvar):
    if not nvar or nvar < 2:
        return 2.0
    return T95.get(nvar - 1, 2.0)


def parse(path):
    """((width, workload, stage) -> (ratio, se or None), variant count)."""
    out, width, cols = {}, None, None
    nvar = None
    for line in open(path):
        m = re.match(r'^## Speed, (\d+)-bit cells', line)
        if m:
            width = m.group(1)
            cols = None
            continue
        if width and line.startswith('| stage |'):
            cols = [c.strip() for c in line.strip('|\n').split('|')][1:]
            continue
        if width and cols and line.startswith('|'):
            m = CELL.match(line)
            if not m or m.group(1) == 'stage':
                continue
            stage = m.group(1)
            for col, cell in zip(cols, m.group(2).split('|')):
                cell = cell.strip()
                if cell in ('--', ''):
                    continue
                mm = re.match(r'([\d.]+)\s*(?:±|\+/-)\s*([\d.]+)$', cell)
                if mm:
                    out[(width, col, stage)] = (float(mm.group(1)),
                                                float(mm.group(2)))
                else:
                    try:
                        out[(width, col, stage)] = (float(cell), None)
                    except ValueError:
                        pass
        m = re.search(r'mean over (\d+) layout variant', line)
        if m:
            nvar = int(m.group(1))
        if line.startswith('## ') and 'Speed' not in line:
            width = None
    return out, nvar


parsed = [parse(p) for p in sys.argv[1:]]
runs = [r for r, _ in parsed]
nvars = [n for _, n in parsed if n]
TM = tmul(min(nvars)) if nvars else 2.0
if len(runs) < 2:
    sys.exit(0)

keys = set(runs[0])
for r in runs[1:]:
    keys &= set(r)

bad, checked, worst = [], 0, (0.0, None)
for k in sorted(keys):
    vals = [r[k] for r in runs]
    if any(se is None for _, se in vals):
        continue
    checked += 1
    lo = min(v for v, _ in vals)
    hi = max(v for v, _ in vals)
    span = hi - lo
    # combined band of the two extreme runs, at 95% for the number of
    # layout variants actually built
    ses = sorted(vals, key=lambda t: t[0])
    tol = TM * ((ses[0][1] ** 2 + ses[-1][1] ** 2) ** 0.5)
    rel = 100.0 * span / lo if lo else 0.0
    if rel > worst[0]:
        worst = (rel, k)
    if span > tol:
        bad.append((k, lo, hi, span, tol))

print("agreement across %d runs: %d comparisons (95%%, t=%.2f for %s"
      " layout variants)"
      % (len(runs), checked, TM, min(nvars) if nvars else '?'))
if not checked:
    print("  nothing comparable - were the runs saved with error bars?")
    sys.exit(0)
print("  widest spread: %.1f%% on %s/%s-bit/%s"
      % (worst[0], worst[1][1], worst[1][0], worst[1][2]) if worst[1] else "")
if not bad:
    print("  every figure agrees within its stated uncertainty.")
    sys.exit(0)
print("  %d figure(s) disagree by MORE than their error bars:" % len(bad))
for (w, col, st), lo, hi, span, tol in bad[:12]:
    print("    %-11s %-7s %s-bit: %.3f..%.3f (spread %.3f, allowed %.3f)"
          % (st, col, w, lo, hi, span, tol))
print()
print("  A disagreement here means the error bar is too small: some")
print("  source of variation is not being sampled. Suspect the workload")
print("  before the stages - short, narrow benchmarks do this.")
sys.exit(1)
