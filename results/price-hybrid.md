# The hybrid stack/register design, priced again (Iteration 172)

The owner asked for it at Iteration 163; then only the stack shuffles were
measured (23-46% of dispatches, results/tracer.md). Iteration 32's price
(results/price-register-stage1.md) covered the image's code only - and four of
today's six selection workloads (fib, loop, bubble, ackermann) are compiled at
run time. This prices every executed dispatch, run-time code included, from
the profiler's dynamic opcode pairs (JIT off - for a JIT design the saving is
in the copied handlers, not in dispatches). The tool: results/drafts/
hybprice.py; the full tables: results/drafts/hybprice-iter172.txt.

**A measurement bug found on the way:** regprice.py's opcode names (Iteration
32) are computed from the primitive list's order, which has moved since (the
single SYSCALL, TABS>BL out, newer genes): on evolved designs it names opcodes
wrongly - a NOOP at 8% of loop's dispatches - while every opcode still gets a
name, so nothing looks unnamed. The converter writes each opcode's real name in
CALLMAP's O records; this price takes them from there. regprice.py needs the
same fix before it is used again.

| design | moves: the bound | a move feeding the next operation | return stack feeding one | unnamed |
|---|---|---|---|---|
| s6 | 17-27% | 0-12% (fib 0, loop 4.3, bubble 4.2) | 0-4% | 0-19% |
| 9932cc5c32, the fastest | 11-27% | 0-8% (fib, loop, bubble 0) | 0-3%, loop 20% | 0-30% |
| b40b6b7e2d, the smallest | 17-27% | 0-10% (fib 0, loop 4.2, bubble 5.8) | 0-4% | 0-20% |

Evolution has not taken the moves out: a fifth to a quarter of every design's
dispatches. The simplest absorbing form - a move feeding the next operation -
would save 4-12% on the image-heavy workloads (kernel, corpus, parse, sieve),
little on the run-time ones. That is the count's blind spot, not the
design's: in fib every move feeds a literal first (DUP 2 <, DUP 1 -, SWAP 2 -),
seen only by a triple, and the designs' immediate-operand opcodes are not yet
classified as uses. fib's moves alone are 23% of its dispatches.

**Next:** (1) the profiler's triples (a move, then any two) and every opcode
kind named - the price of operand-carrying forms with immediates, which is
what the selection's workloads need; (2) if that is 10% or more of the
selection's dispatches: the gene - forms in the converter, in the run-time
compiler (where fib, loop, bubble and ackermann are compiled), handlers in
the engines, the JIT copying them; (3) the laptop's measurement in the run
after seed 40's batch.

## With triples and every opcode named (Iteration 173)

The profiler now counts each opcode with the two before it (profiling builds
only - results/applied-after-seed40/triples-after-seed40.patch), and every
opcode kind takes its name from CALLMAP, immediates included. A move counts as
absorbed when the next operation uses it, when a literal stands between it and
a binary operation (DUP 2 <), or when a move does and a use follows; a literal
feeding a binary operation becomes an immediate. Collapsed runs (moves before a
call or a branch) are not counted - the price errs low, most on ackermann and
loop. Tables: results/drafts/hybprice3-iter173.txt.

| saved, of all dispatches | kernel | fib | corpus | loop | bubble | ackermann | selection mean | sieve | parse |
|---|---|---|---|---|---|---|---|---|---|
| s6 | 16.1% | 36.4% | 22.2% | 4.4% | 6.8% | 3.9% | 15.0% | 7.4% | 22.6% |
| 0ceb043115, seed 40's smallest | 12.8% | 36.4% | 20.5% | 4.2% | 8.3% | 3.9% | 14.4% | 5.9% | 20.9% |
| d9247d19b0, seed 40's fastest (JIT off) | 3.2% | 5.9% | 6.0% | 0.0% | 10.0% | 3.9% | 4.8% | 5.6% | 6.3% |

fib's moves all feed literals - the pairs saw none of it. The fastest's own
run-time compiler genes already make fib's literals immediates; it has less to
gain, and runs mostly JIT code. **Decision:** the gene is worth building for
the interpreted designs (over half the joint front; 14-15% of the selection's
dispatches, past the 10% set before measuring) - register forms with
immediates, in the converter and the run-time compiler, handlers in the
engines; the collapse form priced next, for ackermann and loop.

## Before building: what evolution could already have (Iteration 175)

