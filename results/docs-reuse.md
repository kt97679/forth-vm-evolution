# What the collection's doc/ gives this project (Iteration 120)

The owner: anything to reuse from the docs directory? doc/ is 52 MB, mostly
books for learning Forth (Brodie, Pelc, Kelly, the Russian books). Read for
what they say about building and measuring Forth machines. Books and papers:
ideas, not code to copy.

## Koopman, "Stack Computers: the new wave" (doc/Koopman) - the most useful

**Section 6.3, Forth instruction frequencies.** Dynamically, calls and exits
dominate everything; about 25% of instructions manipulate the stacks. Table
6.3: on the RTX 32P, combining opcodes cut the instructions executed by 10%
(op-op: SWAP DROP, OVER +) and instruction compression by ~25% (an operation
sharing its instruction with the call or exit after it). Against this
project's genes:

| combination on the RTX 32P | share of instructions | here |
|---|---|---|
| op + the EXIT after it | 12% | folds (`op;EXIT`) |
| call + EXIT -> jump | 1% | tail calls (`tail`) |
| op + op (SWAP DROP, OVER + ...) | ~3% | superinstructions (`supers`) |
| literal + op, variable + op | (their own rows) | specialisations (ADDI ..., `vf`/`vs`) |
| **op + the call after it** | **11%** | **none** |

**Priced on this project's designs** (the profiler, the selected workloads):
an operation immediately followed by a call in the same straight line is,
of all dispatches, on the fastest design 2.7% (kernel), 6.5% (parse), 6.6%
(corpus) - preceded by LIT8 19%, ?BRANCH8 19%, (PARSE) 18%, PLACE 18%, DROP 7%,
0= 7% (the top ten 95% of the pairs); on the smallest 2.7%, 3.7%, 3.8% - AND
23%, 1+ 8%, @ 8%, >R 7% (the top ten 73%). **A gene candidate, `opcall`**:
the top pairs as fused opcodes - the operation's handler then a direct jump
into the call code for the call's width, no table dispatch between - up to
2.7-6.6% of dispatches, an opcode slot a pair (competing with `supers`).

**Section 6.4, stack depths**: the deepest data stack 6-52 cells, return stack
7-39, on the book's benchmarks. This project's stacks are far deeper, but an
untouched page costs nothing: no gain in memory.

## Rodriguez, "Moving Forth" (doc/Rodriguez)

**Part 5: which words should be primitives** - the human version of the
primitive-set gene (results/deep-dive-2.md): arithmetic, logic and memory in
code; what cannot be written well in Forth (U<, RSHIFT); frequent small words
(NIP, TUCK); whatever is smaller in code; stack-juggling words with simple
logic; complex control flow in Forth. And the spectrum: 13 primitives make
"a very slow Forth", eForth has 31, CamelForth about 70 - this kernel 68, about
38 without the file and OS calls. A prior for the instruction-set search.

**Part 1**: the top of stack in a register - most PC Forths do it, the number
of operations stays the same, memory accesses fall: the `tos` gene's case.
CamelForth's source (camel80*.txt) is for personal or educational use only.

## Knaggs, "Practical and theoretical aspects of Forth software development" (1993)

A type algebra for stack effects (sections 1.8.2 and 4, "Formal Forth"): a
formal way to check that a fused sequence, a rewrite or an edited word keeps
its stack effect - the check genetic improvement (level 3) would want next to
the held-out tests.

## The rest

- Bruno and Lassagne, "The Generation of Optimal Code for Stack Machines"
  (JACM): optimal evaluation of expression trees on a finite-depth stack -
  compiler theory for expressions, which this system's hand-written Forth
  does not have.
- The ANS standard (doc/ANSI, the X3.215 draft): for the word sets the kernel
  lacks (:NONAME, CATCH/THROW, COMPARE, search order, AHEAD, D-, double
  literals) - each would let more of the held-out ANS suite run.
- "Threading in forth.txt", Moving Forth part 1: threading techniques
  (ITC, DTC, STC, token) - background; the genes have explored these.
- Baranov, "Forth and its implementations" (Russian): implementation
  techniques - worth a reading for ideas, not yet read in depth.
- Gritsenko's stdcore: a Russian translation of the ANS core word set.
  Cherezov: Forth's ideas (extensibility, a compact micro-kernel). The 21C3
  paper and slides: overviews. The books (Brodie, Pelc, Kelly ...): learning.
