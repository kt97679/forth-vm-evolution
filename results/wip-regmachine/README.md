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
- **fib's share is the immediates'** (`DUP 2 <`): rtimm has the forms, but needs the run-time fuser, which needs built
  pairs - a coupling, not a cost. Freeing rtimm from it is a small, testable change: the next step here.
- **kernel's and corpus's** share is spread (11-27%), mostly the image's own code - stage 1's converter-side plan, which
  on today's tag-2 designs prices at 4-8%.

So a general register stage would add less than its first pricing suggested: what remains after the forms in place is
kernel's and corpus's spread share and fib's. Proposed next: rtimm without its pair coupling, measured on fib, as a
patch here - before any new engine form.