Most of the price on the interpreted designs is what genes already offer:
run-time immediates (rtimm: `n +` an ADDI, `SWAP n +` a SWAP+I, in the code
the design's own compiler writes). Seed 40's smallest, 0ceb043115, carries
rtimm=1 - unexpressed: it waited on the pair-fusion overlay, itself waiting on
rtfuse and on pairs the design has no slots for - three mutations away, each
priced alone. So the first step is not new opcodes but **rtimm=2**: the
overlay for immediates without pairs (results/pending/rtimm2-after-seed41.patch;
on a design with pairs and rtfuse it is rtimm=1, one id).

On 0ceb043115: +662 bytes of image; fib -13.6% of its dispatches; kernel,
corpus, parse, sieve +0.4 to +1.1% (the fusing compiler's own cost, on what
they compile); loop, bubble, ackermann unchanged. Every one of seed 40's 218
front designs, rtimm=2 forced: expressed on all, all alive; the held-out
check on the two that ans-check's small front kept: 14 of 14 files as s6.
Evolution now weighs it in one mutation. Next, the hybrid's own forms on top:
`-` and `<` immediates and the keeping forms (DUP n <, DUP n -, SWAP n -) -
fib's price is 36%, rtimm=2 takes 13.6.

## The keeping forms (Iteration 176) - fib's price, met

DUP+I (DUP n +) and DUP<I (DUP n <): one dispatch each where fib's `DUP -1 +`
takes two with rtimm and `DUP 2 <` three - format-10 names, in the image (the
converter's peephole) and at run time (cv8t-fuse-imm.4's IMM+, now SWAP n +,
DUP n +, n + and DUP n <), JIT steps from existing stencils. First try: no
effect on fib - in a small design the forms landed behind the escape (two
dispatches each, and IMM-OPS holds one-byte codes only: escaped, the run-time
compiler had nothing to write). The tag-2 ranking puts them by image use and a
reference profile made before they existed; now they are pinned to one-byte
codes where IMM-OPS is, as the loop opcodes are for the loop tables.

| seed 40's smallest, 0ceb043115 | image | fib's dispatches |
|---|---|---|
| as recorded | 7,406 | 59.27 M |
| rtimm=2 | +662 | 51.20 M (-13.6%) |
| rtimm=2 and the keeping forms | +64 more | 37.74 M (-36.3% in all; the price: 36.4) |

The other workloads within 0.1%. What the run-time compiler writes, probed:
`DUP -1 +` -> DUP+I 255, `DUP 2 <` -> DUP<I 2, both right. All 218 of seed 40's
front designs with rtimm=2 and both forms: alive (rtimm=2 expressed on 171;
the 47 with pairs and rtfuse are rtimm=1). The held-out check: 14 of 14 files
as s6 on the two it took - ans-check keeps only its database's front, and
picked 2 of the 8 given (both JIT designs); the interpreted ones are not yet
checked by the suite - to do before the batch is applied.
results/pending/keepforms-after-seed41.patch, after rtimm2-after-seed41.patch.

## Iteration 178: checked, founded, and the tail

The held-out check on eight front designs with rtimm=2 and the keeping forms -
six interpreted, two JIT, chosen through a remeasure file beside the database
(ans-check checks what it lists): 14 of 14 files as s6 on all eight. A founder
for the run after seed 41 - seed 40's smallest with rtimm=2, DUP+I and DUP<I
(results/pending/founder-after-seed41.patch). regprice.py takes CALLMAP's names
now (regprice-names-after-seed41.patch); on s6's image code it saves corpus and
parse 20.3%, kernel 18.1%, bubble 15.9% - and shows the next target: return-stack
moves no form absorbs, 41% of loop's image dispatches, 30% of sieve's, 23% of
bubble's (results/drafts/regprice-iter178.txt).

## The loops, looked at (Iteration 179)

Seed 40's fastest, JIT off, on loop: five dispatches an iteration, 20% each -
DUP, I, +, XOR, (LOOP); I then + is a fifth of them, and I+ exists (Iteration
60) - behind rtloopall, rtiplus and I+ in ops10, as rtimm was behind pairs.
Seed 40's smallest on loop: NOOPs executed - 8.4% of the dispatches (NOOP NOOP,
NOOP then a call) - padding on the hot path. Careful: in a tag-2 profile the
escaped operations are logical 128 and up, which a quick naming takes for
calls; the next price names them.

## The padding that runs every iteration (Iteration 180)

