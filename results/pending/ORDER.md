# The after-seed-96 batch - to apply at chain A's processing, before chain B's lists (Iteration 706)

Seed 96 is processed (704) and no seed run is planned: process-followup.sh applies no batch, so the chat processing chain
A (the new roles' screen - results/drafts/new-roles-plan-705.md) applies it by hand on master, first: `sh
tools/batch-check.sh` (PASS), the two lines below, a commit, then process-records' move by hand (`git mv results/pending
results/applied-after-seed96`, the citations followed - HANDOFF-REFERENCE.md, step 6). Chain A's x86 readings are not
touched by it (x86 engines byte-identical); chain B and the export measure and ship the ARMv7 engines it builds.

    git apply results/pending/arm2at-after-seed96.patch
    git apply results/pending/armcheck-after-seed96.patch

batch-check (706, on 9d115fa - 2 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**arm2at-after-seed96.patch** (engine/vm-lab.c, tools/gen-msc.py, tools/gen-tos.py) - 2@ and 2! read and write the cell
pair through a one-byte-aligned type (CELLU, `aligned(1), may_alias`), in the engine's handlers and in the two stack
rewrites that restate them (gen-tos.py for tos=1, gen-msc.py for msc). Why: at tos=1 the two cell loads are adjacent with
nothing between, and GCC joins them into ARMv7's LDRD (2! into STRD), which traps on an address not word aligned - the
corpus's `HERE 1 ALLOT  HERE 1 ,  ... 1ST 2@` (Forth 2012 leaves an unaligned `,` ambiguous; the Hayes test does it).
Linux on the Tegra fixes the access up, so its readings stood (88 such designs measured in the final check); qemu-user
does not, nor a kernel set to signal - the ARMv7 pre-flight's 4 false deaths (results/drafts/arm-preflight-705.md).
Tested (results/drafts/arm2at-706.md): x86 - 24 designs expressing 2@ (tos 0 and 1, GCC and clang, the JIT and not)
built by master and by the patched tree at both widths, every engine and image byte-identical (48 of 48;
results/drafts/arm2at-bytes-706.py); ARMv7 under qemu-arm - the GCC builds (arm-linux-gnueabihf-gcc 13) of the 4 that
died, of 7fb40ff7ba and 58479dda0a (dead before, measured on the Tegra) and 2 more, 8 of 8 alive and identical on fib and
apps, the engines 0-4 bytes larger; 14 more spread by speed with the hand-made stages, 14 of 14 alive; clang's 10 of 10.

**armcheck-after-seed96.patch** (tools/arm-cross-check.py) - fib and apps compared as evolve.py compares them (run()'s
OUT_LAST): the "Redefining: X" lines dropped first. Why: s0-cell DIFFERED on apps by two such warnings and nothing else -
a cell design's kernel has no LIT, or CALL, for shellmix (and sim16) to redefine, which evolve.py already allows for.
Tested: s0-cell IDENTICAL after (DIFFER before, on master too), d3496fcc6c beside it the same.
