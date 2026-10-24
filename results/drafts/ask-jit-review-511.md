# A bug hunt in a copy-and-patch JIT (three files attached)

Please read the attached JIT and find real bugs: places where the native code it produces does something different
from what the interpreter would do, or where the JIT itself can crash or corrupt memory. I will turn every bug you report
into a test and run it at both widths, so a specific, checkable claim is worth far more than a general worry.

## Attached

- `jit.c` - the JIT: decoding a word's bytecode into an operation list, the checks that refuse a word, the passes that
  size and copy stencils, patching, the helpers called from native code.
- `spn-stencils.c` - the stencils: small C functions copied as machine code; their "holes" (values patched at
  translation) are magic constants made by inline asm, found by scanning the copied bytes.
- `vm-lab-jit-excerpts.c` - the interpreter's side: `L_x_jit` (entering native code), `jit_interp` and `jit_leave`
  (native code calling back into the interpreter), and the declarations around them.

## How it works, and what must hold

- **Lazy, all or nothing**: a word is translated on its first call. If any operation in it cannot be translated, the whole
  word is refused and stays interpreted; refusals are cached. Callees are translated first, recursively, to a depth
  limit (`JIT_DEPTH`).
- **The stack protocol**: native code runs with `sp` (the data stack, deeper cells at higher addresses) and `tos` (the
  top, in a register) as its two arguments; each stencil passes them on by a tail call. The return stack is `jit_rp` (in
  memory), or a register under the gene `jitrp`. The translation must leave both stacks exactly as interpretation would.
- **Branches** are resolved by matching a branch's target address against the operations' addresses (`at[]`). Under the
  gene **jitfuse**, two operations become one stencil - a literal into `+ < > = XOR AND OR`, or `I` into `+` or `2@` - and
  the second must never be a branch target.
- **jitk**: a register cache of the top few stack items, a state machine; the canonical state at branch targets, calls
  and helpers.
- **jitcfa**: the return stack's depth checked along every control-flow path (`>R`/`R>` balanced on each).
- **jitexec**: `EXECUTE` through a helper (`jit_exec`) with a three-cell cache at each site; a callee it cannot translate
  runs in the interpreter (`jit_interp`: a sentinel return address on the return stack, a trampoline, `longjmp` back).
- **jitmul**: `UM/MOD` with a zero divisor calls a helper that `longjmp`s to the JIT's entry (`jit_call`), and the
  interpreter throws -10. `(ABORT")` with a true flag calls a helper that resumes the interpreter at the call.
- **Two widths**: x86-64 (8-byte cells) and i386 (4-byte cells; native code uses `regparm(2)`, written `SPN_CC`; the
  helpers use the C convention).
- **The operation table** (`jit_ops[]`, generated per design): rows `{ok, n, opnd, k, {stencils}}` - `n` stencils, `k` a
  constant for them, `opnd` the operand's kind: 0 none, 1-5 an unsigned byte, 16-bit, signed 32-bit, 64-bit or signed
  byte literal, 6-7 a branch with an 8- or 16-bit offset, 8-9 a variable's slot.

Bugs we have already found, to show the kind: constants in the converter's map that assumed 8-byte cells at both
widths (`CELL+`, `CELLS`, `2@`, `2!`); jitfuse's pair marks overwritten when translating a callee recursively reused the
same global array; refusals for depth cached as if final. All fixed in the attached files.

## The answer I'd like

For each suspected bug: where (function and line), the mechanism, **a minimal trigger** - a Forth program or the
condition that produces it - the expected and the actual behaviour, and your confidence (high, medium, low). Then,
separately: places that are risky but that you believe are correct, and invariants no code checks that should be
asserted. No style comments, and no "might be an issue" without a mechanism.
