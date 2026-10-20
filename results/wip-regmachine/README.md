# The register machine - work in progress (from Iteration 418)

**Kept apart.** Nothing in this directory runs. The laptop's runs use master's engine and evolver; the processing
routine applies results/pending/ only. The work's patches, when there are any, are written against master and the
pending batch, and reach a run only through the gates everything passes - engines-check, the corpus, the programs past
4 MB, validate, a rehearsal on real designs, dispatches measured - and the owner's approval, into a pending batch. A
directory, not a git branch: the handoff bundle carries master alone (tools/make-bundle.sh). Stopped half way, it costs
the runs nothing.

**Why.** The interpreted designs wait on the dispatch's taken jump (Iteration 301: the remedy is fewer dispatches). The
register machine was priced the largest prize (Iterations 29 and 32); re-priced on seed 60's front (410-411), 7-46% of
its dispatches only move a value or push a lone literal. The first stage planned then (results/price-register-stage1.md)
priced the image's own code - but the selection's programs are compiled at run time. This prices them as they run.

## The first pricing (Iteration 418, price-418.py, its output price-418.out)

Each design built with the profiler and the converter's opcode names; from the profiler's pairs and triples, shares of
the dispatches: *taken in* - a move or literal straight before an operation that consumes it, and the one before that
where it feeds it too, carried as operands; *control* - calls, EXIT, branches and loop words, which no operand form
removes. Deterministic counts, not timings.

| design (taken in / control) | kernel | fib | corpus | loop | bubble | ackermann | sieve |
|---|---|---|---|---|---|---|---|
| tag 2, seed 60's fastest interpreted (4ac602c8bd) | 6 / 39% | 0 / 50% | 13 / 32% | 40 / 20% | 0 / 40% | 0 / 67% | 10 / 31% |
| tag 2, 129e7a9271 | 10 / 35% | 0 / 50% | 13 / 32% | 40 / 20% | 0 / 40% | 0 / 67% | 10 / 31% |
| plain CV8, seed 58's smallest (09de03f091) | 23 / 22% | 36 / 32% | 26 / 18% | 25 / 17% | 23 / 25% | 0 / 54% | 17 / 26% |
| plain CV8, b966d06523 | 21 / 25% | 36 / 32% | 23 / 20% | 40 / 20% | 11 / 40% | 0 / 54% | 18 / 28% |

What is taken in, by name: on the tag nearly all of it is loop's `I +` and `DUP I +` (86%) - I+, which rtiplus fuses on
the tag since patch 11 - then `OVER +` 7%. On plain CV8 it is spread: the ten largest give 67% - `LIT8 <`, `DUP LIT8 <`,
`LIT32 +`, `DUP @`, `>R DUP @`, `R@ =`, `R> ADDI`, `DUP R@ =`, `R> R> ADDI`, `DUP LIT32 +`.

If time followed dispatches and operands cost nothing - an upper estimate - the six selection workloads' mean would be
about 11% faster for the tag-2 design (most of it loop's, now I+'s) and about 23% for the plain-CV8 one.

## What it says

1. **On the tag the stage adds little** beyond the fusions in place; fib and ackermann are calls and returns there
   (50-67% control) - the JIT's ground, not a register form's.
2. **On plain CV8 it has room** - a fifth to a third of most workloads' dispatches - spread over many patterns: a
   general operand form fits it better than more fused pairs, which bought about 1% on the tag
   (results/supers-knockout-seed58.md).
3. **Size is the risk.** Plain CV8 holds the small end, and every handler grows the engine: the stage has to be a gene,
   its forms few and general, so the search weighs its bytes against its speed.

## A first sketch (to be priced before built)

- **Forms**: for the binary operations that consume (+ - AND OR XOR = < > U< and @ C@), a variant carrying one
  descriptor byte - its two sources from the top three stack items, R@, I or an 8-bit literal, and the stack's net change.
  One opcode per operation, or one generic opcode with the operation in the descriptor - the second a dispatch inside a
  dispatch, to be priced.
- **Where compiled**: the run-time compiler's peephole - an overlay like cv8-fuse.4 keeping pending moves and literals
  in a small window, emitting them folded into the next operation, or as they were before a call, a branch or EXIT; the
  converter for the image's code (stage 1's plan).
- **A gene** (say regstage), on plain CV8 first; it subsumes rtimm's ADDI-style immediates where both are on.

## Next

1. Which descriptor set covers how much of the taken-in share, per workload, over seed 58's plain-CV8 front.
2. One form prototyped behind the gene - its handler's bytes, the dispatches it removes - in this directory as a patch.
3. General or targeted, decided on those numbers; then built, rehearsed and gated as above.

