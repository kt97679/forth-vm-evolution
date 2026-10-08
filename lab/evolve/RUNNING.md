# Running the evolution on a machine that is not quiet

## In one command (Iteration 15)

In the clone, with the new bundle in ~/Downloads:

    sh lab/evolve/next-run.sh

With no argument it does what the bundle's `lab/evolve/NEXT-RUN` says - a
seed, `compare`, `experiment TOOL ARGS` (a tracked tool in lab/evolve/,
given every database; Iteration 23) or `none` - so the same command follows
every pull; an argument (`4`, `compare`) overrides it.

`lab/evolve/next-run.sh` does all of this page: it pulls the newest
`forth-vm-evolution*.bundle` from ~/Downloads into the clone it is in
(fast-forward only; REPO= to choose another; tracked files the benchmark
suite rewrote under results/ are kept as a git stash and sent back in the
pack, any other change stops it), then carries on as the copy it pulled - so it updates itself, and only bundles need
downloading. It moves the previous run's
records to runs/archived-TIME/ in the clone (~/forth-vm-evolution-runs before Iteration 84) (never deletes them:
every untracked file at the top but RESULTS.md, every file in
build/evolve/ - each seed's database and reports - and build/bench-laptop/
and build/results/; MANIFEST.txt lists them), removes the rest of build/
and builds again, runs the tests, `--validate` and the jail
test, then the run (seed as given; 32 x 40, 3 rounds), `--remeasure 6`, and
packs what to send back into runs/forth-vm-evolution-
seedN-....tar.gz. After the pull it goes on in the background; the last
line of its log names the pack. Run it again with the same seed after an
interruption and it resumes; a new commit or seed starts afresh.

    sh lab/evolve/next-run.sh compare

measures every run's front again in one session - this clone's database
and every archived one, each design rebuilt with the current commit, all
timed round-robin against hand-made s6, s6 itself as the calibration
(`lab/evolve/compare-fronts.py`) - and packs the table. It archives and
removes nothing. Runs measured on different days cannot be ranked by a
few per cent: their calibrations differ (Iteration 20). The
sections below are what it does, by hand.


## Safety: engines are jailed (Iteration 10)

A design is generated, so a broken one runs arbitrary code - and the
engines' primitives include FORK. In the third run on the Ryzen, wild
designs forked without bound and froze the laptop; the CPU limit and the
process-group kill came too late, since a fork bomb fills the machine in
milliseconds. Every engine the evolver runs is now jailed: no new
processes at all (no workload forks), at most 1 GB of address space,
64 MB files, 64 open files, no core dumps (`_contain` in evolve.py;
`CPUTIME_JAIL` in tools/cputime.c). The process limit does not bind
root, so the evolver refuses to run as root.

A second layer: the designs that go wild most - two-byte-only call or
DOES> forms at scale 0, whose 16 KB reach the kernel workload always
outgrows (345 of 345 died) - are not run at all (`reach_lethal`). The
third run's fork bomb was one: 8cfd49f24c, which tried to fork 8,181
times in its gate run (`lab/evolve/forklog.c` counted them).

Before a run, after the rebuild, check it on this machine - it runs a
real fork bomb, but only after one jailed fork has been refused:

    python3 lab/evolve/test-jail.py      # must end: PASS

## What is measured

- **CPU time of the engine process** - user plus system time, from
  `getrusage` of the child (`tools/cputime.c`) - not wall time. Time the
  machine spends on other processes does not count against a design.
- **Paired with a reference.** Every timed run of a design is paired with
  a run of hand-made s6 on the same workload, back to back, alternating
  which goes first; each takes its median over the rounds (Iteration 25 -
  until then its best, which reported luck: see below). A
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
fluctuations remain as noise, which the median over rounds reduces. The
minimum reduced it too, and was wrong on fib: on the laptop a rare fib run
is 20-38% faster - 0.4-2.3% of runs for some designs, with address
randomisation on or off, at no stack offset in particular (Iterations 25,
27) - and the best of the rounds reported that draw, a different one each
session; two sessions ranked the same designs up to
28% apart. The median of the same runs agreed within 3.6% between halves
of a session and 2.1% between CPUs
(`results/run-spread-amd-ryzen-7-pro-8840hs.md`).

## Before the run

Needs Linux on x86-64, `gcc`, `python3`, `objdump` (binutils) and `taskset`
(util-linux).

    git clone forth-vm-evolution-claude-iterN-YYYYMMDD-HHMMSS.bundle forth-vm-evolution
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

