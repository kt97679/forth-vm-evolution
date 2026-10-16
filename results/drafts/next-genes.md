# The next genes - where the dispatches go now (Iteration 323)

Seed 54 runs the after-seed-52 genes; if it is small, the stopping rule ends them until new
genes exist. This is the search for those.

## The interpreted designs - lab/evolve/price.py on seed 53's three fastest

ccf55ad2f5, b926dd6bc8, b38afcd676 (0.343-0.355 of s6's time; the JIT designs 0.13-0.15), their
dispatch streams on the selection workloads, after their own fusions:

| workload | calls | EXIT | calls + EXIT | next 16 pairs (overstated) |
|---|---|---|---|---|
| kernel | 17-19% | 7-10% | 25-29% | 8-11% |
| fib | 11% | 11-12% | 22-24% | 12-21% |
| corpus | 12-14% | 8-9% | 21-23% | 16-19% |
| bubble | 16-19% | 10-16% | 29-32% | 7-8% |
| ackermann | 27-29% | 8% | 35-37% | 0.1% |
| loop | 0% | 0% | 0% | 60-100% |

Triples negligible (the best 0.3%). Calls and returns are the largest share - as missmap found
for mispredictions (15-25%) - but the genes for them exist: folds (prim;EXIT for 23 primitives),
tail, hotinl, factor, opinline, rtempty. Pairs: price.py's own record - nine of the next 16,
given slots, removed 0.2-2.4% in practice; the estimate's overlap overstates it. Two of the
three fastest fuse no pairs at all, the fastest 13: the evolution weighs them already. The
interpreted designs' dispatch-level levers are mostly in the genes now.

## The JIT designs - what the JIT leaves to the interpreter (next)

The speed frontier is the JIT's (0.13-0.15 of s6's time). The JIT translates a word only whole -
an operation without a stencil leaves the word interpreted - and kernel and corpus (compiling,
parsing, FIND) may run much of their time so. No tool counts it: **jitleft.py**, to build - a
JIT design with the profiler (as hotwords.py, the JIT on): the dispatches left are exactly what
the JIT did not translate; by word, and for each hot word the operation that kept it out. New
stencils for those operations are genes. And bfind's effect on the laptop's predictor (missmap,
a design with and without it) can be a chain's first measurement.

## What the JIT leaves to the interpreter (Iteration 339) - lab/evolve/jitleft.py

Seed 55's two fastest JIT designs (c549c0677c, c708e864b7) profiled with the JIT off and on, on this
VM. Both alike:

### c549c0677c

| workload | dispatches, JIT off | left by the JIT | left |
|---|---|---|---|
| kernel | 2,032,355 | 1,136,217 | 55.9% |
| fib | 59,245,391 | 9,767 | 0.0% |
| corpus | 3,714,212 | 3,703,940 | 99.7% |
| loop | 20,033,411 | 9,566 | 0.0% |
| bubble | 7,131,570 | 148,624 | 2.1% |
| ackermann | 17,557,699 | 17,136 | 0.1% |

What is left, by word (the mean share over the workloads), beside the word's share of the JIT-off work:

- (compiled at run time)    21.0% of what is left;  67.3% of the work, JIT off
- INTERPRET                 15.0% of what is left;   5.2% of the work, JIT off
- PARSE-WORD                 8.8% of what is left;   2.7% of the work, JIT off
- COLD                       7.5% of what is left;   0.0% of the work, JIT off
- ?STACK                     3.5% of what is left;   1.5% of the work, JIT off
- REFILL                     3.5% of what is left;   0.7% of the work, JIT off
- C,                         2.3% of what is left;   0.5% of the work, JIT off
- WORD                       2.1% of what is left;   1.1% of the work, JIT off
- HERE                       1.8% of what is left;   0.6% of the work, JIT off
- CMOVE>                     1.8% of what is left;   0.6% of the work, JIT off
- *                          1.8% of what is left;   0.2% of the work, JIT off
- SUPER-OP                   1.7% of what is left;   0.6% of the work, JIT off


**The reading**: fib, loop and ackermann are translated whole (0.0-0.1% left), bubble nearly
(2%); **kernel is 56% interpreted and corpus 99.7%**. The benchmarks' own words are compiled at run
time and translated (fib, loop) - so the corpus's run-time words, run once or a few times each, stay
under whatever makes the JIT translate. What carries the rest: the outer interpreter - INTERPRET
(15% of what is left), PARSE-WORD (8.8%), REFILL, WORD, ?STACK - and compiling words (C, HERE).

