# Running the evolution on a machine that is not quiet

## What is measured

- **CPU time of the engine process** - user plus system time, from
  `getrusage` of the child (`tools/cputime.c`) - not wall time. Time the
  machine spends on other processes does not count against a design.
- **Paired with a reference.** Every timed run of a design is paired with
  a run of hand-made s6 on the same workload, back to back, alternating
  which goes first; each takes its best (minimum) over the rounds. A
  design's speed is the geometric mean, over the four selection
  workloads, of its CPU time divided by s6's: **1.0 is as fast as s6, 0.83
  is 17% less CPU time.** Two runs seconds apart see the same machine, so
  drift over a run of hours - background load, clock speed - cancels.
  Measured against itself, s6 comes out within 1% of 1.0.
- **Correctness limits are CPU time too**: 5 s for the corpus, 10 s for the
  kernel workload, with a wall-clock backstop of minutes for a design that
  blocks. A correct design waiting its turn on a busy machine is not
  killed; one that loops still is.

What CPU time does not remove: the clock speed (a hot, busy laptop turbos
lower - the pairing takes out slow changes), and contention for what a
core shares - its hyperthread sibling, the caches, memory bandwidth. Fast
fluctuations remain as noise, which the minimum over rounds reduces.

## Before the run

Needs Linux on x86-64, `gcc`, `python3`, `objdump` (binutils) and `taskset`
(util-linux).

    git clone forth-vm-evolution.bundle forth-vm-evolution
    cd forth-vm-evolution
    LAYOUTS=1 bash tools/build-stages.sh      # about half a minute
    bash tools/run-tests.sh                   # must end: PASS - no regressions
    python3 lab/evolve/evolve.py --validate   # seven stages, all IDENTICAL

**After every `git pull`, build again** - the evolver builds each design
from the engine source and dumps that `build/` holds, and a `build/` older
than the sources makes the newest genes die for reasons that are not
theirs. The evolver checks this at start-up and stops with the command
if `build/` is older than its sources.

Plug the laptop in. If you can, choose a performance power profile
(`powerprofilesctl set performance`, or your desktop's power settings);
it is not required.

## The core

Every timed run is pinned to one core. By default the evolver picks the
core that, together with its hyperthread sibling, was least busy over one
second at start-up, and prints it: `pinned to cpu N (...)`. If you know
where your background work runs, choose yourself: `BENCH_CPU=N`. Prefer
a core whose sibling is idle as well - `lscpu -e` shows which logical CPUs
share a CORE.

## A trial, then the run

A short trial first, to see the time per design on your machine:

    rm -f build/evolve/db.jsonl
    python3 lab/evolve/evolve.py --pop 8 --gens 2 --rounds 3 --seed 1

Each line it prints is one new design: its id, speed and size, and how it
was made. Then the run:

    rm -f build/evolve/db.jsonl
    nohup python3 lab/evolve/evolve.py --pop 32 --gens 40 --rounds 3 --seed 1 > evolve.log 2>&1 &

About 1,300 designs. On the development VM a design took 2.4 s on average
(build, strict check, timing) - about an hour; designs with tail calls or
multi-state caching build longer. The trial's time per design tells you
yours.
`tail -f evolve.log` follows it. The report, `build/evolve/report.md`, is
written at the end; `python3 lab/evolve/evolve.py --report` writes it from
what is done so far, at any time.

**Interrupted?** Run the same command again, with the same seed and
without deleting `build/evolve/db.jsonl`. Every design already evaluated
comes from the database, so the run replays quickly to where it stopped
and goes on. Do not change the measurement in between - `BENCH_CPU`,
`EVOLVE_METRIC`, `--rounds` - or the old and new numbers mix; for that,
start fresh.

`EVOLVE_METRIC=cycles` measures CPU cycles instead of CPU time, from the
hardware counters (`kernel.perf_event_paranoid` at most 2); still paired
with s6 the same way.

## After the run: measure the front again

    python3 lab/evolve/evolve.py --remeasure 6

The front was chosen as the best of many noisy measurements, so its
designs were partly chosen for luck - in the VM rehearsal they came out
3-6% slower when measured again. This measures each front design again
with six rounds and adds a "re-measured" column to the report: quote
those numbers.

A build step that fails is tried once more before the design dies, and
a death now records why - the converter's or the compiler's last error
line - in `build/evolve/db.jsonl`.

## What to send back

`build/evolve/report.md`, `build/evolve/db.jsonl`, `build/evolve/remeasure.json`,
`evolve.log`, and the output of `lscpu`.

## The benchmark suite

`tools/bench-laptop.sh`, which measures the hand-made stages for
`results/`, also defaults to CPU time now; `BENCH_METRIC=cycles` makes
cycles the metric. It asks for sudo to make the hardware counters
readable - they add cycle and instruction columns; `NO_COUNTERS=1`
skips that.