## Coverage (Iteration 419, coverage-419.py, its output coverage-419.out)

Eight plain-CV8 designs of seed 58's front, 14,146 to 20,977 bytes, every taken-in pattern classed by the operand sources
it needs, cumulative: A a literal; B and the top kept (a DUP before); C and the return stack (R@, R>); D and the loop
index (I, J); E and OVER and SWAP. Shares of all dispatches:

| workload | A | B | C | D | E | all taken in |
|---|---|---|---|---|---|---|
| kernel | 2-4% | 4-8% | 7-11% | 7-11% | 10-17% | 11-25% |
| fib | 10-18% | 15-32% | 15-32% | 15-32% | 20-36% | 20-36% |
| corpus | 1-9% | 4-16% | 8-18% | 8-18% | 13-22% | 15-27% |
| loop | 0 | 0-4% | 0-21% | 21-40% | 21-40% | 0-40% |
| bubble | 0 | 0-7% | 0-8% | 7-10% | 9-23% | 11-23% |
| ackermann | 0 | 0 | 0 | 0 | 0 | 0 |

Two operations take most of it in: `+` 42% and `<` 21% - then `@`, `C@`, `=`, `CELL+`, ADDI 3-4% each. So few forms would
do: `+` and `<` with a literal, a kept top or the loop index cover fib's and loop's share nearly whole.

## What exists already (Iteration 419, existing-419.py, its output existing-419.out)

Those forms are largely in the project: rtimm's immediates (ADDI, and DUP<I, DUP+I among the format-10 words), rtloop
and rtloopall's loop compiler with rtiplus's I+. The smallest design uses none of them - no run-time fuser at all. Its
run-time loop compiler turned on, nothing else changed: **loop's dispatches -79%, bubble's -62%, for 465 bytes**
(14,146 to 14,611); the larger b966d06523 already has it. (A first try put DUP<I and DUP+I ahead of the design's
format-10 words and pushed others out of their slots - kernel and corpus +4-13%: existing-419-first.out.)

## Where this leaves it

- **Loop and bubble are the loop compiler's**, already in reach: the search takes it on the larger plain designs and
  leaves it on the smallest for its bytes - the small end trades speed for size by definition, and a register stage
  would meet the same refusal there.
- **fib's share is the immediates'** (`DUP 2 <`, `-1 +`, `SWAP -2 +`): rtimm has the forms. (419 said it needed built
  pairs; wrong - Iteration 175 freed it already: rtimm=2, the immediates without pairs. Measured in 420, below.)
- **kernel's and corpus's** share is spread (11-27%), mostly the image's own code - stage 1's converter-side plan, which
  on today's tag-2 designs prices at 4-8%.

So a general register stage would add less than its first pricing suggested: what remains after the forms in place is
kernel's and corpus's spread share and fib's. Next: the immediates as they exist, measured on fib (420, below).

## The immediates, and what the forms in place cost (Iteration 420, existing-420.py, its output existing-420.out)

Seed 58's smallest design (14,146 bytes; it builds 9 of the 31 format-10 words it lists), each variant against it:

| variant | bytes | fib | loop | bubble | kernel | corpus |
|---|---|---|---|---|---|---|
| rtimm=2 - the immediates, no pairs (Iteration 175) | +608 | -13.6% | 0 | 0 | +0.7% | +0.9% |
| and DUP<I built, in CMOVE's place | +656 | -13.6% | 0 | 0 | +9.4% | +6.5% |
| and the loop compiler (rtloop) | +1,119 | -13.6% | -79.1% | -61.9% | +9.9% | +6.5% |
| the loop compiler alone | +465 | 0 | -79.1% | -62.0% | +0.5% | +0.1% |

fib's `-1 +` and `SWAP -2 +` fuse (ADDI, SWAP+I): -13.6%. DUP<I adds nothing to fib here, and a slot given up costs kernel
and corpus 6-9% - a slot is dear. The loop compiler takes loop and bubble down by two-thirds to four-fifths.

**What it says.** The gains a register stage was priced for are mostly there already, gene by gene - and they cost
bytes: 465 for the loop compiler, 608 for the immediates, 3-4% of the smallest design each. That, not their reach, is why
the small end goes without them; a register stage would cost bytes the same way. **The lever is the bytes**: a run-time
compiler that costs a hundred bytes instead of five or six hundred would be worth taking even at the small end.

## Where the bytes go (Iteration 421, bytes-421.py, its output bytes-421.out)

The engine does not grow in either case: the handlers are there already. Every byte is the image's - the overlay's words,
from the converter's map:

