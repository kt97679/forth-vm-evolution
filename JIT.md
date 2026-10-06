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

- **Code**: new C at most ~300 lines beside SPN's stencils; engine code
  (the tracked .text) at most +15 KB over the design without the gene.
- **Memory**: peak resident memory at most +1 MB on any workload.
- **Image**: unchanged (the Forth side: a few lines in forth/cv8t.4,
  counted in the image as always).
- **It must pay**: counted and timed on the code it targets - fib, loop,
  the sieve, the kernel workload's cross-compiler - or it is removed, as
  `rtlit` was (Iteration 59).

## The phases

1. **A prototype on the VM**, x86-64, tag-2 designs: `JIT?`/`NATIVE`, the
   translator for the short list, executable memory. Measured: fib and
   loop's time, engine code, peak memory, image size; the life test.
   Decision with the owner on its numbers.
2. If it pays: the gene `jit`, the evolver's build, 32-bit ARM (SPN's
   stencils already run there; the patcher's ARM forms and an icache
   flush), the proofs as for the tag (all engine forms, past 4 MB).
3. A laptop run.
