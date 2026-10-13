# Calls and returns at the fast end - priced (Iteration 245)

The C baseline (results/c-baseline-x86-64.md) puts the fastest design,
28677d13b1 (JIT, jitinl, jitloop, jitx, cached top), at 16.8x C -O2 on
ackermann and 5.1x on fib, against 1.7-3.5x on the loop benchmarks. Is the
JIT's call and return the cost?

## What a call costs now

Native words call each other with the machine's own call and ret (jit.c), so
returns are predicted by the CPU's return stack. In 28677d13b1's engine:

    st_call: sub $8,%rsp; call <callee>; add $8,%rsp; mov %rax,%rdi; mov %rdx,%rsi
    st_exit: mov %rdi,%rax; mov %rsi,%rdx; ret

Eight instructions a call and return, two of them predicted transfers: the
data-stack state (sp, tos) moves through the return registers and back.

## Where the gap is

C at -O0 is 13.4x C -O2 on ackermann and 5.2x on fib; the JIT is 16.8x and
5.1x - about unoptimized C, which also calls and returns every time. -O2 earns
its 13x on ackermann by turning two of the three recursive calls (tail calls)
into jumps, keeping arguments in registers, and on fib by eliminating one call
in two (accumulator). So the gap is not the call's eight instructions but what
an optimizing compiler does around them: tail calls, and registers instead of
the memory stack.

## What a JIT tail call would buy

bench/ackermann.fth's -ack makes three recursive calls; two are tail calls - a
RECURSE followed by THEN THEN ; (in the bytecode, the call, a BRANCH to the
EXIT, the EXIT). Translated as a jump to the callee instead (S_BRANCH aimed at
the callee's native entry - its ret then returns to our caller; no new stencil),
each removes st_call, the branch and st_exit: about 9 of the roughly 35
instructions a -ack call runs, and the native stack no longer grows with the
tail recursion. Estimate: ackermann 15-25% faster; fib nothing (no tail calls);
loop, sieve, bubble nothing measurable; parse a little at most. One selection
workload in six: about 3-4% on the speed objective's geometric mean, for the
designs with the JIT.

Cost: in the translator only (jit.c) - recognising a call to a native word whose
next operation is EXIT, or a BRANCH chain ending at EXIT; some tens of bytes.
Safe because return addresses are on the machine stack, not the Forth return
stack: >R, R> and loop parameters are untouched by a jump; a call followed by
anything else (R>, LOOP) is not a tail call.

Recommendation: a gene, jittail (0/1), like the bytecode engines' tail - offered
to evolution, timed by the laptop. The rest of the gap - the data stack in
memory between operations - needs a register-allocating translator, a much
larger step.
