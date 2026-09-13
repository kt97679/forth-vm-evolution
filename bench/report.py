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

# Each line: stage engine wall_ns cpu_ns   (cpu 0 when unmeasured)
wall, cpu, samples = {}, {}, collections.defaultdict(list)
for line in open(dat):
    f = line.split()
    st, eng, w, c = f[0], f[1], int(f[2]), int(f[3]) if len(f) > 3 else 0
    k = (st, eng)
    if k not in wall or w < wall[k]:
        wall[k] = w
    if c and (k not in cpu or c < cpu[k]):
        cpu[k] = c
    samples[k].append((w, c))

USE_CPU = len(cpu) == len(wall) and all(v > 0 for v in cpu.values())
best = cpu if USE_CPU else wall

rows = collections.defaultdict(list)
for (st, _eng), ns in best.items():
    rows[st].append(ns)


def cv(vals):
    vals = [v for v in vals if v]
    if len(vals) < 2:
        return None
    m = sum(vals) / float(len(vals))
    sd = (sum((x - m) ** 2 for x in vals) / (len(vals) - 1)) ** 0.5
    return 100.0 * sd / m


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
print("minimum of %s rounds of %s; startup subtracted per binary."
      % (reps, "CPU TIME" if USE_CPU else "wall clock"))

# Which clock was steadier here, averaged over binaries. On a quiet
# machine the two are alike; on a loaded one CPU time should win,
# because it does not count the time a process spends descheduled.
cvs = [(cv([w for w, _ in v]), cv([c for _, c in v])) for v in samples.values()]
cvs = [(a, b) for a, b in cvs if a is not None and b is not None]
if cvs:
    aw = sum(a for a, _ in cvs) / len(cvs)
    ac = sum(b for _, b in cvs) / len(cvs)
    print("round-to-round spread per binary: wall %.1f%%, cpu %.1f%%."
          % (aw, ac))
if nv == 1:
    print()
    print("ONE build per stage. The per-build layout bias is larger than")
    print("the run-to-run noise and is invisible here - rebuild with")
    print("LAYOUTS=5 to measure it.")
