# The after-seed-72 batch - applied at seed 72's processing (Iteration 517)

Prepared while seed 72 runs; master stays what seed 72's bundle tests.

    git apply results/applied-after-seed72/jitexec-table-after-seed72.patch
    git apply results/applied-after-seed72/memory-without-apps-after-seed72.patch

**jitexec-table-after-seed72.patch** (tools/layout.py) - **why no search kept jitexec**: the converter placed jitexec's
three extra JIT-table rows after the highest name it knew - T2_JIT, the JIT's own opcode at 0xFE00 - so jit_ops ran to
65,029 rows: **585 KB in every jitexec engine** (seed 71's fastest: 36,708 bytes, 623,252 with jitexec). Now they follow
the real operations: 39,460 bytes with jitexec - 2,752 for its gain (applications -13.7% of instructions, the seven
-1.7%; results/drafts/jit-genes-517.md). engines-check PASS in a clone with it, 101 paths.

**memory-without-apps-after-seed72.patch** (520; lab/evolve/evolve.py) - **found at seed 72's processing**: a design's
memory is the most any selection workload touched, and since seed 71 that is always the applications - their own data,
gc16's 320 KB of cells: every design 460-500 KB, where the six old workloads give 108-136. The memory objective measured
the programs, not the machine (and in seed 71 the cpt16 designs that failed early looked small too). Now the most of the
others - as before seed 71; the record keeps every workload's. A side effect of 495, undone.

**At seed 72's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