- **The immediates, rtimm=2: +608.** Nine words added - IMM+ 89 bytes, SUPER-TABLE 88, SMALL-LIT? 85, SUPER-OP 52,
  FOLD-TABLE 32, ?BRANCH, 26, IMM-OPS 16, LIT-PREV 16, FOLD-DEFAULTS 15 - and their headers about 106; COMPILE, and
  LITERAL grow 59. **The pair lookup, SUPER-TABLE and SUPER-OP, is 140 bytes of it, and with rtimm=2 there are no pairs.**
- **The loop compiler, rtloop=1: +465.** Twelve words - X10-OP 55, X10-XTS 48, COMPILE,8 32, RESOLVE-LEAVE16 27, ?DO8
  25, DO8 22, LEAVE8 22... - and headers about 125. Its cheaper form exists: **rtloop=2** (Iteration 190) builds the
  internal words headerless with the converter's switch - +361 on this design.
- **Names across the image**: on the smallest design the 322 words' names and links are about 2,679 bytes, 32% of the
  image. Hiding the internal ones was priced (-2.7 to -2.8%, Iterations 222-223) and deferred by the owner - reusable
  helpers keep their names (Iteration 227): only an overlay's own internal words may go, as rtloop=2 does.

## Next (as of 421)

1. **A cheaper rtimm=2**, as rtloop=2 is to rtloop: the overlay without the pair lookup when there are no pairs (-140),
   its internal words headerless (about -90) - 608 toward 380 bytes for fib's -13.6%. Prototyped here as a patch and
   measured against these rows.
2. The loop compiler past rtloop=2: X10-OP and X10-XTS look its opcodes up at run time (103 bytes); constants written by
   the converter, as LOOP-OPS is, might do.
3. A general register stage only if a later workload shows move-heavy code these do not reach.

## A cheaper rtimm=2 - built, as a patch here (Iteration 422, rtimm-lean-422.patch)

**What it is.** forth/cv8-imm.4: rtimm=2's forms - `n +` as ADDI n, `SWAP n +` as SWAP+I n - over the kernel's own
compiler, without cv8-fuse.4: no pair lookup, no copy of the fold table (the kernel folds at `;` itself). BEGIN clears
LAST-OP, as cv8-fuse.4's does, so no literal fuses across a loop's start; the kernel clears it at every branch
resolution. Its four internal words are built headerless. lab/evolve/evolve.py: a kernel variant `-lit`, chosen by
rtimm_lean(g) - rtimm=2 in a plain-CV8 design with nothing else for the fuser to do (no pairs, no fused tests). Tag-2
designs keep the full overlay. 68 lines added. No new gene value: the same forms, fewer bytes.

**Measured** (rtimm-lean-422-measure.py; the output rtimm-lean-422.out), seed 58's smallest design:

| variant | bytes | fib | loop | bubble | kernel | corpus |
|---|---|---|---|---|---|---|
| rtimm=2 as it is (420) | +608 | -13.6% | 0 | 0 | +0.7% | +0.9% |
| **rtimm=2 lean** | **+240** | -13.6% | 0 | 0 | +0.2% | +0.1% |
| rtimm=2 lean and rtloop=2 | +599 | -13.6% | -79.1% | -62.0% | +0.4% | -0.7% |

The same cut in fib for 61% fewer bytes; with the cheaper loop compiler, loop, bubble and fib for 599 bytes where the
two at their old cost were 1,119.

**Checked.** The corpus and kernel workload at both cell widths; run-time compiles of a literal before BEGIN, `n +`,
`SWAP n +`, a loop and a branch give the same numbers with and without the immediates, at both widths
(rtimm-lean-422-checks.py); every seed 58 and 60 front design with rtimm=2 rebuilt (rtimm-lean-422-front.py): 6, one
lean (-392 bytes against its record), five not (tag 2 or pairs) and byte-identical to their records, none failing;
run-tests PASS; validate: the hand-made stages IDENTICAL.

**Status.** A patch here, not in any batch: master's code is unchanged and the runs do not see it. It applies to master
as of Iteration 422 (`git apply`, then `LAYOUTS=1 bash tools/build-stages.sh`). To reach a run it would join a pending
batch with the owner's approval, rehearsed with the others there - once seed 62's batch is applied, rebased onto it.

## Next

1. The five front designs it leaves alone: tag 2 or pairs - a tag-2 version (cv8t-imm.4) if tag-2 designs carry rtimm=2
   with nothing else to fuse.
2. The loop compiler past rtloop=2: X10-OP and X10-XTS look its opcodes up at run time (103 bytes); constants written by
   the converter might do.
3. A general register stage only if a later workload shows move-heavy code these do not reach.
