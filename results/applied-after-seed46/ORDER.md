# The after-seed-46 batch - apply in this order (against master after Iteration 241)

Seed 46 runs at Iteration 241's commit without these. Apply when it is processed:

| # | patch | what |
|---|---|---|
| 1 | primfirst-after-seed46.patch | every PRIMITIVE together at the start of the dictionary (kernel.4's second block - the file words, SYSCALL and its slots, the memory words - moved up after RP!; their order, so every token, unchanged), then a marker variable, (PRIMITIVES-END), and PRIMITIVE? ( xt --- flag ): xt below the marker. Every compiler's COMPILE, (the kernel's, cv8, cv8t and their fuse, imm and empty overlays, cpt16, sod16) asks PRIMITIVE? instead of the primitive bit through >NAME - so UTF-8 names compile right without moving the count byte, and the headers go back to the classic [link][count][name]: Iteration 232-234's layout change reversed (names counted strings again; the walk's 6-8% back). **Changes kernel.4: reseed after applying** (242) |

| 2 | nobit7-after-seed46.patch | bit 7 of the count byte freed: nothing sets or reads it (the kernel's HEADER, the byte headers' HEADER8, the cross-compiler, the converter). POSTPONE decides immediacy when it compiles - by FIND's flag; the cross-compiler's target POSTPONE by the target header's flag, found along the name's own thread - so (POSTPONE) only compiles. That fixes POSTPONE of an immediate word with a UTF-8 name, which patch 1 still got wrong (the scan back stopped on a UTF-8 byte and read its bit 6). >NAME leaves the kernel - no compiler asks it - for coreext.4, beside the name-token words, exact by the walk; the tracer and the SPN diagnostic walk for themselves. Images 64-136 bytes smaller than patch 1 alone; dispatches on the smallest design: corpus -0.26%, kernel +0.6% (the cross-compiler's flag walk), parse +0.1%. **Changes kernel.4: reseed after applying** (244) |

| 3 | jittail-after-seed46.patch | the gene jittail (0/1, JIT designs): the translator turns a call to a native word whose next operation is EXIT - or a BRANCH chain to one - into a jump, so tail recursion runs in place. Ackermann 15-18% faster (VM, alternating runs on 28677d13b1), the other selection workloads within noise; +256 engine bytes; off, the engine byte-identical, so every id stays. No kernel change (246) |

| 4 | tailfix-after-seed46.patch | the tail engines compile again: build_tail preprocesses with -DDISPOFF=0. gen-tail.py reads the preprocessed source, where its own '#ifndef DISPOFF' guard (Iteration 237) is already resolved - so the handlers' table was offsets between functions, which C cannot initialize: every tail design of seed 46 died (222, "engine did not compile"). Found processing seed 46 (248) |

    git apply results/applied-after-seed46/primfirst-after-seed46.patch
    git apply results/applied-after-seed46/nobit7-after-seed46.patch
    git apply results/applied-after-seed46/jittail-after-seed46.patch
    git apply results/applied-after-seed46/tailfix-after-seed46.patch
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

Patch 2, tested on patch 1, reseeded (the cell kernel 27,264 bytes, a fixed
point; the 4-byte kernel identical from old and new seed): names-check PASS
(every design and all 14 stages, now also bit 7 clear and POSTPONE of UTF-8
words, immediate and not); run-tests PASS (the tracer's self-test ok); 7 of 7
identical; 128 of 128 alive; the suite on the six designs 14 of 14 each, 0
differ; outbuf-check and readline-check PASS. Both patches apply in order on a
fresh clone of master and, reseeded, reproduce the tested files, the seeds
included.

Patch 3, tested on patches 1-2: run-tests PASS; 7 of 7 identical; the standard
suite on 28677d13b1 and 0af26c8e89 with jittail on, 14 of 14 each, 0 differ;
ackermann right and a 3-million-deep tail recursion running in place (without
the gene, or where a word stays bytecode, the stack overflows as before); built
also without jitx, without jitloop and with jitos; the gene-off engine byte-
identical to before. All three apply in order on a fresh clone of master and,
reseeded, reproduce the tested files, the seeds included.
