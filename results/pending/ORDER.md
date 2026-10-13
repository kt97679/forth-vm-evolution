# The after-seed-47 batch - apply in this order (against master after Iteration 252)

Seed 47 runs at Iteration 248's commit (c0bf29d) without these. Apply when it is
processed:

| # | patch | what |
|---|---|---|
| 1 | faulttrap-after-seed47.patch | a fault handler in every engine without the guard gene: on SIGSEGV it flushes the output (the engine's buffer and fsys 4-5's Forth-side one, as t_flush does), writes "relf: segmentation fault" and exits 70 - as the guard gene's handler does, without its guard pages, own stack and messages. 114 of seed 46's 127 front designs had no handler: `0 @` killed them with a bare SIGSEGV, and those buffering output for a pipe or file lost it. Installed by the runtime's rt_fault (the kernel's struct filled in place; libc builds use sigaction): +128 to +160 engine bytes (3456ac1e5e 7,112 -> 7,272, fe3c9c3940 +128, 3bb2087f9d +128); guard designs unchanged. No kernel change (252) |

| 2 | lean-open-after-seed47.patch | two runtime savings that pay for patch 1: the image's magic checked as one 32-bit compare and a byte (memcmp, its only caller, gone: 42 bytes), and the engine's opens through a three-argument rt_open in both runtimes (the C library's variadic open made the runtime's save every argument register: 95 bytes) - libc builds keep open. Engines with both patches against today: 3456ac1e5e 7,112 -> 7,168 (+56), fe3c9c3940 16,828 -> 16,828 (0), 3bb2087f9d 21,308 -> 21,276 (-32). No kernel change (257) |

| 3 | jitk-after-seed47.patch | the gene jitk (0, 2, 3 cells; JIT designs): the JIT keeps the top K data-stack cells in fixed registers across its copied code - tools/gen-jitk.py writes, per build, a variant of 16 hot data stencils for each cache state 0..K and a canonicaliser per state, and the map the translator plans each operation with; control, calls, loops, exits and branch targets run in state 1. Off, the engine is as before (every id stays). Fastest design's engine +2.3 KB (K=2), +2.8 KB (K=3); on the VM loop -9%, bubble -5%, corpus -4%, fib +16% at K=2 and flat at K=3 - the laptop decides (259) |
| 4 | buildgenes-after-seed47.patch | two build genes: lto (0/1) - the engine and its runtime as one, the JIT's stencils compiled outside it (inside, the JIT stopped translating): -32 to -160 bytes after patch 2; and gotodup (0/1/2) - GCC's max-goto-duplication-insns at its default, 32 or 128: interpreted engines +704 to +800 bytes for a dispatch copied into more handlers, JIT engines unchanged. engines-check grows to 25 paths (260) |

| 5 | compiler-after-seed47.patch | the gene compiler (0 GCC, 1 clang; CV8 designs): every engine compile through clang - -Oz for -Os, only the flags it knows, GCC's own genes (nogcse, nocrossjump, align1, noreorder, peel, ipaclone, tracer, noinls, gotodup, jitos, regpin, lto) not expressed under it; a bcmp in the runtime (clang's memcmp() == 0). **Offered only where clang is installed** - on the laptop: `sudo apt install clang` (clang 18; clang-19 for preserve_none later) before the run, or the gene stays dormant. On the VM: engines larger at the small end, 4% smaller at the fast end at -Oz (262) |
    git apply results/pending/faulttrap-after-seed47.patch
    git apply results/pending/lean-open-after-seed47.patch
    git apply results/pending/jitk-after-seed47.patch
    git apply results/pending/buildgenes-after-seed47.patch
    git apply results/pending/compiler-after-seed47.patch

Tested on master: `0 @` with output to a pipe now exits 70 with the output
kept, on the smallest, the Q-best and the fastest design; run-tests PASS (the
generators: 19 paths); 7 of 7 identical; seed 46's front and the joint front
alive (148 of 148); the suite on 3456ac1e5e, fe3c9c3940, 3bb2087f9d, c05f76468e
14 of 14 each, 0 differ. Applies on a fresh clone.

Patch 2, tested on patch 1: run-tests PASS (19 generator paths; the 32-bit
stages link the i386 runtime's rt_open); 7 of 7 identical; seed 46's front and
the joint front alive, 148 of 148; the suite on six front designs 14 of 14
each, 0 differ; `0 @` still exits 70 with the output kept. Both apply in order
on a fresh clone and reproduce the tested files.

Patches 3 and 4, tested on 1-2: run-tests PASS (the generators: 21 paths with
jitk, 25 with lto and gotodup); 7 of 7 identical; the standard suite on three
JIT designs (3bb2087f9d, fe3c9c3940, cfee5345ab) with jitk at 2 and at 3, 14 of
14 each, 0 differ; the corpus right with lto on the smallest and the fastest,
the JIT translating under it; seed 46's front and the joint front alive with
all four, 148 of 148. The four apply in order on a fresh clone of master and
reproduce the tested files.

Patch 5, tested on 1-4 with clang 18 installed: run-tests PASS (the generators:
29 paths - clang plain, with the JIT, the tail engine, -Oz); 7 of 7; the suite
on 3456ac1e5e and 3bb2087f9d built with clang, 14 of 14 each, 0 differ. The five
apply in order on a fresh clone and reproduce the tested files.
