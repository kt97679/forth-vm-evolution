# The after-seed-81 batch - to apply first at seed 81's processing (Iteration 567)

process-run.sh checks and applies it. The first two: HANDOFF.md's open item 3, seed 80's two JIT deaths
(results/drafts/jitexec-alignhot-566.md, its section "The cause and the fix"); the last two: the automation audit's
candidates 2 and 3 (results/drafts/automation-audit-567.md).

    git apply results/pending/jitscan-after-seed81.patch
    git apply results/pending/ccflags-after-seed81.patch
    git apply results/pending/design-after-seed81.patch
    git apply results/pending/bar-after-seed81.patch

batch-check (567, on 92b9e8a - the two patches): PASS - both applied to a fresh clone, run-tests PASS (engines-check 107
paths, 102 on master: the variant at both widths, regression c578b55046, two stencil sets), validate 7 of 7 IDENTICAL,
the jail PASS.

**jitscan-after-seed81.patch** (engine/jit.c, lab/evolve/stencil-check.py, engines-check.py, regressions.json, README.md)
- **the cause**: jit_scan reads a stencil at most JIT_SCAN_MAX bytes (160); under -falign-*=64 st_execute's cache-hit
exit ended at byte 164, the copy ended at its first exit and kept the short je to the rest - the first EXECUTE cache
hit on a native target jumped past the copy. At 160, 17 of 84 flag sets cut a stencil, all at 64 (st_execute 16,
st_callx 4, st_ummod 1); the longest stencil is 242 bytes at 64, 146 at 32 (results/drafts/stencil-window-567.py).
**JIT_SCAN_MAX 512**: none cut; builds without 64-byte alignment copy the same bytes. stencil-check.py reads the window
(it read to the last exit and passed all 17); engines-check runs it at -falign-*=64 at 64 and 32 bits, builds "the JIT
with jitexec, aligned to 64", and runs jit-diff.fth on every regression that expresses the JIT (T2's second loop hits
the cache; the corpus does not). **The minimal design is regression c578b55046** (s6 + tag2, jit, jitx, jitexec,
alignhot=3). At 160 it and the variant are wrong on jit-diff and sim16; at 512 they, and seed 52's two regressions,
compute the corpus, jit-diff and sim16 right at 8- and 4-byte cells.

**ccflags-after-seed81.patch** (lab/evolve/evolve.py) - **ccflags() builds what express() expresses**: alignhot under
align1, alignfn or clang no longer appends -falign-*=32/64 (seed 80's two dead designs had align1 and alignfn - their
id without alignhot, their engine with it); alignfn, noinls, gotodup and alignhot no longer reach the families that do
not express them. 9 of the 1,481 records in seeds 76-80's results files build differently (seed 78 6, seed 79 3, each
an unexpressed alignhot); seed 52's two regressions build as their ids say (they carried alignhot=2, built at 32).

At seed 81's processing, if seed 81 has deaths of this class: the control (process-run.sh step 5) measures them right on master
and wrong before the batch - deaths-check names it.

**design-after-seed81.patch** (lab/evolve/design.py, evolve.py, engines-check.py, README.md) - **one design built and
run against s6**: a recorded id (results/ or --db) or a hand-made stage with GENE=VALUE set, each gene said expressed or
not; workloads by name, jit-diff, or files, at 8- or 4-byte cells; right, WRONG (the first differing line) or DIES. The
jit-diff input moved into evolve.py's jit_diff_in(), engines-check's too (the same 32,453 bytes). Tested: the minimal
design right on apps and jit-diff at both widths; with JIT_SCAN_MAX put back to 160, DIES on all three (exit 1);
alignhot under align1 said NOT expressed; a recorded id rebuilt to its own id, its corpus and fib right.

**bar-after-seed81.patch** (lab/evolve/stopping.py, README.md) - **`stopping.py --bar GEN[,GEN]`**: what the next
run must reach by its last generation, from the ledger alone - a prediction's numbers, typed by hand until now. At 120
and 140 it gives prediction 566's bars but one: the smallest 13,910 and 13,875, where 13,849 had been taken by hand from
seed 80's end (results/predictions.md's note). The self-test's 30 checks pass.
