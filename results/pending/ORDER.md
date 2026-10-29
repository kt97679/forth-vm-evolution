# The after-seed-81 batch - to apply first at seed 81's processing (Iteration 567)

process-run.sh checks and applies it. HANDOFF.md's open item 3: seed 80's two JIT deaths
(results/drafts/jitexec-alignhot-566.md, its section "The cause and the fix").

    git apply results/pending/jitscan-after-seed81.patch
    git apply results/pending/ccflags-after-seed81.patch

batch-check (567, on BATCHCOMMIT - the two patches): BATCHRESULT

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
