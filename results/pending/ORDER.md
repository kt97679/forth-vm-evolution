# The after-seed-46 batch - apply in this order (against master after Iteration 241)

Seed 46 runs at Iteration 241's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | primfirst-after-seed46.patch | every PRIMITIVE together at the start of the dictionary (kernel.4's second block - the file words, SYSCALL and its slots, the memory words - moved up after RP!; their order, so every token, unchanged), then a marker variable, (PRIMITIVES-END), and PRIMITIVE? ( xt --- flag ): xt below the marker. Every compiler's COMPILE, (the kernel's, cv8, cv8t and their fuse, imm and empty overlays, cpt16, sod16) asks PRIMITIVE? instead of the primitive bit through >NAME - so UTF-8 names compile right without moving the count byte, and the headers go back to the classic [link][count][name]: Iteration 232-234's layout change reversed (names counted strings again; the walk's 6-8% back). **Changes kernel.4: reseed after applying** (242) |

    git apply results/pending/primfirst-after-seed46.patch
    sh tools/reseed.sh

Tested on master and the patch, reseeded (fixed point; the 4-byte kernel
identical from old and new seed): lab/evolve/names-check.py PASS - every
evolved design given and all 14 hand-made stages (s0-s8, p4, p8) right;
dispatches on the smallest of all runs (add5ec8937) back to seed 45's code -
corpus 58.90M (seed 45's code 58.95M, master 63.43M), kernel 8.48M (8.47M,
8.95M), parse 148.96M (148.96M, 160.24M); run-tests PASS; 7 of 7 identical;
seed 45's front and the joint front alive (128 of 128); the standard suite on
six designs (tag2, JIT, multi-state, tail, fsys 2 and 3) 14 of 14 each, 0
differ; outbuf-check and readline-check PASS. The patch applies on a fresh
clone and, reseeded, reproduces the tested files, the seeds included.
