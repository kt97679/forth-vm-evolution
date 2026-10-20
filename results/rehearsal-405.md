# The after-seed-62 batch, rehearsed (Iteration 405)

Its patches applied in ORDER.md's order to a scratch clone of master (Iteration 404) and built, then evaluated and evolved
as seed 63 would be: what batch-check's tests do not reach - the genes in mutation and crossover, the 32-bit evaluation of
the new mechanisms on real designs, any new death class. All on this VM, whose GCC is the laptop's, 13.3 (seed 59's
machine.txt); one round a design, so the speeds are rough.

**Targeted** (results/drafts/rehearsal-targeted-405.py): 13 of seed 59's front designs evaluated as a run does, at both
widths.

| designs | case | outcome |
|---|---|---|
| 4 | the JIT with jithelp, jitre and jitret on | alive at both widths |
| 3 | tos designs with bfind, as they were - bfind now built | alive at both |
| 3 | seed 59's dead at 32 bits (bfind, no tos), as they were | alive at both - 32-bit 0.44-0.49 |
| 2 | + tail with clang, without and with preserve_none | alive at both |
| 1 | + tail with GCC (cd9d470f51) | alive at 64 bits; at 32 bits "tail calls not jumps (t2call)" |

**A short run**: `evolve.py --pop 16 --rounds 1 --seed 405 --noevolved --widths 8,4 --require tag2`, stopped with the
session at generation 21 - 330 designs (results/drafts/rehearsal-db-405.py): 322 alive at both widths, 8 refused by the
reach limit (the designs' own, results/fail32-400.md), no 32-bit failure. jitret on in 51 of them, jithelp in 4, a GCC
tail engine in 4 and clang's in 6 - all alive at both widths. bfind and jitre were not reached in so short a run.

**The one failure, and patch 9.** engines-check's tail variants had not been on the two-bit tag. Its shared call path,
t2call, is a static function the other handlers only jump to; at 32-bit x86 GCC gave it a convention of its own, as a
local function - arguments in registers - so its incoming stack was too small for the five arguments the next dispatch
passes on the stack, and its tail call stayed a call: `call *%eax` in H_t2call (results/drafts/t2call-build-405.py). The
same tail call in a function that keeps the declared convention is a jmp, with the design's own flags
(results/drafts/sibcall-i386-405.c). gen-tail.py now makes every handler noipa there - TC_NOIPA, empty for clang and off
i386, so no other engine changes - and engines-check builds tail calls on the two-bit tag at both widths
(results/applied-after-seed62/tailipa-after-seed62.patch). With it seed 59's three designs with a GCC tail engine on the tag live at
both widths, 32-bit 0.813, 0.821 and 0.874 (results/drafts/tailipa-405.py). Without it such designs would have been the
slowest at 32 bits - not every tag2 design takes that path: the short run's four GCC tail engines lived without it.

batch-check, the nine: PASS - 9 patches on a fresh clone of 789364b: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.
