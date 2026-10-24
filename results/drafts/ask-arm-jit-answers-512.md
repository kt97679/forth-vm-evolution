# The answers to the ARM prompt, checked (Iteration 512)

Five answers to results/drafts/ask-arm-jit-511.md (the owner, 512), checked here with GCC 13.3's ARM cross compiler
(arm-linux-gnueabihf, -march=armv7-a, hard float), QEMU's ARM user mode, Linux's own source, and the assembler -
and a copy-and-patch round trip built from what they agree on: results/drafts/arm-cp-poc-512.c, three stencils copied,
two movw/movt holes patched, the tail jumps found and dropped, (sp, tos) in r0:r1 in and out, the code flushed and
run under QEMU - 40 2 + gives 42. QEMU does not model caches: the flush is only shown to be called; the Tegra is the
real test.

## What holds - checked here

| Question | What the answers agree on | Checked |
|---|---|---|
| 1. Mode | A32 (-marm), all five; fixed 4-byte words, ±32 MB branches | the round trip is A32 throughout |
| 3. Tail jump | a sibling call at -O2 is `b next` | compiled: `f_u64` ends `b next`; the stencils too - *if the marker is opaque*: a marker defined in the same file was inlined away (`noipa`) |
| 3. Encodings | B = cond 1010 imm24, BL = cond 1011; target = address + 8 + imm24*4; veneer `ldr pc, [pc, #-4]` = E51FF004 | assembled: `b .+0x1000` = EA0003FE, `bl .-8` = EBFFFFFC, E51FF004 |
| 4. movw/movt | A1: imm4 in bits 19:16, imm12 in 11:0; MOVW 0x03000000, MOVT 0x03400000 (cond aside); one asm statement keeps the pair together | assembled: E3013234 / E3453678 for 0x1234 / 0x5678; patched and run |
| 5. Two values | an 8-byte struct returns through memory (sret); a uint64_t in r0:r1 | compiled: the struct version takes a hidden pointer in r0; **this project's ARM stencils already return uint64_t** (spn-abi.h, Iteration 30) |
| 6. Cache | `__builtin___clear_cache` → libgcc's `__clear_cache` → the kernel; mmap RW, write, flush, mprotect RX | compiled: `bl __clear_cache`; Linux's v7_coherent_user_range cleans D to the point of unification, invalidates I **and the branch predictor** (BPIALL/BPIALLIS, cache-v7.S) - answer 5's claim, right |
| 7. longjmp | 8-byte stack alignment at calls | - |
| Literal pools | LDR Rt, [PC, #imm] = 0x?59F.... / 0x?51F.... (cond aside) | assembled: `ldr r0, [pc, #8]` = E59F0008; the round trip refuses a stencil holding one |

## What is wrong - checked here

- **`-mword-relocations` makes literal pools, not movw/movt** (answers 2 and 4 recommend it): with it, a global's
  address became `ldr r3, .L10` - a literal load; without it, `movw/movt #:lower16:gvar`. Answer 1 is right that it
  does not mean movw/movt; it is worse - the opposite of what a copyable stencil needs.
- **`-mslow-flash-data` is not for ARMv7-A** (answer 5 calls it "the magic flag"; answer 2 "relevant"): GCC refuses
  it - *only supports non-pic code on M-profile targets with the MOVT instruction*. Answers 1 and 3 are right.
- **"The compiler always emits movw/movt consecutively"** (answer 5) - only one asm statement guarantees it, as
  answers 1-3 say; our holes are made that way already.
- **`longjmp` does not restore VFP registers** (answers 3 and 5) - not our case: a function holding
  `__builtin_setjmp` saves r4-r10, fp, lr **and d8-d15** in its own prologue (compiled: `vpush {d8-d15}`), so the JIT's
  entry restores them on its way out, and our stencils use no floating point.
- **Found here, in none of the answers: the distribution's default stack protector** puts a literal pool into every
  function with a frame (Ubuntu's GCC: the canary's address, `ldr ip, .L6`) - stencils need `-fno-stack-protector`
  (our x86 stencils are already checked for it: stencil-check, "a stack protector would make all 43 unsafe").

## The answers, ranked

1 is the most careful (flags right, veneers both ways, uint64_t, the setjmp caution, says what it cannot verify); 3 is
good and concise; 2 is mixed (recommends -mword-relocations); 4 is thin, recommends -mword-relocations, and its literal-
pool bit pattern is garbled; 5 is the most confident and has the most errors (-mslow-flash-data, "always consecutive")
alongside one right claim no other made firmly (the branch predictor). Prior art: none verified a 32-bit ARM
copy-and-patch project (copapy's ARMv7 wheels were not confirmed by any; Gforth's dynamic superinstructions and
LuaJIT's ARM backend as references only).

## For the port (HANDOFF's item 2)

Stencils: `-O2 -marm -march=armv7-a -mfpu=neon -mfloat-abi=hard -fno-pic -fno-stack-protector`, no
`-mword-relocations`; holes as one asm movw/movt each (as now); the marker opaque. The JIT: a stencil's end is its
`b <marker>` (cond AL, decoded target = the marker); refuse any LDR from PC; branches and calls between copied code as
B/BL with the +8 bias, a `movw ip; movt ip; bx ip` veneer past ±32 MB (12 bytes); the trampoline the same; helpers called
through a register (`blx`), AAPCS, the stack 8-aligned; `__builtin___clear_cache` then mprotect RX; jit_call's
`__builtin_setjmp` as on x86. QEMU for correctness here (tools/arm-qemu-check.sh's setup), the Tegra for the cache
and the speed.
