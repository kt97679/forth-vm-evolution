# Real Forth applications as held-out workloads - what exists, what runs (Iteration 466)

The owner (465-466): look for Forth application benchmarks to hold out beside sieve, check their licences, and see which
run on our Forth. Our six selection workloads (kernel, fib, corpus, loop, bubble, ackermann) and the held-out sieve are
small programs; the question is how the evolved designs fare on real ones.

## Why it matters

The application suite the Gforth authors measure on - **Appbench**: benchgc (a garbage collector), brainless and fcp
(two chess programs), cd16sim (a circuit simulator), EEMBC's CoreMark and lexex (a lexical-analyser generator) - behaves
unlike kernels. A 2026 paper that ran it beside 18 Shootout kernels (Izawa and Hakamada, "RPyForth: Exposing a
Call-Shared Data Stack to a Meta-Tracing JIT Compiler", arXiv 2609.23759) counted the difference: a 95th-percentile
data-stack depth of 14.5 cells against 4, and 22.7 word calls per 1,000 primitives against 0.004. Deep stacks and
frequent calls are exactly what our genes trade on (tos, jitk, the JIT's calls, jitinl), and none of our workloads but
kernel and corpus has them. The same paper's systems (VFX Forth, SwiftForth, gforth-fast, its own JIT) rank differently
on the two suites - the reason to hold applications out.

## What exists, and where

| suite | programs | where | reachable here |
|---|---|---|---|
| Appbench (Ertl and Paysan) | benchgc, brainless, fcp, cd16sim, CoreMark, lexex | complang.tuwien.ac.at/forth/appbench.zip | **no** - this machine reaches GitHub and package archives only |
| The Shootout's Forth programs (Bagley 2001) | 25 kernels: ackermann, ary, except, hash, hash2, heapsort, lists, matrix, methcall, nestedloop, objinst, random, sieve, spellcheck, strcat, sumcol, wc, ... | dada.perl.it/shootout (Calpini's mirror) | no |
| Gforth's own benchmarks | siev.fs, bubble.fs, matrix.fs, fib.fs (and fft-bench.fs, floating point) | the Gforth repository (github.com/forthy42/gforth; an older mirror, earl/gforth-mirror) | yes |

Licences: Gforth's files are under its GPL-3; Appbench's programs each carry their authors' terms (brainless is a
SourceForge project, fcp Ian Osgood's, CoreMark EEMBC's, lexex Gerry Jackson's) - to read in the zip once downloaded.
Until then **no copy of any of them goes into this repository**: a harness can fetch them, and the owner decides.

## What runs on our Forth - tried on the hand-made s6

Gforth's three integer benchmarks run **unchanged but for two shims**:
- **case**: our words are upper case and the programs are written in lower case (Gforth folds case); the source upper-
  cased, harmless for these programs;
- **a three-line prelude** for words our kernel lacks - `: NIP SWAP DROP ;`, `: CELL 1 CELLS ;`,
  `: .( [CHAR] ) PARSE TYPE ; IMMEDIATE`.

| program | result on s6 |
|---|---|
| siev.fs | runs to its end, 1.02 s here |
| bubble.fs | runs to its end, 1.21 s |
| matrix.fs | runs to its end, 0.31 s (200 x 200 integer matrices - new to us) |
| fib.fs | not as it is: its timing code uses [IF] and floating literals (we have fib already) |

A finding on the way: **our kernel has no NIP and no .(** - both CORE EXT. The corpus never needs them; real programs
do. Appbench's will want more of the same: [IF] [ELSE] [THEN], case folding, perhaps TUCK and others - a prelude, or the
words in the kernel (which changes the hand-made stages' images - validate would say so).

## Proposed (the owner's calls)

1. **Download Appbench on the laptop** (complang.tuwien.ac.at/forth/appbench.zip) and keep it outside the repository; I
   then write the prelude and harness it needs and report which programs run, with their licences.
2. **A held-out tier of applications**: heldout.py taking several programs, each with an output check (sieve as now;
   Gforth's matrix at once; Appbench's programs as they run), its ranking reported per program beside sieve's.
3. **NIP, .( and [IF] in the kernel or in a prelude** - a prelude touches nothing measured; the kernel route makes every
   design a little more standard and changes the images.
