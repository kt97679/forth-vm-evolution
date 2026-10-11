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
