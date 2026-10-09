# Deep dive 2: more genes, and an instruction set evolution can build (Iteration 115)

The owner: add the primitive-set gene; find more ideas for genes; and can
the GP process be changed so that new designs - "SOD32 from nothing" - become
possible? Measured on the VM on seed 35's fastest (e5193642ef) and smallest
(585376cf49) designs, the long workloads.

## 1. The primitive-set gene, priced: no demotion pays

A demoted primitive becomes a colon word over the rest: every use grows from
a one-byte opcode to a two-byte call, the word gains a body, each execution
costs a call, its operations and EXIT - against a C handler of 10-40 bytes.
Return-stack words cannot be demoted (a colon body would read its own return
address), nor the file and OS calls without one SYSCALL primitive.

| primitive | uses in the image (smallest, fastest) | dispatches (kernel, parse, corpus) | demoted |
|---|---|---|---|
| OVER | 38, 35 | 2.5%, 2.4%, 2.7% | ~+28 bytes in all; each use 6 dispatches, not 1 |
| ROT | 32, 17 | up to 5.8% | worse |
| NEGATE | 8, 8 | up to 1.4% | ~+5 bytes, a little slower |
| UM* | 4, 3 | 3.6% of kernel on the fastest | a shift-and-add loop: kernel more than 2x slower |
| UM/MOD, D+ | 1-6 | ~0.2% | the Forth loop larger than the C |
| = U< < LSHIFT RSHIFT | 5-22 | 0.5-1.7% | branches or loops in Forth: larger, slower |

So the kernel's primitive set is near a sweet spot - primitives are tiny C,
their Forth replacements cost more bytes and time - and evolution would never
pick a demotion on its own. The gene matters as the floor of section 3, not
alone; recorded in lab/evolve/GENES.md, not built.

## 2. New genes, with their numbers

**Memory has a lever** - `fbuf`, built (Iteration 115): the engine gives each
open file a 4 KB read-ahead buffer; with 1 KB the smallest design's kernel
workload touches 172 KB instead of 200, with 512 bytes 168 (the fastest:
216 -> 180 -> 176). The front's memory spans 186-200 KB: this jumps the 8 KB
tie three to five times over. The price: more read(2) calls on files.

**The stack check** - `kstack`, next: after every word the interpreter runs
?STACK - DEPTH DUP 0< SWAP 10000 > OR ABORT" Stack error" - whose ABORT" calls
(ABORT") to skip its message: **17.8% of parse's dispatches** (12.7% + 5.1%),
~12% of corpus's. A C opcode doing the check, falling into the Forth body
only when it fails (the error path unchanged): ~15 dispatches a word -> ~3.

**Numbers** - `knum`: NUMBER? 19.1% of parse, 7.8% of corpus - a C fast path
for plain numbers, the Forth body for the rest (prefixes, points, errors).

Where parse's dispatches go on the fastest design: INTERPRET 34.0%, NUMBER?
19.1%, PARSE 16.9%, ?STACK 12.7%, (ABORT") 5.1%, REFILL 2.9%, HERE 2.6%,
>IN, BL, CONTEXT ~1.3% each. Corpus: INTERPRET 24.8%, PARSE 12.9%, ?STACK
9.1%, NUMBER? 7.8%, run-time code 5.0%.

Others, smaller or costlier: hot-site inlining from the current fastest
design (hotinl's list is from an old one: HERE, BL, >IN, CONTEXT ~6% of
parse); more JIT stencils (COUNT, DODOES, PICK, (?DO), (+LOOP)); 16-bit
dispatch tables (~768 bytes; the generators rewrite that table by its text);
one SYSCALL primitive (~1.3 KB and the handlers - vsnprintf was dead code, not
the shell's); packed names (~500 bytes, later); the outer interpreter's loop
in C (INTERPRET 34% of parse - large, re-entrant: later).

**For the search itself** - against the anchoring the owner suspected:
`fromzero` (built, section 3); immigrants (a few random genomes every
generation); macro-mutations (several genes at once, now and then); islands
(the four workers as four populations, migrating now and then); mutation
rates that follow success (genes whose mutations reach the front, mutated
more); a knock-in sweep (the front's designs with each recent gene added).

## 3. An instruction set evolution can build: SOD32 from nothing

Today's genes switch mechanisms written by hand: evolution selects among
them, it does not invent. SOD32 is a point in this space (the hand-made
s0-cell stage: cell tokens, the kernel's primitives), and every run starts
next to it - so "from nothing" cannot happen yet. Inventing a machine from no
building blocks cannot happen at all: almost every random instruction set
runs nothing, so fitness has no slope to climb, and the kernel and compiler
would have to evolve with it. What can be done is to make the INSTRUCTION SET
a gene, between a floor and a ceiling evolution chooses:

1. **The floor - demotion** (section 1): any derived primitive can be a colon
   word over a minimal core (stack, memory, + AND OR XOR, the branches,
   READ WRITE BYE, one SYSCALL). Not worth it alone; it lets a design start
   with almost nothing.
2. **The ceiling - promotion by synthesis**: any straight-line kernel word or
   hot sequence can become an opcode whose C handler is COMPOSED from the
   core's handlers - tools/gen-super.py already composes pairs; generalized
   to words and n-grams, evolution makes new instructions, not just picks
   hand-written ones (format-10 and the kernel genes are hand-written now).
   Correct by construction: compositions of verified handlers, their stack
   effects checked.
3. **From zero** - built now: `fromzero` (next-run.sh; evolve.py --fromzero),
   the first generation all random genomes - no hand-made design, founder,
   carried front or mutant of a hand-made one. Over today's space first; over
   1 and 2 later.

With all three, SOD32's instruction set - the core plus OVER ROT UM* UM/MOD
D+ and the file words promoted - is one point evolution can BUILD from a
minimal core with cell tokens, and it can go past it to instruction sets no
one wrote. Cost, roughly: 1 a day (the converter's colon bodies, the engine's
handlers dropped, a library of definitions); 2 two or three days (the
synthesizer, its genes); 3 done. What stays out of reach: primitives whose
meaning is not a composition of the core's - new semantics need program
synthesis with an oracle.
