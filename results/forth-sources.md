# Improving the Forth sources: kstack, ABORT", rewrites, other Forths (Iteration 116)

The owner: GP should improve the Forth sources too - start with a variant
gene (kstack, in Forth) and verified rewrites; collect other Forths to see
how they implement the same words.

## 1. kstack - and a correction to deep dive 2

Deep dive 2 put ?STACK and (ABORT") at 17.8% of parse's dispatches and
proposed a Forth ?STACK that calls (ABORT") only on failure. Built as the
overlay kstack.4 (an X8 swap: ?STACK8 into ?STACK), it made the fastest
design SLOWER - parse +3.5%. Its compiled ?STACK showed why: it already was

    SP@ vf SWAP - LIT8 RSHIFT  LIT SWAP U<  ?BRANCH8 ...

- the kernel input gene's own ?STACK8 (cv8b-kinput.4, Iteration 54):
`DEPTH 10000 U> IF -1 ABORT" Stack error" THEN`, one unsigned compare,
(ABORT") behind an IF - and the new overlay, loaded later, replaced it with
a worse body. The deep dive had read kernel.4's ?STACK, not the one that
runs; and (ABORT")'s 5.1% was not ?STACK's at all: per call site, on the
fastest design's parse, INTERPRET calls it 48,000 times (NUMBER? 0= ABORT"
Undefined word"), REFILL 12,021 (once a line), ?STACK never.

**kstack is now that body on its own** - for designs without kinput's C
code, never on top of it: on the smallest design (no kinput) parse and
corpus -0.7% of dispatches, kernel -0.2%, the image the same size, the
same message on an underflow.

## 2. The real fix: a guarded ABORT" - a source change, the owner's call

ABORT" compiles a call to (ABORT"), which runs even when its flag is false,
only to skip its inline message (R> COUNT + ALIGNED >R): ~6 dispatches at
every site, every time. Compiling `IF -1 (ABORT") <message> THEN` instead,
on the fastest design: parse -4.3% of dispatches (60,000 skipped calls),
corpus -2.3%, kernel -0.8%, for ~20 bytes; every ABORT" in user code too.
It needs the run-time ABORT" (kernel.4) and the cross-compiler's (cross.4,
for the kernel's own sites) - every image changes, so not done unasked.

## 3. Verified rewrites (level 2): priced, not worth building

Every run of 2-4 stack operations in the two images (116 and 203 runs),
each against the shortest sequence of stack words with the same effect on
both stacks (exhaustive, up to 3 words): 2-4 patterns have a shorter
equivalent (ROT ROT SWAP -> SWAP ROT, ...), at most 0.09% of the selected
workloads' dispatches. The kernel's stack code is tight, and the converter's
folds and superinstructions take the common pairs. The waste is in idioms
(ABORT" on the success path), not in local shuffles.

## 4. Other Forths

Fetched (ideas only from the GPL ones): pforth (0BSD-like), jonesforth and
the eForth of howerj/subleq (public domain), sectorforth and zForth (MIT),
lbForth and gforth (GPL). On the words this iteration is about:

| | ABORT" | the stack check |
|---|---|---|
| gforth | `if ... c(abort") then` - guarded | `sp@ sp0 @ u> IF -4 throw THEN` - one unsigned compare |
| lbForth | `if s" (abort") then` - guarded | `sp0 sp@ cell+ < abort" ..."` - underflow only |
| pforth | (ABORT") called every time, the message on the stack | - |
| ours | (ABORT") called every time, the message skipped through R> | kinput's: one unsigned compare, guarded |

Two mature Forths guard ABORT" at compile time - section 2's fix. A
systematic comparison of the hot words (INTERPRET, NUMBER?, PARSE, FIND)
across these sources is the next use of the collection: variants for genes
(level 1), material for genetic improvement (level 3).

## 5. The guarded ABORT" as a gene: `abortif` (Iteration 117)

The owner: a gene, not a change to every image. The converter
(tools/sod16.py guard_aborts, layout.py --guard-abort) puts every compiled
call to (ABORT") with its message behind `?BRANCH` to just past the message
and `-1` - before the fusers, which then fuse the ?BRANCH with its test, and
`-1` becomes the one-byte literal. Sites already guarded by hand (the kernel
input gene's ?STACK8) and words with a DOES> entry are left alone; every
branch the splice moves is moved back, as hot-site inlining does.

| design | image | kernel | parse | corpus |
|---|---|---|---|---|
| fastest, e5193642ef | +56 bytes | -1.0% | **-5.6%** | -3.0% |
| smallest, 585376cf49 | +72 bytes | -0.3% | -0.8% | -0.7% |

(Bytecode dispatches.) Errors unchanged: an undefined word still prints
"Undefined word", a tick of a missing name "Not found". Through the gate on
both; tests pass; hand-made stages identical. On the smallest design the
share is small because it does far more work a word without the kernel's
fast paths - the trade evolution weighs.
