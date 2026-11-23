# The data layout's step 2 - queued until the series ends (Iteration 738)

The owner (737): "proceed with step 2" - prototyped and queued, not applied: it changes the memory reading (the
record's rss, MINFLT x 4 KB), so a seed measured after it would not compare with seeds 97 and before. Apply it when
the series ends (stopping.py's stop), before the final build (results/drafts/ship-rehearsal-737.sh's order), and
before relf's handoff. Check it on master as it stands: `env PENDING=results/queued-layout2 RECORD=1 sh
tools/batch-check.sh`. Then, from the repository's top:

    git apply results/queued-layout2/data-layout2-after-series.patch

batch-check (738, on e198c8b3 with this batch committed - 1 patch): PASS - run-tests PASS (the generators: 118 paths), validate 7 of 7
IDENTICAL, the jail PASS.

What it does (results/drafts/data-layout2-738.txt): engine/vm-lab.c's stacks' chunk (STACKSEP) gets STK_PAD = 1024
bytes more return stack, so it ends 1 KB into a page; engine/data-layout.ld puts it first in .bss.hot, the small
variables straight after it - the return stack's top and the variables a run writes share a page. The floors and the
guard pages stay page-aligned; without STACKSEP STK_PAD is 0. lab/evolve/data-layout-check.py excepts stackmem in
.bss.hot.

Measured on the ten roles: outputs the same, x86 engines byte for byte the same size, the record's memory 0-8 KB less
(smallest 104 -> 96, small-jit 228 -> 220, best-all-round 300 -> 292), about a fault fewer a workload over 31 runs;
every stack trap the same in both trees (x86, and the three clang ARM designs under qemu-arm). The cost: +4 B on
every 32-bit ARM engine (the stacks' end is no longer one ARM immediate) - a constant, no ranking moves.

**When applying:** every role's memory reading changes - re-measure the shipped roles (the record's rss) rather than
carrying the old numbers into designs/ or relf's handoff; the Tegra may check ARM's faults (qemu cannot) - if no
fault fewer there, `#define STK_PAD 0` under `__arm__` takes the 4 bytes back.
