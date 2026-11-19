# The system-call wrapper at x86-64 - the patch's tests (Iteration 707)

The after-seed-96 batch's rtsc (results/pending/ORDER.md): found by reading the smallest design's engine by symbol size
(nm -S on 21768033b7's engine.full: 4,784 bytes of code - virtual_machine 2,028, main 758, the dispatch table 512,
**syscall 241**) - the ideation pilot's loop (results/drafts/ideation-707.md): a proposal against the largest, built,
measured exactly. The runtime's variadic `syscall(long n, ...)` (engine/rt-linux-x86_64.c) makes the compiler save every
argument register for va_arg; Iteration 257 gave open the fixed-argument rt_open for the same reason, not syscall. The
engine's one call (the SYSCALL operation, vm-lab.c) now goes through SYSCALL6: rt_syscall6 - six arguments, the same
errors (-1, errno) - where the runtime is linked at x86-64; the variadic syscall stays for any other caller and
--gc-sections drops it. At i386 and ARMv7 SYSCALL6 is the variadic call as before: their runtimes keep it for their own
calls, so a second function there cost 16 bytes (measured, then left out).

results/drafts/rtsc-707.py on results/followup-seed96-roles.md: 20 designs - the 8 smallest and 12 spread by speed,
tos, GCC and clang, the JIT among them - built by master and by the patched tree; each binary's bytes, evolve.alive, and
fib and apps against s6 at its width:

| width | designs | binary, patched less master | alive, fib and apps as s6 |
|---|---:|---|---:|
| 8-byte cells | 20 | -304 to -192 bytes | 20 of 20 |
| 4-byte cells | 20 | +0 to +0 bytes | 20 of 20 |

At 8-byte cells -192 bytes on the interpreted designs, -208 to -304 on the JIT ones (their engines align functions);
the smallest, 21768033b7, 4,960 to 4,768 bytes - its total 22,409 to 22,217 (-0.86 %). Speed: the wrapper runs once a
system call, and the engine's I/O is buffered (fbuf, t_obuf) - no timing effect expected; chain B measures it anyway.