forth/cv8t.4 (and cv8.4): `(LOOP)` and `(+LOOP)` read an inline cell operand,
kept cell-aligned, so OPERAND-ALIGN pads with NOOPs before the call. The
comment says the pad "executes once per loop" - true for ?DO8, whose pad is
before the loop; LOOP8's and +LOOP8's sit inside the body, before (LOOP)'s
call: they execute every iteration - 8.4% of seed 40's smallest's dispatches on
loop. Designs with the run-time loop compiler (rtloop: loop opcodes, no cell
operand) never pad; the smallest has seven loop opcodes and is one mutation
from rtloop (its rtloopall is dormant: it needs rtloop and (+LOOP) too) - the
overlay's bytes against the loops' speed, evolution's to weigh. A fix for the
designs without it, to price next: a wider call (tag 2's 3- and 4-byte forms)
absorbs up to two pad bytes; an unaligned-safe operand read (memcpy, one load
on x86-64) needs no pad at all - with ARM in mind.

## The padding, removed where it runs (Iteration 181)

Priced first: executed NOOPs on the eight workloads - s6 loop 4.3%, bubble
3.5%, sieve 5.6%; three interpreted front designs without a run-time loop
compiler (27 of seed 40's 218) loop 8.0-8.3%, bubble 3.3-3.4%, sieve 6.7-6.9%,
kernel and corpus under 1%. The loops that matter are compiled at run time,
so only the run-time compiler changes: cv8t.4's OPERAND-ALIGN pads only where
LOOP-ALIGN is set, and the converter sets it for JIT designs alone - (LOOP)'s
@ reads its operand unaligned, a plain load on x86-64 (CELL() is
*(UNS64*)); the converter's image layout, s6's cv8.4 and the ARM path are
untouched. Seed 40's smallest: loop 96.15 M -> 88.14 M dispatches (-8.3%),
bubble -3.4%, sieve -6.9%, no NOOP executed; alive. All 218 of seed 40's front
designs alive; the held-out suite on six interpreted designs as s6; run-tests
PASS; 7 of 7 stages identical. results/pending/loopalign-after-seed41.patch.

## The return stack, priced - and rtloop inert on a tag-2 design (Iteration 186)

On the founder configuration (seed 40's smallest, rtimm=2, the keeping forms;
JIT off), return-stack operations are loop 31.8% of the dispatches, bubble
18.8%, sieve 13.2%, kernel/corpus/parse 6-8%, fib and ackermann 0. The pairs
name the cause: a call then R> (loop 9.1%), DUP R@, R@ =, R> R> - the kernel's
colon-word loop runtime, (LOOP) beginning R> R> 1 + DUP R@ = ...

The remedy should have been rtloop (loop opcodes at run time), one mutation
from this design. Counterfactual: rtloop expressed, +582 bytes - and loop,
bubble, sieve unchanged to the dispatch (compile-heavy kernel, corpus, parse
+0.7-1.3%). Probed: `: T 10 0 DO I DROP LOOP ;` compiles LIT8 10, LIT8 0,
then tag-2 calls to (DO) and I, DROP, a call to (LOOP) and its operand byte -
calls to the colon words, not the opcodes, with rtloop's LOOP-OPS table in
the image and I an opcode of this design. **rtloop is inert here** - pure cost,
which may be why evolution declines it at the small end.

**Next, first:** why - the LOOP-OPS table's contents in a tag-2 image (zeros
for what the converter is not told about?), the converter's flag for rtloop
in tag 2, cv8-fuse-loop.4 (a cv8, not cv8t, overlay) under the tag-2
compiler; then how many of the front's rtloop designs are inert. Worth it:
loop's iteration from about 15 dispatches to 5 on the interpreted designs.

## Corrected: rtloop works; the founder lost the loop opcodes (Iteration 187)

Iteration 186's "rtloop inert on a tag-2 design" was wrong - an artifact of
testing it on the founder. In the running design with rtloop alone, LOOP-OPS
reads 0 12 0 0 13 and X10-OPS 14 15 0, and `: T 10 0 DO I DROP LOOP ;` compiles
I as opcode 14 and (LOOP) as opcode 12 with its 16-bit branch - only (DO),
unslotted in this design, stays a call (once a loop). The founder put DUP+I and
DUP<I first among format-10 names; this design has 10 slots (SWAP+I pinned
first), so they pushed out the last two: I and (LOOP). rtloop on the founder
had no loop opcode to use.

The founder's choice, measured (dispatches, JIT off; the forms taking the slots
of different pairs, every other name in place): displacing I and (LOOP) costs
kernel +0.9% and corpus +1.9% - the kernel's own loops; displacing +!/?DUP,
+!/CMOVE, ?DUP/UNLOOP or BRANCH8/?DUP costs more (kernel 5.53-6.18 M against
5.44, corpus 35.7-37.1 M against 34.1). The founder as built is the best of
these; fib's -36% is the same in all. results/drafts/founder-variants-iter187.txt.

