# The after-seed-68 batch - apply in this order (deferred at Iteration 464 to seed 69's processing)

**Rebased again (476)** onto jitexec - a clean three-way merge this time; the three apply in order to 8c2731a.
**Rebased (475)** onto this session's JIT work (jitmul, jitdoes, UM/MOD's throw path): two conflicts in engine/jit.c,
resolved - the holes a cell wide (JIT_HOLEW) and the throw hole kept, in the scan and the patching; the three patches
apply in order to cc7a93e. Batch-check again at seed 69's processing, as below.

**Deferred (464)**: seed 69 is the real islands trial (islands never ran before - HANDOFF), and the 32-bit JIT changes
what "widths" selects for; one change at a time, so this batch waits for seed 69's processing. Batch-check again then.

The owner (460-461): "yes, please proceed" - the JIT at 32-bit x86 made real (results/drafts/jit-i386-460.md, steps
1-4). After seed 68, so seed 68 is not mixed with it.

| # | patch | what it does |
|---|---|---|
| 1 | jit-i386-engine-after-seed68.patch | **The JIT builds at 32-bit x86** (engine/: spn-abi.h, spn-stencils.c, spn-markers.c, jit.c, vm-lab.c) - i386 takes ARM's convention (the state one 64-bit value; regparm(2): eax and edx in and out), 4-byte holes (mov $imm32), endbr32; and **a variable's address aligned to the cell**, not to 8 bytes - 4 bytes off at 32 bits before, unchanged at 64. The prototype of Iteration 460, as is. |
| 2 | jit-i386-lab-after-seed68.patch | **The 32-bit measurements keep the JIT**: eval32() builds the design as it is (until now "its JIT off"), jitk dropped at 32 bits by the build (w32(): gen-jitk.py's stencils name x86-64's registers); xcheck.py's prebuilt 32-bit sample (dream) takes JIT designs - a host building itself at 4-byte cells (the Tegra, ARM) still takes none; engines-check builds the JIT's variants at 32 bits too (69 paths to 81). |
| 3 | stencil-check-after-seed68.patch | **The stencils checked safe to copy** (Iteration 463; the owner: proceed with the second pass's first idea - Gforth's relocatability rule, Ertl and Paysan 2025). lab/evolve/stencil-check.py compiles engine/spn-stencils.c alone and reads it with objdump: in the part the JIT copies, any relocation to anything but a marker (a call GCC put in, a .rodata constant) or any branch past the copied part (a cold block after the last jump) fails it. engines-check runs it at 64 and 32 bits. And engine/jit.c refuses at run time a stencil whose 32-bit call or jump leaves it for the engine image (E8, E9, 0F 8x; FF 15 / FF 25 on x86-64) - slower, never wrong. |

    git apply results/pending/jit-i386-engine-after-seed68.patch
    git apply results/pending/jit-i386-lab-after-seed68.patch
    git apply results/pending/stencil-check-after-seed68.patch

After patch 3: list lab/evolve/stencil-check.py among lab/evolve/README.md's tools (the handoff check asks for it).

**A break to note**: from seed 69, the "fastest at 32 bits" column and speed32 measure JIT designs with their JIT -
about half the time they took before (below); comparisons across the break at 32 bits are not like for like.

## How it was tested

In a clone of master (b678e55) with both, its stages built: run-tests PASS (engines-check 81 paths, each built and
its corpus right - the JIT's variants at 32 bits among them), validate 7 of 7 IDENTICAL. Seed 67's front, its three
fastest JIT designs and two from its middle, timed at 32 bits against the 32-bit s6 (one core here - indicative):

| design | 64-bit speed | jitk | 32 bits, JIT off | 32 bits, with the JIT | with / off |
|---|---|---|---|---|---|
| 3e6253f682 | 0.125 | 3 | 0.535 | 0.242 | 0.451 |
| 99fbe5da86 | 0.128 | 3 | 0.469 | 0.245 | 0.523 |
| 4d72023100 | 0.131 | 3 | 0.542 | 0.240 | 0.442 |
| 04c2fda2fa | 0.157 | 3 | 0.583 | 0.256 | 0.438 |
| c34219918d | 0.157 | - | 0.713 | 0.249 | 0.350 |

1.9 to 2.9 times faster at 32 bits, jitk not yet ported - about the JIT's gain at 64 bits. One thing this machine could
not show: eval32()'s harness reports "died: corpus" here for evolved designs at 32 bits - with master's code as with
this batch, while the same 32-bit build runs the corpus to its end when run directly; the laptop's chain has measured
every front at 32 bits without a failure, so this is this machine's, to be watched at seed 69's processing (fail32).
**batch-check on e6044c3: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS.**

## Patch 3, how it was tested (Iteration 463)

In a clone with patches 1 and 2 committed: run-tests PASS, validate 7 of 7 IDENTICAL (with the runtime check and the
first form of stencil-check). stencil-check, its exact form:

| compiler and flags | result |
|---|---|
| gcc, the JIT's defines, -O2 | 43 stencils, every one safe to copy |
| gcc -m32 -fno-pie, the same | 43 stencils, every one safe to copy |
| gcc ... -fstack-protector-all | 43 not safe: each a jne past the copied part, to the stack check's failure path |
| gcc -m32 -fno-pie ... -fstack-protector-all | the same, 43 |
| gcc ... -pg | 43 not safe: each refers to mcount |

The stack protector's case is the instructive one: the JIT built that way still ran the corpus and ran fast (s6 with
the JIT: fib 0.341 against 0.324), because a canary never failed - the jump past the copied part was latent, never
taken. The runtime check does not see it (a short jump); stencil-check does, which is why the tests run it.

**The three together, batch-checked on 687a0e2: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS.**
