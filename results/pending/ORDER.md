# The after-seed-47 batch - apply in this order (against master after Iteration 252)

Seed 47 runs at Iteration 248's commit (c0bf29d) without these. Apply when it is
processed:

| # | patch | what |
|---|---|---|
| 1 | faulttrap-after-seed47.patch | a fault handler in every engine without the guard gene: on SIGSEGV it flushes the output (the engine's buffer and fsys 4-5's Forth-side one, as t_flush does), writes "relf: segmentation fault" and exits 70 - as the guard gene's handler does, without its guard pages, own stack and messages. 114 of seed 46's 127 front designs had no handler: `0 @` killed them with a bare SIGSEGV, and those buffering output for a pipe or file lost it. Installed by the runtime's rt_fault (the kernel's struct filled in place; libc builds use sigaction): +128 to +160 engine bytes (3456ac1e5e 7,112 -> 7,272, fe3c9c3940 +128, 3bb2087f9d +128); guard designs unchanged. No kernel change (252) |

| 2 | lean-open-after-seed47.patch | two runtime savings that pay for patch 1: the image's magic checked as one 32-bit compare and a byte (memcmp, its only caller, gone: 42 bytes), and the engine's opens through a three-argument rt_open in both runtimes (the C library's variadic open made the runtime's save every argument register: 95 bytes) - libc builds keep open. Engines with both patches against today: 3456ac1e5e 7,112 -> 7,168 (+56), fe3c9c3940 16,828 -> 16,828 (0), 3bb2087f9d 21,308 -> 21,276 (-32). No kernel change (257) |

    git apply results/pending/faulttrap-after-seed47.patch
    git apply results/pending/lean-open-after-seed47.patch

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