A build step that fails is not tried again - a retry added for
"transient" failures was removed once their real cause was found (the
register in GOALS.md); the design dies, and the death records why - the
converter's or the compiler's last error line - in `build/evolve/db.jsonl`.

## Then: what each gene is worth

    python3 lab/evolve/evolve.py --knockout ID,ID,...

For each design (default: the front, re-measured where `--remeasure` was
run), every gene that differs from hand-made s6 is set back to s6's
value, one at a time, and the design measured again: what that gene is
worth in that design. Progress and the report go to the screen, and the
report to `build/evolve/knockout.md` - machine, commit, a calibration (s6 against itself, the
design itself) and one table per design. About 7 s per variant at the
default 6 rounds, so a few minutes per design. `--db FILE` reads a
database kept aside. Run it when no evolution is running: both pin a core
and would measure each other.

## What to send back

`build/evolve/report.md`, `build/evolve/db.jsonl`, `build/evolve/remeasure.json`,
`evolve.log`, and the output of `lscpu`.

## The benchmark suite

`tools/bench-laptop.sh`, which measures the hand-made stages for
`results/`, also defaults to CPU time now; `BENCH_METRIC=cycles` makes
cycles the metric. It asks for sudo to make the hardware counters
readable - they add cycle and instruction columns; `NO_COUNTERS=1`
skips that.

## A uniform sample of the space

Before trusting the front (prompts/02, step 5) - designs drawn at random,
not bred:

    python3 lab/evolve/evolve.py --sample 128 --rounds 3 > build/evolve/sample.md

Its records go to `build/evolve/sample-seed1-POOL.jsonl` - POOL a
fingerprint of the gene pool, since a new gene changes the draws - never
the run's database; run again, it resumes. `sample.md` has how many live, the
spread of speed and size, the run's best placed in it, and every death
by cause. On the VM, 32 designs took about three minutes.

## A run for a night (Iteration 93)

    sh lab/evolve/next-run.sh seed 25 tag2 night then experiment compare-fronts.py --rounds 10 --cpus 2,8

`night` after the seed (and tag2) runs a population of 96 for 80
generations instead of 32 for 40: about 7,800 designs, ~3 hours at seed 23's
pace (1.4 s a design), then the re-measure and the comparison - a night with
room to spare. Why the population first: under three objectives the front
outgrew it - seeds 21-23 ended with 38-46 designs on the front and 32 in the
population, so part of the front was cut from breeding every generation;
and a third of each final front was still found in the last 10 of 40
generations, while the best speed and the smallest total mostly settled by
generation 20-30. Other sizes: `POP=... GENS=...` before the command, as
always. A night run counts as one run for the stopping rule; being six
times larger, a small one says more about convergence than a small one of
the usual size. Its database is larger too (~16 MB, ~3 MB packed); the
front's genomes travel in its report (Iteration 87).

Seed 26, the first night run (Iteration 97): 29 of the 30 designs on the
front of all runs against four short runs, its front born mostly after
generation 40 and the best speed still moving at generation 80. A night
has room for twice that - 96 x 160, ~7 hours - by size alone:

    POP=96 GENS=160 sh lab/evolve/next-run.sh seed 27 tag2 then experiment compare-fronts.py --rounds 10 --cpus 2,8

## Four cores, and runs of hours (Iteration 99)

`JOBS` workers (default 4, the owner's allowance) evaluate a generation's
designs side by side, each pinned with its builds to its own physical core
(evolve.py free_cores: the least busy, hyperthread siblings counted
together, core 0 last; BENCH_CPUS=2,4,6,10 to choose) and pairing every
timed run with hand-made s6 on that core, in its own copy of the
reference's work directory. A generation's children are all made before any
is evaluated, so the run decides as it did serially, and a resumed run
replays (checked: generation 0 the same designs in the same order with one
worker and two; a rerun on its own database evaluated nothing new).

    sh lab/evolve/next-run.sh seed 28 tag2 12h then experiment compare-fronts.py --rounds 10 --cpus 2,8

`12h` (any number of hours) runs a population of 256 for as many
generations as fit before a deadline 50 minutes short of the end (evolve.py
--until), leaving the re-measure, the report and the comparison inside the
hours - ~90,000 designs at 4 cores, a database of ~180 MB (~30-40 MB
packed). Resumed after an interruption, the deadline counts from the new
start. The front over all designs is found without comparing every pair
(evolve.py first_front: identical to the old one on seeds 25-27's
databases, 0.07 s against 130 s on 7,267 designs).