What rtloop does on the recorded smallest (I and (LOOP) slotted): +568 bytes;
loop 88.14 M -> 20.09 M dispatches (-77%), bubble -13.5%, sieve -27.7%;
kernel, corpus, parse +0.2-1.4% (the compiler's own cost). About a quarter
fewer dispatches on the selection's geometric mean, for ~3% more bytes - and
the smallest lacks it because it is the front's size end: the trade-off doing
its work. The return stack's 32% on loop is the colon-word loop runtime, and
rtloop already takes it away. Worth pricing next: a cheaper rtloop - the
overlay's 568 bytes are what keep the small end from it.

## A cheaper rtloop, priced (Iteration 187)

rtloop's 568 bytes on seed 40's smallest, by word (CALLMAP): the overlay's 12
new words' bodies 326 - X10-OP 56, X10-XTS 48 (a five-cell table), COMPILE,8
43, ?DO8 30, RESOLVE-LEAVE16 29, LEAVE8 26, DO8 25, LOOP-OPS 16, X10-OPS 16,
CHAIN16? 16, RESOLVE-LEAVES 11, W@ 10; their headers about 160 (names and
links nothing reads at run time); the kernel's compile words, swapped to the
overlay's, +79. Two levers: the overlay-internal words headerless (~160 bytes,
for every overlay - fuse, imm, loop alike), and the I/J/UNLOOP lookup and the
16-bit leave chain simpler (~50-100). From 568 to roughly 320-370 - for the
small end, -77% of loop's dispatches at about half the bytes.

## Rerun on today's designs (Iteration 194) - regprice.py with CALLMAP's names

The first register stage priced again (lab/evolve/regprice.py: data-stack
moves absorbed into the operation after them, collapsed into one shuffle
where the stack must be real, lone literals made immediate) - on s6 and four
of seed 40's front designs built with the after-seed-41 batch's code. Shares
of the dispatches executed in the image's own code (code compiled at run time
- fib's words, the benchmarks' loops - has no CALLMAP and is not priced):

| design | kernel | corpus | parse | bubble | sieve | loop |
|---|---|---|---|---|---|---|
| s6 | 18.1% | 20.3% | 20.3% | 15.9% | 10.2% | 5.9% |
| 0ceb043115, the smallest (interpreted) | 19.8% | 25.4% | 25.6% | 17.7% | 10.2% | 5.9% |
| d99e3d9ed9, the small-end knee (JIT) | 11.5% | 11.2% | 11.3% | 15.9% | 10.2% | 5.9% |
| 528c2523c3, the Q-best (JIT) | 8.7% | 11.5% | 12.0% | 15.3%* | 11.0%* | 10.0%* |
| d9247d19b0, the fastest (JIT) | 7.2% | 10.1% | 10.9% | 19.5%* | 8.2%* | 8.3%* |

\* of 8-70 thousand image-code dispatches: the JIT compiled those loops.

What it says: the register forms' value is at the interpreted small end -
a fifth to a quarter of the image's dispatches there; half that on the JIT
designs, whose hot code no longer dispatches. The loop workload's 41% of
return-stack moves (s6, the smallest, the knee) is the kernel's colon-word
loop runtime - rtloop's ground (rtloop=2 now +460 bytes on the smallest), not
the register stage's. The largest absorbable patterns on the smallest, as
shares of each workload's image-code dispatches - the next keeping forms, as
DUP+I and DUP<I were:

- kernel: DUP | ?BRANCH:QBRS 4.6%, OVER | C@ 2.0%, DROP SWAP DROP | ?DUP 1.5%, DUP | C@ 1.3%, SWAP | C! 1.0%
- corpus: DUP | ?BRANCH:QBRS 4.8%, DROP SWAP DROP | ?DUP 3.6%, DUP | C@ 2.7%, OVER | C@ 1.6%, SWAP OVER | C@ 1.6%
- bubble: DUP ROT | + 4.2%, DUP | CELL+ 3.1%, DUP | @ 2.1%, SWAP | < 2.1%, SWAP OVER | ! 2.0%
