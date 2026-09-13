#!/usr/bin/env python3
"""report.py DATFILE WIDTH REPS NAME STAGE... - one table, one method.

Reads `stage engine nanoseconds` lines: one per binary per round. Every
harness uses this, so the five workloads cannot report their numbers in
five subtly different ways, which is how they had started to drift.

Per binary we keep the MINIMUM across rounds - run noise only ever adds
time, so the fastest round is the least contaminated. Across the layout
variants of a stage we take the MEAN, and report one standard error of
the resulting ratio.

Why the mean and not the median: layout effects are roughly symmetric,
so the mean of n has standard error sd/sqrt(n), while the median of a
small n is much less efficient. Measured on this project, a median of
five moved 6-9% between runs where the mean moves 2-3%.

Why an error bar at all: a single build gives a figure that repeats to
1% and can be wrong by 12%, because every repetition shares that
build's layout bias. The interval below includes it.
"""
import collections
import os
import sys

dat, width, reps, name = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
order = sys.argv[5:]
base_stage = os.environ.get('BASE_STAGE', 's0-cell')

best = {}                      # (stage, engine) -> min ns
for line in open(dat):
    st, eng, ns = line.rsplit(' ', 2)[0], line.split()[1], int(line.split()[2])
    st = line.split()[0]
    k = (st, eng)
    if k not in best or ns < best[k]:
        best[k] = ns

rows = collections.defaultdict(list)
for (st, _eng), ns in best.items():
    rows[st].append(ns)


def stats(v):
    n = len(v)
    m = sum(v) / float(n)
    if n < 2:
        return m, None
    var = sum((x - m) ** 2 for x in v) / (n - 1)
    return m, (var ** 0.5) / (n ** 0.5)


if base_stage not in rows:
    print("no %s in the data; nothing to normalise against" % base_stage)
    sys.exit(0)
base, base_se = stats(rows[base_stage])
nv = max(len(v) for v in rows.values())

print("%-12s %10s %10s %12s" % ("stage", "ms", "vs cell", "+/- (1 SE)"))
for st in order:
    if st not in rows:
        continue
    m, se = stats(rows[st])
    ratio = m / base
    if se is not None and base_se:
        rel = ((se / m) ** 2 + (base_se / base) ** 2) ** 0.5
        err = "%.3f" % (ratio * rel)
    else:
        err = "1 build"
    print("%-12s %10.2f %10.3f %12s" % (st, m / 1e6, ratio, err))

print()
print("%s, cell width %s: mean over %d layout variant(s), each the"
      % (name, width, nv))
print("minimum of %s rounds; startup subtracted per binary." % reps)
if nv == 1:
    print()
    print("ONE build per stage. The per-build layout bias is larger than")
    print("the run-to-run noise and is invisible here - rebuild with")
    print("LAYOUTS=5 to measure it.")
