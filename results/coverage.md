# Engine coverage - are all execution paths tested? (Iterations 159-160)

The owner, after the far-address findings: check that every execution path has
a test. Measured, not guessed: every stage engine built with --coverage (the C
library runtime: gcov writes at exit), the whole run-tests.sh suite run on them,
gcov per binary - tools/covsum.py lists the lines run and the handlers (L_
labels, switch cases) that nothing reached.

**Found - handlers no test ran:** READ-FILE, RESIZE on every engine; FREE,
ALLOCATE, WRITE-FILE, SYSCALL on most stages (the shell suites, which use them,
run on s0 and s5 only); the 32-bit engines' system-call translation (x86-64 39
-> i386 20). tests/core/paths.fth - memory, the whole file cycle, a system call
by x86-64's number, s6's <> and INVERT - runs on every stage at both widths in
run-tests.sh, with a control. Lines run, before -> after: relf.c (s0) 86-87% ->
92-93%, pack4/pack8 73-75% -> 89-90%, the vm-lab stages 70-82% -> 82-87%.

**Left, each with its reason:**
- L_nosys: where the 17 retired OS primitives point - no name reaches it; a guard.
- LIT64 on 32-bit stages: never emitted at 4-byte cells - dead by construction.
- L_noop (relf, pack): padding, never executed.
- The escape opcode on the hand-made stages: none has the escape gene; the
  front's escape designs are where it runs - see below.
- s6's locals opcodes: locals.4 is not loaded by any test on s6 - a gap.
- s1's near DODOES: its DOES> words in the tests all take the far form - a gap.
- exit_group's translation at 32-bit (vm-lab, pack): covered on s0 and s5 by
  the shell suites; elsewhere not, and a test calling it would end its own run.

**Not measured yet - the front's engines.** Their builds copy code stencils
(the JIT, run-time fusion) byte for byte; compiled with --coverage those carry
counter updates at fixed addresses and break when copied - 12 of 14 sampled
front designs died at the corpus under instrumentation. Measuring the tag2,
JIT and escape paths needs the stencil compile left uninstrumented.
