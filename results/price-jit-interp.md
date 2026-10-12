# Native code calling byte code, priced again (Iteration 220)

Item 2 of results/drafts/jit-vm-survey.md, GENES.md's candidate 5 (SPN's
`st_interp`): let a translated word call a word that stays byte code, so a
word the JIT now leaves because of one such call goes native. Priced at
Iteration 90 at 10% of the kernel workload's dispatches and 80% of the
sieve's - before jitx (Iteration 108) made the sieve's PRIMES native.

**Method.** The `JIT_PRICE` build (results/price-jit-stack.md): the JIT
translates as it would, the byte code runs and is counted. Its dump now also
lists every call of every word the JIT met (`K` lines, engine/jit.c, price
builds only; two designs' engines and images byte for byte as before). For
each word met and left byte code: its operations run, whether it was left by
an operation without a stencil (stays byte code whatever happens) or by a
call alone, and how often the latter calls a word that is not native - each
such call would cross from native code into the interpreter and back.

The fastest design of all runs (28677d13b1), all workloads:

| workload | left by a call alone: words, operations (of all dispatched) | crossings | operations per crossing |
|---|---|---|---|
| kernel | 58 words, 180,846 (9.3%) | 44,675 | 4.0 |
| corpus | 191 words, 166,835 (4.1%) | 54,795 | 3.0 |
| bubble | 4 words, 61,500 (0.5%) | 18,156 | 3.4 |
| sieve, ackermann | 156 and 138 operations | 6 and 69 | - |
| fib, loop, parse | none | - | - |

(Left by an operation without a stencil: 3.9% of the kernel workload, 0.2%
of bubble, nothing elsewhere.)

**Not built.** The prize is a tenth of what Iteration 90 measured where it
is largest, and those words would run three or four operations native
between crossings: each crossing saves and restores the stack and return
state and re-enters the interpreter - tens of instructions - for the few
dispatches it spares. Recorded in GOALS.md's register.
