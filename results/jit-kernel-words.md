# Kernel words made native, priced (Iteration 103)

The owner (Iteration 103): "if we expand any word we eventually can turn it
into a sequence of primitives ... we can start with converting only words
that contain only primitives." No expansion is needed: a kernel word
translated once, kept beside the image, can be called natively by every
translated caller - native code bounded by the image's own. Priced with
lab/evolve/callsites.py (its JIT section, Iteration 90's fixpoint, two new
kinds of blocker cleared) on two JIT designs of the front of all runs,
70bc3ae6b5 and 106f83c7bf, with the long workloads (Iteration 100); the
designs agree to 0.5%. Of 296 kernel code words, 76 are made of operations
with stencils only; letting them call each other adds none.

Of each workload's dispatches (70bc3ae6b5):

| workload | in bytecode now | kernel words of primitives native | the same, recursively | and data words as literals | every call translatable (SPN's st_interp) |
|---|---|---|---|---|---|
| kernel | 46.6% | 0.0% | 0.0% | **8.2%** | 10.7% |
| corpus | 4.5% | 0.1% | 0.1% | 0.1% | 1.7% |
| sieve (held out) | 79.0% | 0.0% | 0.0% | 0.0% | 79.0% |

So the first step pays together with data words and constants as literals:
8.2% of the kernel workload's dispatches native, most of what native code
calling bytecode would give there, without re-entering the interpreter.
What still waits: the kernel workload's hottest bytecode word (24.6% of its
dispatches) on run-time data and `>R` (no stencil; `>R` is first in words
holding 29.6%); the sieve's PRIMES (79%) on `FILL` - a C opcode without a
stencil (1+ and 2DROP have theirs). The JIT's next steps, each priced:
kernel words native with data as literals (8.2% of kernel), a FILL stencil
(the sieve's 79%), stencils for >R and R> (up to ~30% more of kernel), then
native code calling bytecode for the rest.
