# Porting a copy-and-patch JIT to 32-bit ARM (ARMv7-A, Cortex-A9)

I'm porting a small copy-and-patch JIT from x86 to 32-bit ARM, and I'd like concrete, checkable knowledge: exact
encodings, compiler flags and known pitfalls - with sources where you can give them. Where you are not sure, say so
rather than guess; a wrong flag or encoding costs me more than a missing one.

## What exists

- A Forth virtual machine in C (a bytecode interpreter) with a lazy JIT: on a word's first call its bytecode is
  translated into native code by copying "stencils" and patching them.
- **Stencils** are small C functions, `spn_st st_x(cell *sp, cell tos)`, where `spn_st` is `struct { cell *sp; cell tos; }`
  and the top of the data stack is kept in `tos`. Each stencil ends by tail-calling the next one (a marker function), so
  stencils chain: we copy each one's bytes up to that final jump and drop the jump, so the next stencil follows in line.
  Compiled ahead of time by GCC (and clang) at -O2.
- **Holes**: every value patched at translation time (an immediate, an address, a helper's address) is produced by
  inline asm that materialises a distinctive magic constant - `movabs` on x86-64, `mov $imm32` on i386 - so we find each
  hole by scanning the stencil's bytes for its value, then overwrite it.
- **Control flow between copied code**: x86 `jmp rel32` (E9) for branches inside a translated word, `call rel32` (E8)
  for calls between translated words (a real call and return), helpers (C functions: an EXECUTE helper, a throw helper
  that longjmps back to the JIT's entry) called through holed function pointers, and a trampoline written at start-up
  (`mov reg, imm; jmp reg`) into a C function.
- **On 32-bit ARM we already have stencils** from an earlier interpreter: every hole is a `movw`/`movt` pair with a
  distinct 32-bit value, found by its two 16-bit halves; no immediate is folded into an instruction. What is missing is
  the JIT side: copying, finding the tail jump, patching branches and calls, the trampoline, the helpers' calls.
- **Target**: NVIDIA Tegra 3 (Cortex-A9, ARMv7-A, 32-bit Linux), GCC 16 natively; clang also available.

## The questions

1. **A32 or Thumb-2 (T32)** for the stencils and the code that glues them? The trade-offs for this use: regularity of
   encodings to find and patch, branch ranges, code size, interworking (the mode bit, `BX`/`BLX`), Cortex-A9 speed. How do
   I force one mode for all of it (`-marm` / `-mthumb`, attributes)?
2. **Making stencils copyable**: which flags or attributes keep GCC (and clang) from literal pools, PC-relative loads,
   GOT accesses and section anchors in such small functions, so that every constant arrives as a `movw`/`movt` pair?
   (I have seen `-mword-relocations`, `-mslow-flash-data`, `-fno-section-anchors`, `-fno-pic` mentioned - which of these
   apply to ARMv7-A Linux, and do they guarantee it?) How would I detect a stencil that still uses a literal pool, by
   scanning its code?
3. **The tail jump at a stencil's end**: what do GCC and clang emit for a sibling call at -O2 (`b`, `bx`, something via
   `ip`)? With `__attribute__((musttail))`? How do I find it reliably, and the encodings of `B`/`BL`/`BLX` (A1, and T4
   for Thumb) - the immediate's layout and scaling, the range (±32 MB in A32?), and what to emit beyond the range
   (a veneer: `ldr pc, [pc, #-4]` with a literal, or `movw`/`movt` and `bx`)?
4. **Patching `movw`/`movt`**: the A1 (and T3) encodings - the imm4:imm12 split - and whether the compiler always keeps
   the pair together and in order, or may schedule other instructions between them or reuse one half. How robust is
   finding them by decoding both halves?
5. **Returning two values**: AAPCS returns an 8-byte struct through memory (a hidden pointer in r0), not in r0:r1 as I
   want for `(sp, tos)` between stencils. What is the best way to keep both in registers - return a `uint64_t` and split
   it, an attribute (`pcs`?), a different signature? What do other copy-and-patch systems do on 32-bit ARM?
6. **Writing and running code on ARMv7 Linux**: cache maintenance after writing (`__builtin___clear_cache`, the
   `cacheflush` syscall), what Cortex-A9 needs (I-cache/D-cache coherence, the branch predictor), `mmap` with
   `PROT_EXEC` and W^X, alignment.
7. **Leaving native code early**: a helper called from native code `longjmp`s back to where the JIT was entered
   (`__builtin_setjmp`/`__builtin_longjmp` on x86). Anything ARM-specific to watch - the frame pointer, callee-saved
   registers, VFP registers, the 8-byte stack alignment at calls?
8. **Prior art** on 32-bit ARM - code copying or copy-and-patch, or a JIT that copies compiled fragments (Gforth's
   dynamic superinstructions, LuaJIT's ARM backend, copapy, others) - with links, and the pitfalls they recorded.

## The answer I'd like

Numbered as above. For each: the recommendation, the exact encodings, flags or code, the pitfalls, and sources (links)
where you have them. Mark what you are unsure of. No need to explain copy-and-patch or Forth in general.
