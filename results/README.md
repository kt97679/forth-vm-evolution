# Published measurement runs

`RESULTS.md` in the repository root is generated and untracked - it
differs on every machine and would conflict on every pull. Files here
are deliberate snapshots, each naming the machine it came from, so two
runs can be compared without either being mistaken for the canonical
one.

    tools/collect-results.sh run
    tools/collect-results.sh report --save results/<machine>.md

Ratios travel between machines; absolute milliseconds do not. Each file
carries the host block the sweep recorded, so it says for itself what it
ran on.

## The Ryzen 8840HS, twice

`amd-ryzen-8840hs.md` is the September snapshot: CPU time, five layout
builds, three builds from a clean tree. `amd-ryzen-7-pro-8840hs-x86_64-run1.md`
and `-run2.md` are the two sweeps of one build on 29 September, measured
in CPU CYCLES with the machine in use - load 1.7, powersave governor -
by `tools/bench-laptop.sh`; `spn-amd-ryzen-7-pro-8840hs-x86_64.md` is the
same run's SPN measurements: start-up, end to end, memory, in CPU time
and in cycles.

The two snapshots agree. For s1-s6 the ratios differ by a median of
1.1%, the largest by 7.2% (fib, the layout-sensitive one), none by more
than about one combined standard error - a busy machine measured in
cycles reproduced a run in CPU time. The SPN report's sections "Does CPU
time agree with cycles?" and "Clock, and time outside user space" were
rewritten from its raw minima by `tools/clockfit.py` after the run: the
first explanation blamed the clock, and the clock was 4.84-4.94 GHz for
every system. The difference was the kernel's part of each run.
