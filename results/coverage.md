# Engine coverage - are all execution paths tested? (Iterations 159-161)

The owner, after the far-address findings: check that every execution path has
a test. Measured, not guessed: engines built with --coverage (the C library
runtime - gcov writes at exit); the whole run-tests.sh suite on the stage
engines; the gate, the tests and all eight workloads on 14 front designs.
tools/covsum.py: per binary, the lines run and the handlers (L_ labels, switch
cases) nothing reached.

## The stages

Found: READ-FILE and RESIZE run by no test on any engine; FREE, ALLOCATE,
WRITE-FILE and SYSCALL by none on most stages (the shell suites, which use them,
run on s0 and s5 only); the 32-bit engines' system-call translation (x86-64's
39 -> i386's 20). tests/core/paths.fth - memory, the file cycle with WRITE-LINE,
a system call by x86-64's number, <> and INVERT compiled - runs on every stage
at both widths, with a control. Lines run: relf.c (s0) 86-87% -> 92-93%,
pack4/pack8 73-75% -> 89-90%, the vm-lab stages 70-82% -> 82-87%.

## The front

Fourteen designs - seed 38's smallest and fastest, a JIT, jitx, t2wide, escape,
rtfuse, supers, klookup and hotinl 40 design, one without kfast, one without
kinput, and both founders. Their builds copy code stencils (the JIT, run-time
fusion) byte for byte: those two files are left uninstrumented
(-fprofile-exclude-files=spn-), or the copies carry counters at fixed addresses
and break (12 of 14 died at the corpus that way). jit.c: 98-100% of its lines
run; vm.c: 80-82%. WRITE-LINE was run by none: paths.fth now writes a line.

## Left, each with its reason

- L_nosys, L_t2bad: guards - the 17 retired OS slots have no names; no opcode
  is invalid in an image the converter wrote.
- L_invert: nothing emits it - both converters inline INVERT as -1 XOR.
- L_esc in tag2 engines: tag2 escapes through its own handler, which ran.
- LIT64 at 32-bit: never emitted at 4-byte cells. L_noop (relf, pack): padding.
- The locals opcodes: evolved images are kernel-only and never have them; on the
  stages only images with locals.4 converted do - s5's shell, where the shell
  suite runs them. s6 has no shell image.
- s1's near DODOES: the converter's numbered DOES> tails; DOES> words compiled
  at run time take the far form.
- exit_group's translation at 32-bit outside s0 and s5: a test calling it would
  end its own run, and its coverage.

## gdb

A dictionary overflow on s6 (Iteration 161): SIGSEGV at a byte store
(mov %al,(%r12)) past the end of memory - the refusal in far-addresses.md.

## A correction (Iteration 163)

The standard suite in tests/ans runs - by lab/evolve/ans-check.py, not by
run-tests.sh - through prelude.fth and upper-cased copies; a probe that fed
runtests.fth raw died at .( and was read as "never runs". What it does not
reach is the word sets the kernel lacks: see tracer.md, "Second use".
