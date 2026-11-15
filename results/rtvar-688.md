# The gene rtvar - a data word's @ and ! as one operation at run time (Iterations 687-688; step 3)

forth/cv8-fuse-var.4 (the byte header): a call to a word whose code is DOVAR (a VARIABLE, a CREATE) followed straight
by @ or ! becomes vf or vs and the slot of its parameter field - the operations the converter lays for the kernel's
own variables (spec var). Never across a branch target: LAST-OP left at a mark no other rule matches, cleared by every
target. tools/layout.py writes VAR-OPS (vf, vs, @, !, VARSLOT; zeros: the fusion off); lab/evolve/evolve.py's gene
rtvar and its -var dumps; it needs the run-time fusers, spec var and - since 688 - varslot.

## Correct (lab/evolve/rtvar-check.py, portable-knee with varslot on): PASS

Alive with rtvar 0 and 1; `: T1 V @ ;` compiles to vf, its slot and EXIT (0x63 0x28 0x70 0x01) where it was a call, @
and EXIT; `5 V !` to LIT8 5, vs and the slot; the values the same with 0 and 1, `IF V ELSE W THEN @` (a branch target
between the call and the @) and a loop over a variable among them; run-tests PASS.

## What it buys (portable-knee)

Each program's benchmark alone (genapps.py's drivers, the full run less the load; medians of 7, CPU 1), rtvar 0 -> 1,
varslot off (each program alone lies within 64 KB of the image, so every slot reaches):

| program | benchmark | ratio |
|---|---:|---:|
| sim16 | 815.8 -> 772.9 ms | 0.947 |
| gc16 | 598.3 -> 586.2 ms | 0.980 |
| scan | 591.2 -> 433.2 ms | 0.733 |
| evo | 454.1 -> 435.1 ms | 0.958 |
| shellmix | 166.4 -> 124.9 ms | 0.750 |

The same outputs; the loads (about 1.5 ms each) within their noise.

**The apps workload needs varslot.** Its five programs load into one process: they start 10, 46, 388, 441 and 451 KB
from the image (gc16's heap pushes scan past 388 KB). Without varslot a slot is 16 bits from the image - 64 KB - so
the fusion missed scan, evo and shellmix, and the workload ran 1.038 (36.2 -> 37.6 ms: the extra COMPILE,8 layer on
every word, about 6 % of its compile time, and little fused). With varslot's 23-bit slots (8 MB) it ran **0.902**
(37.5 -> 33.8 ms, medians of 15); rtvar-check's measure() 0.960. A real program - relfsh is 46,096 tokens - would
miss the same way with 16-bit slots: the gene needs varslot (688), as relf's 3-byte slots reach 4 MB.

Bytes: the five apps' code 8,365 -> 8,342 (the knee, varslot on) - a slot beyond 32 KB is 3 bytes, as relf found:
dispatches, not bytes.

## The two-bit tag (Iteration 689)

The same overlay serves both families (cv8t.4's OP, is C, as cv8.4's; DOVAR-OP is rewritten to the design's code):
the -var dumps for both, VAR-OPS remapped to the tag's one-byte codes (all four or none), vf and vs pinned to one
byte. On fastest-x86-64 (the tag, the JIT, jitvar) the values were right and the five apps' code 9,988 -> 9,886 B -
**but the apps workload ran 1.999**: the JIT refused the run-time words holding vf (T1's JIT header 0 where without
rtvar it held its native offset 0x2C0), so they ran interpreted. The JIT's op table has vf and vs (vm-jit-ops.h's [99]
and [100], jitvar) and translates the kernel's own; why it refuses a run-time word's is not found yet - next, with a
JITLOG build of that engine. Until then rtvar needs no JIT under the tag (evolve.py's rtvar_can): the byte header's
designs and the tag's interpreted ones.

Next: the JIT's refusal; then the other step-3 genes (constants as literals by relf's test, inlining at 3/6, the JIT
header, DOES> @ as VAR@, the DODOES stencil); the compile layer's cost weighed on the kernel and corpus workloads by
the search.
