# JIT.md - a minimal lazy JIT, as a gene (a plan, Iteration 73)

The owner (2026-10-06): a JIT may be a gene - lazy, so the image stays
small and speed grows - but **no significant growth in code complexity or
memory**, and both tracked (done: every design's engine code and peak
memory are recorded since Iteration 73). The project's aim decides the
rest (GOALS.md, "The aim"): the smallest mechanism that pays, behind a
gene, measured, and taken out if it does not pay.

## What is borrowed

SPN (FINDINGS-SPN.md) proved copy-and-patch on this system, on x86-64 and
32-bit ARM. Borrowed as they are: its stencils (`engine/spn-stencils.c`,
one Forth operation an ordinary C function the compiler builds and nobody
calls), its markers and native convention (`spn-markers.c`, `spn-abi.h`:
the stack as `(sp, tos)` in registers both ways), and its rule that a
stencil of an unexpected shape is not used - slower, never wrong. NOT
borrowed: SPN's engine copy (1,861 lines) or its translator (~2,600 lines
of Forth, a whole CV8 decoder).

## The design

- **Only words compiled at run time**: the image never grows - no native
  code in it, no translator in it.
- **Lazy, on the first call**: the run-time compiler begins each colon
  word with a one-byte `JIT?` opcode and four bytes reserved (in the
  dictionary at run time, not the image). Its first execution runs the
  translator; then `JIT?` becomes `NATIVE` and the four bytes the native
  code's offset - or, if the word cannot be translated, a branch over
  them, and the word stays bytecode for good. A word never called is
  never translated.
- **All or nothing per word**: the translator (C, in the engine) walks the
  word's bytecode; every operation must have a stencil - a short list:
  the stack operations, arithmetic and comparisons, literals, @ ! C@ C!,
  branches, the fused tests and ADDI the run-time compiler writes, the
  loop opcodes, EXIT - and every call must reach a word already native,
  or itself (recursion). Anything else: no translation, no fallback code.
- **Memory**: native code in one executable region, allocated once,
  growing by what is translated; full, nothing more is translated.

## Budgets - measured, or it comes out

Since Iteration 75 the evolution itself weighs these: binary + image and
memory (pages touched) are objectives beside speed, equal - so the JIT's
stencils and translator count in the binary, and its native code in the
memory, of every design that carries the gene.


- **Code**: new C at most ~300 lines beside SPN's stencils; engine code
  (the tracked .text) at most +15 KB over the design without the gene.
- **Memory**: peak resident memory at most +1 MB on any workload.
- **Image**: unchanged (the Forth side: a few lines in forth/cv8t.4,
  counted in the image as always).
- **It must pay**: counted and timed on the code it targets - fib, loop,
  the sieve, the kernel workload's cross-compiler - or it is removed, as
  `rtlit` was (Iteration 59).

## Phase 1's numbers (Iteration 80)

Built as designed: `forth/cv8t-jit.4` (the header, an overlay loaded only
with the gene), `engine/jit.c` (the scanner and the translator, 246
lines with the check's main), the handler `L_x_jit` (vm-lab.c), the
converter's per-design table `vm-jit-ops.h` (each operation's stencils
from its name: 86 of seed 19's fastest design's 168 operations), the gene
`jit` (lab/evolve: the two-bit tag, byte headers, the cached top, one
state, no tail calls; x86-64). Seed 19's fastest, cc0b1e2aeb, measured
with and without it, 5 rounds:

| | without | with the JIT | ratio |
|---|---|---|---|
| fib | 0.605 | 0.221 | 0.37 |
| loop | 0.173 | 0.070 | 0.41 |
| kernel | 0.307 | 0.337 | 1.10 |
| parse | 0.102 | 0.115 | 1.13 |
| corpus | 0.192 | 0.212 | 1.11 |
| sieve (held out) | 0.438 | 0.472 | 1.08 |
| speed (geometric mean) | 0.229 | 0.166 | 0.72 |
| image / binary / memory | 9,064 / 33,448 / 212 KB | 9,200 / 41,736 / 216 KB | |

Budgets: engine code +8.3 KB (15 allowed), new C ~250 lines (~300),
memory +4 KB (1 MB), the image +136 bytes (the new : and ;). It pays where
code is compiled at run time and runs hot; elsewhere every run-time word's
call pays the JIT dispatch, and most such words stay bytecode - they call
kernel words. Across gene combinations: eight more seed-19 front designs with the gene
on - the four with the cached top pass the corpus and the kernel
workload (fib 0.21-0.29, loop 0.07-0.08 where loops compile to opcodes at
run time); the other four keep it dormant. Where a word cannot be
translated, the cost is more than the JIT dispatch: the smallest design's
loop, its INNER calling the kernel's loop words, 1.51 -> 1.70 - the new
engine code moving the interpreter's layout, likely. **Next
optimisations, priced first**: a word that stays
bytecode should cost nothing per call (e.g. its callers re-pointed past
the header); calls from native code to bytecode words (SPN's st_interp);
?DO and +LOOP; 32-bit ARM.

## Iteration 81: two fixes, and where the overhead is

- **No format-10 slot.** The JIT opcode took the first format-10 slot,
  which the pairs share: seed 19's fastest lost R> =. Now it is an
  operation of its own under the tag (T2_JIT = 0xFFFD): a pinned one-byte
  code and no slot; designs keep their pairs.
- **Bytecode words cost their call sites nothing**: the first call
  through the header re-points the call past it (jit_repoint).

Neither moved the overhead on kernel, parse and corpus (10-17% on this
VM), and with translation switched off it was there too: it belongs to
the design, not the translator - the pinned code pushes CELLS into the
escaped band, the engine's ~8 KB move the interpreter's layout - and to
this VM's noise. The laptop's comparison (10 rounds, two CPUs) weighs it.

**The binary objective moves in 4 KB steps**: a static engine's segments
are page aligned, so a few bytes can cost a page (41,736 -> 45,832 here) -
why the converged front's engines came in sizes 4 KB apart. To raise
with the owner: link without page alignment, so the objective sees bytes.

## The phases

1. **A prototype on the VM** - begun, Iteration 74: engine/jit.c reads
   SPN's stencils in C (tools/jit-check.sh prints how a compiler shaped
   them: at gcc -O2 and -Os every stencil fib and loop need has the
   expected holes; ?DO's does not, so it would stay bytecode). Next: the
   converter's per-design table (each logical operation's stencils and
   operand), the translator, JIT? and NATIVE, executable memory, the
   run-time compiler's header. The plan: x86-64, tag-2 designs: `JIT?`/`NATIVE`, the
   translator for the short list, executable memory. Measured: fib and
   loop's time, engine code, peak memory, image size; the life test.
   Decision with the owner on its numbers.
2. If it pays: the gene `jit`, the evolver's build, 32-bit ARM (SPN's
   stencils already run there; the patcher's ARM forms and an icache
   flush), the proofs as for the tag (all engine forms, past 4 MB).
3. A laptop run.
