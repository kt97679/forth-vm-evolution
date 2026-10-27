# The before-seed-77 batch - applied before seed 77 starts (Iteration 556)

The owner (556): seed 77 from scratch, 12 hours, with every gene that still has code enabled; the stopping rule's
extremes from every alive design. Applied to master before the run - seed 77's bundle carries it.

    git apply results/applied-before-seed77/unfreeze-before-seed77.patch
    git apply results/applied-before-seed77/stopping-alive-before-seed77.patch

batch-check (556): PASS - run-tests (the stopping rule's self-test among them), validate 7 of 7 IDENTICAL, the jail; applied before seed 77.

**unfreeze-before-seed77.patch** (lab/evolve/evolve.py, GOALS.md) - **every freeze that still has code lifted**: FROZEN
keeps only the retired (tail, kstack, tailpn - their code removed); alignhot, msc, scale and sharedcall free again;
bytehdr, doesfar, thinhdr, varcall, bss and lean free to take 0; the old table kept in a comment. GOALS.md notes the
12-hour series. The pre-flight (results/drafts/unfreeze-preflight-556.md): no new failure - scale inert on cv8 (canon
keeps 0), doesfar and varcall at 0 screened by reach_lethal before any build, the rest right everywhere.

**stopping-alive-before-seed77.patch** (lab/evolve/hv.py, stopping.py; results/stopping-series.md) - **the stopping
rule's extremes from every alive design**, for a series whose method line says so ("extremes": "alive") - seed 77's
does; hv.py's measure() also returns them, its printed line unchanged. Tested: the self-test (17 checks); seed 76's
records as the new series' first run - the fastest 0.1383, the least memory 108 KB, the fastest at 32 bits 0.1714 (the
strict front's), the hypervolume 0.35036 (the true front's, as before).