**Two genes to look for**: (1) the outer interpreter translatable - which operation in INTERPRET,
PARSE-WORD, WORD, REFILL has no stencil (next: the blockers, word by word); (2) when the JIT
translates code compiled at run time - its threshold, for compile-and-run-once work. With selection
at both widths, (1) counts twice: a JIT design's interpreter is its 32-bit speed.

## Next: why each word is left - a JITLOG build (planned, Iteration 339)

engine/jit.c's jit_body(w, a, end, depth) decodes a word into opl[] with each operation's address in
at[n] and refuses at its first untranslatable point - 17 `return 0`s; the commonest in the decode
loop: `if (L >= JIT_NOPS || !jit_ops[L].ok) return 0;` (an operation with no mapping), the later
ones in loops over i (jit_usable(s) refusals - a stencil read short, a branch it cannot place). The
plan, under -DJITLOG=1 only (a normal build's text the same - no 64-bit change): a static last-address
set to at[n] in the decode loop and at[i] in the later loops, and jit_body's caller writing
"R word address why" to a file named by an environment variable when it refuses; jitleft.py --why
building so, and naming each refused operation from the call map's O lines (address, kind, opcode,
name). Then the counts: which operations keep INTERPRET, PARSE-WORD, WORD, REFILL out - each a
stencil to write, a gene.

## Why each word is left - jitleft.py --why (Iteration 340)

engine/jit.c logs each refusal in a -DJITLOG=1 build only (a normal JIT engine byte-identical: c549c0677c,
112c1292f2df before and after); jitleft.py --why follows each word's refusal through refused callees to
the root. Seed 55's fastest JIT design, c549c0677c:

What is left, by word (the mean share over the workloads), beside the word's share of the JIT-off work:

- (compiled at run time)    21.0% of what is left;  67.3% of the work, JIT off
- INTERPRET                 15.0% of what is left;   5.2% of the work, JIT off; left: never tried
- PARSE-WORD                 8.8% of what is left;   2.7% of the work, JIT off; left: never tried
- COLD                       7.5% of what is left;   0.0% of the work, JIT off; left: never tried
- ?STACK                     3.5% of what is left;   1.5% of the work, JIT off; left: never tried
- REFILL                     3.5% of what is left;   0.7% of the work, JIT off; left: never tried
- C,                         2.3% of what is left;   0.5% of the work, JIT off; left: never tried
- WORD                       2.1% of what is left;   1.1% of the work, JIT off; left: no mapping for vf
- HERE                       1.8% of what is left;   0.6% of the work, JIT off; left: no mapping for vf
- CMOVE>                     1.8% of what is left;   0.6% of the work, JIT off; left: never tried
- *                          1.8% of what is left;   0.2% of the work, JIT off; left: no mapping for UM*
- SUPER-OP                   1.7% of what is left;   0.6% of the work, JIT off; left: never tried

The root operations, by the share of what is left behind them:

-  62.6%  never tried
-   5.1%  no mapping for vf
-   1.8%  no mapping for UM*
-   0.9%  no mapping for @4431
-   0.8%  no mapping for WRITE
-   0.5%  no mapping for vs
-   0.5%  no mapping for 0<?BRANCH8
-   0.3%  no mapping for SP@
-   0.3%  no mapping for DUP?BRANCH8
-   0.2%  no mapping for UM/MOD

**The reading.** 62.6% of what is left was **never tried**: INTERPRET, PARSE-WORD, COLD, ?STACK, REFILL,
C,, CMOVE> - the JIT translates a word on its first call through a JIT header, which the run-time
compiler gives the words it compiles, and a callee when translated code reaches it; the image's own
words have no header, and the outer interpreter is the top-level loop, never called from translated
code. Not a missing stencil: **not a candidate at all**. Then the operations with no mapping: vf (a
fused variable fetch: WORD, HERE - 5.1%), UM* (* - 1.8%), WRITE, vs (a fused variable store),
0<?BRANCH8, SP@, DUP?BRANCH8, UM/MOD.

**The genes**: (1) the image's words JIT candidates - translated on their first call as run-time words
are (or the outer interpreter and its callees at start) - the large lever; (2) stencils for vf, vs,
UM*, UM/MOD and the fused branches - small ones, each.
