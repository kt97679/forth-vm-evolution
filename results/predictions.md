# Predictions, written before the runs

Each entry is written before the run it predicts and judged after it, by the
run's own pack - so a result can be told from an explanation found afterwards.

## Seed 39 - written at Iteration 154, while it runs

Seed 38's pair: the same genes and measurement, 7 hours (Iteration 153).

1. **Small again.** Against the best of seeds 35-38 in session 34, no
   objective's best moves past its threshold: speed within 2% (a tie on
   either CPU), binary + image within 2% (~20.6 KB), memory within the 8 KB
   tie (~152-156 KB).
2. **The front of all runs shared between 38 and 39**, the two runs adapted to
   the same workloads - neither below a third of it; the older seeds a handful.
3. **The fastest still not a JIT design** - nothing in seed 39 changes what kept
   seed 38's out (bubble and ackermann are bytecode on the JIT until jitloop and
   jitinl).
4. **The chain ends on time**: the evolution stops at its start + 7 h - 147 min,
   the chain within ~10 minutes of 7 hours; runs/phase-times holds this
   chain's own durations afterwards.

## The first run after the batch - written at Iteration 154

The seven pending patches applied (GOALS.md has the procedure). Rehearsed on
seed 38's whole front (165 designs, the batch's code): all alive, the tab
test right on all, 146 with new ids.

1. **No deaths beyond the reach limit** in the carried designs.
2. **Every design ~3.1 KB smaller** - median -3,148 bytes in the rehearsal; the
   smallest starts at ~17.6 KB (seed 38's 20,622 -> 17,594) and ends a little
   below.
3. **jitloop and jitinl spread from the founders** (Iteration 155, revised
   before the run: the eighth pending patch seeds them - seed 37's fastest with
   both, its bubble -98.5% and ackermann -99.9% of interpreted dispatches, and
   s6 with the JIT and both): most JIT designs on the front carry jitloop by the
   end, and many jitinl - with jitx, which it needs. Without the founders, jitinl
   was two mutations from 41 of seed 38's 47 JIT front designs.
4. **The fastest becomes a JIT design with jitloop**, bubble's ratio about
   halved; with jitinl too, ackermann's as well.
5. **Every speed number moves**: s6, the yardstick, does 36% fewer dispatches
   on the kernel workload and 31% on the corpus (NAME>BUF, the parsing), and
   designs that already had kfast and kinput gain less - their ratios rise.
   Speed and size are not to be compared across the batch; within the session
   that measures it, they are.

## Added before the post-batch run (Iteration 166)

6. **s6 itself is faster on lookup-heavy workloads** - lean (the batch's
   thirteenth patch): its dispatches parse -5.0 percent, corpus -2.2, kernel
   -0.9, the rest under 0.1. Speed is a ratio to s6, so on those workloads every
   design's ratio moves against it by about as much - on top of what the batch
   does to the designs themselves.

## Seed 39, checked (Iteration 168)

1. Small again - **right** (fastest 0.239 against 0.237, smallest and memory
   equal; the second small run in a row).
2. The front shared with seed 38 - **right**: 71 and 39 of the joint 119.
3. The fastest still not a JIT design - **wrong**: the joint front's fastest,
   9932cc5c32, is a JIT design, and so are 74 of the 119 - before jitloop and
   jitinl are even expressed.
4. The chain ends on time - **right**: 6 h 28 min of 7 hours.

## Added at Iteration 169, before seed 40 (9 hours)

1. Every design's image grows by ~100-150 bytes (the standard's numbers,
   CREATE-FILE): the smallest binary + image of the session moves up by about
   that much from 20,622 - for the carried designs as for the new.
2. The chain ends within its 9 hours (the reserve from seed 39's times; the
   comparison has one workload more, far).
3. The far workload: every design on the joint front answers it (the gate
   refuses any that does not).

## Seed 40, the batch's first run, checked (Iteration 173)

From Iteration 154: (1) no deaths beyond the reach limit among the carried
designs - **right** (none died; 5 new designs died with a wrong corpus);
(2) ~3.1 KB smaller, the smallest from ~17.6 KB ending a little below -
**right** (17,770 carried, 17,762 at the end - with the later ~170 bytes);
(3) jitloop and jitinl spread from the founders - **right** (all 42 JIT
designs on the joint front carry jitloop, 34 jitinl); (4) the fastest a JIT
design with jitloop, bubble's ratio about halved, ackermann's too with jitinl
- **right, and more**: bubble 24%, ackermann 58% of the best carried; (5)
every speed moves, carried ratios rise - **right** (seed 38's fastest 0.237
-> 0.280, seed 39's 0.239 -> 0.299). From 166: (6) s6 faster on lookup -
consistent, not separable. From 169: (1) images +100-150 bytes - **roughly**
(~170); (2) within 9 hours - **right** (8 h 39 min); (3) far answered by the
whole joint front - **right** (97 of 97).

## Seed 41, predicted (Iteration 174)

1. Every image ~170 bytes larger (the exception wordset): the session's
   smallest binary + image starts near 17,930, carried designs too.
2. Small against seed 40 in its session: the fastest within 5% - the JIT genes
   have spread already.
3. The held-out check: no front design differs from s6.
4. The chain ends within its 9 hours.
5. A few corpus deaths again (10 or fewer), every one with opcall.

## Added at Iteration 183, for the run after seed 41's batch

1. dskew (the stacks' page offsets apart) neutral on the laptop's AMD core:
   on the joint front no more often than mutation alone would put it - if it
   is enriched there, the skew is worth something after all.

## Seed 41, scored (Iteration 198)

1. The session's smallest near 17,930 bytes: 17,938 (f0aeaeb237). Yes.
2. Small against seed 40, the fastest within 5%: +1.6%, and small by all five
   measures. Yes.
3. No front design differs from s6: 0 of 12 sampled, with the after-seed-41
   batch's code (2,119 tests). Yes, on the sample.
4. The chain within its time (6 hours since Iteration 177): 14:45 to 20:54 with
   the comparison. Yes.
5. Ten or fewer corpus deaths, every one with opcall: 12, every one opcall 1+.
   Half - the count was over, the cause right (fixed in the batch since).

## Seed 42, predicted (Iteration 198) - the after-seed-41 batch's first run

1. No corpus death with opcall (the padding between X;CALL and its call is
   fixed), and opcall's X;CALLs outside the base band on the front.
2. Short branches out of range again, about as often as seed 41's 37 in 18,213
   (0.2%) - not fixed yet.
3. Crossover makes about a quarter of the children; mutation-only children
   still most of the final front.
4. Among front designs with rtloop, rtloop=2 more often than rtloop=1 (the
   same loops, 96-108 bytes smaller).
5. regpin on the joint front, if at all, at the fast end (JIT designs), not
   the small end.
6. At least one front design made "via the attic".
7. Not small: hypervolume +2% or more - the forms and run-time immediates
   (fib 0.83 on the knee founder) are new trade-offs at the knee.

## Seed 42, scored (Iteration 209)

1. No corpus death with opcall: none at all. Yes.
2. Short branches out of range about as often as seed 41's 0.2%: 35 of 15,352
   (0.23%). Yes - fixed in the after-seed-42 batch since.
3. Crossover a quarter of the children: 33% of those recorded (children
   repeating a genome already measured are made again, and those are mostly
   mutation-only ones); mutation-only children most of the final front: 98 of
   the 133 made in the run. Half.
4. rtloop=2 more often than rtloop=1 on the front: 56 against 66 (the carried
   fronts could only have 1). No.
5. regpin at the fast end if at all: 19 designs, all 0.179-0.187. Yes.
6. At least one front design via the attic: 8. Yes.
7. Not small, hypervolume +2% or more: +4.8%. Yes.

## Seed 43, predicted (Iteration 209) - the after-seed-42 batch's first run

1. No death from a short branch out of range (now converted again).
2. The screen skips about a third of the children from generation 5 on, and
   the run makes more designs an hour than seed 42's (3,000 an hour over its
   5 h 06 min) - 9 hours now (Iteration 210), so per hour; of the audited
   (measured though screened) none on the final front.
3. threads: 64 or 128 chains on most of the front's designs without klookup -
   the corpus 28-41% fewer dispatches - and 16 chains, if anywhere, at the
   smallest end.
4. fsys: 2 to 4 at the small end (600-1,200 bytes), 0 at the fast end (the
   I/O workloads 16-27% slower at 3 and 4 there).
5. Not small: hypervolume +2% or more.

## Seed 43, scored (Iteration 215)

1. No death from a short branch out of range - **right**: 182 deaths, every one
   "reach limit at scale 0 - not run".
2. The screen skips about a third from generation 5 - **wrong**: 18.4% (6,839
   of 37,088). More designs an hour than seed 42's 3,000 - **right**: 5,667
   made (4,668 measured) over 6 h 51 min. None of the audited on the final
   front - **right** (805 audited, 0 there).
3. threads 64 or 128 on most designs without klookup - **wrong**: never 64 or
   128 anywhere; 16 chains on 83 of the 90 without klookup and on 121 of all
   165 - 128 bytes fewer won over the lookup's dispatches. "16, if anywhere, at
   the smallest end" - wrong too: 48 of the small third, 29 of the fast third.
4. fsys 2-4 at the small end - **right** (the small third: 3 on 44, 4 on 4, 2 on
   7); 0 at the fast end - **wrong**: fsys 2 on 49 of the fast third's 55 - it
   moves only the file words into Forth, so the fast designs pay nothing for
   its ~1,000 bytes. (fsys 4 ran as fsys 3 with dead bytes in this run.)
5. Not small, hypervolume +2% or more - **right**: +22.4% (smallest +12.26%,
   best Q +9.3%, fastest -1.9%).

## Seed 44, predicted (Iteration 215) - the after-seed-43 batch's first run

The batch: --rebind takes the newest redefinition (fsys 4 buffered for real,
INCLUDED with the forgetting wrappers), fsys 5 (READ-LINE reading ahead where
a file seeks; tightened, Iteration 214), the dump guard.

1. fsys 4 on 10 or more of the front (seed 43: 4, unbuffered then) - at the
   small and middle ends, where fsys 3's unbuffered output costs the corpus.
2. fsys 5 on at least 3 designs, none in the smallest tenth (it is ~600 bytes
   over fsys 4).
3. fsys 2 on most of the fast third still; threads 16 on two thirds or more of
   the front.
4. The crossover share 30-33% again (XOVER 0.25 and remade repeats).
5. Not small: hypervolume +2% or more, from the small and middle ends' I/O;
   fastest under 5%.

Iteration 216: 6 hours, not 9 (the owner) - about 4 hours of evolution
against seed 43's 6 h 51 min. The predictions above stand as written.

**Seed 44, scored (Iteration 230): 3 of 5.** (1) fsys 4 on 10 or more - wrong:
3; fsys 5 took that place (15). (2) fsys 5 on at least 3, none in the smallest
tenth - right: 15, from 17,769 bytes; the smallest tenth all fsys 3. (3) fsys 2
on most of the fast third (32 of 40) and threads 16 on two thirds or more (85
of 120, 71%) - right. (4) Crossover 30-33% - right: 32.2%. (5) Not small -
wrong: small (hypervolume +0.9%); the fastest under 5% held (-0.6%).

## Seed 45, predicted (Iteration 230) - the after-seed-44 batch's first run

The batch has no new gene: native WRITE-LINE gives back the read-ahead, the
file buffers' slots apart (24-36 KB less memory with 4 KB buffers), READ's
FS-SEEK0 gone, the loader's 32 KB local static (32 KB less on every run), a
zero divisor -10 THROW (+96 to +192 engine bytes, +64 image).

1. Memory on every front design 16-60 KB lower than seed 44 recorded; the
   comparison measures all runs on the new code, so no run gains by it.
2. fbuf 0 (4 KB buffers) on more of the native-file designs than fbuf 1 -
   seed 44 had 23 against 49; the memory reason for small buffers is gone.
3. fsys 5 on 10 or more again, the smallest tenth still fsys 3.
4. Small - the second in a row (no new gene to find): hypervolume under 2%,
   fastest under 5%, smallest under 2%; by the rule, the evolution stops after
   it until new genes exist.
5. Crossover 30-36%.

**Seed 45, scored (Iteration 240): 4 of 5.** (1) Memory 16-60 KB lower than
seed 44 recorded, no run gaining by it - right: the front 124-188 KB against
160-224, memory +4 KB in the comparison. (2) fbuf 0 on more than fbuf 1 - right:
46 against 14. (3) fsys 5 on 10 or more, the smallest tenth fsys 3 - right: 11,
all fsys 3. (4) Small, the second in a row - wrong: hypervolume +6.2%, the
memory landscape moved. (5) Crossover 30-36% - right: 31.5%.

## Seed 46, predicted (Iteration 240) - the after-seed-45 batch's first run

The batch: native terminal output unbuffered, the SPN stages' -10 THROW, UTF-8
names in byte and cell headers (a reseed), the dispatch table as offsets
(384-448 bytes off every engine), and a new gene, jitos (the JIT's translator
-Os, 416-800 bytes off JIT engines built -O2/-O3).

1. jitos on half or more of the front's JIT designs not built -Os.
2. Every design 380-450 bytes smaller than seed 45 recorded (the offsets); the
   comparison measures all runs on the new code, so no run gains by that alone.
3. The fast third still all JIT with fsys 2; fbuf 0 on most native-file designs.
4. Small (hypervolume under 2%): jitos moves the JIT end by ~2% of size at most,
   and the memory landscape has been explored by seed 45.
5. Crossover 30-35%.

Iteration 241: 10 hours, not 6 (the owner) - about 8 hours of evolution
against seed 45's 3 h 51 min. The predictions above stand as written.

## Seed 46, scored (Iteration 248)

1. jitos on half or more of the front's JIT designs not built -Os - **wrong**:
   on none of the 45; 33 designs with it lived, none reached the front. The
   translator's -Os costs translation time on every word the JIT meets, and
   400-800 bytes do not buy that back at the fast end.
2. Every design 380-450 bytes smaller than seed 45 recorded - **right**: the
   smallest 15,872 against 16,296 (-424).
3. The fast third all JIT with fsys 2; fbuf 0 on most - **right**: the fast
   third all fsys 2, the JIT on 45 of the front; 4 KB buffers on 66 of 127.
4. Small - **wrong**: hypervolume +6.4%. With 8 h 10 min of evolution (seed
   45: 3 h 51 min) the middle filled in - fsys 5 on 17 of the front (seed 45:
   11).
5. Crossover 30-35% - **right**: 33.7%.

Three of five. Not predicted, and the run's real news: every tail design died
("engine did not compile" - the dispatch offsets broke gen-tail.py's engines),
so seed 46 ran without the gene tail.

## Seed 47, predicted (Iteration 248) - the after-seed-46 batch's first run

The batch: primitives first and PRIMITIVE? by address, the classic header
layout back, bit 7 of the count byte free, POSTPONE deciding immediacy when it
compiles, >NAME to coreext.4 (a reseed; images 64-136 bytes smaller); the gene
jittail (JIT tail calls as jumps: ackermann -16%, +256 engine bytes); the tail
engines compiling again. Six hours (the owner).

1. tail back on the front: at least one design with it.
2. jittail on a third or more of the front's JIT designs.
3. The smallest at least 60 bytes under seed 46's 15,872.
4. Not small: hypervolume above 2% - jittail moves the fast end, tail the
   middle.
5. Crossover 30-37%.

## Seed 47, scored (Iteration 269)

1. tail back on the front - **wrong**: 626 designs with tail lived (the engines
   compile again), none reached the front.
2. jittail on a third or more of the front's JIT designs - **right**: 27 of 44.
3. The smallest at least 60 bytes under seed 46's 15,872 - **right**: 15,808
   (-64), the batch's smaller images.
4. Not small, hypervolume above 2% - **wrong**: small, +1.4%. Four hours of
   evolution (seed 46: eight) and one new gene that moves the fast end only.
5. Crossover 30-37% - **right**: 32.3% (the last fifth 35.4%).

Three of five.

## Seed 48, predicted (Iteration 269) - the after-seed-47 batch's first run

The batch: a fault handler in every engine without guard (+128-160 engine
bytes), mostly repaid by memcmp and the variadic open leaving the engine (the
smallest +56 net); the genes jitk (the JIT's stack cache), lto and gotodup (build
options), compiler (GCC or clang 18 - offered where clang is installed) and
factor (repeated code in headerless bodies, 0-3). No kernel change. Six hours.

1. factor at 1 or more on at least half of the small third: level 1 is about 50
   image bytes for +0.007% dispatches.
2. The smallest at least 30 bytes under seed 47's 15,808: factor (-41 to -127
   image bytes) and lto (-32 or more) against the fault handler's net +56.
3. lto on most of the front's GCC-built designs.
4. compiler=1 (clang) on under a quarter of the front, and on none of the small
   third: clang's engines are larger at the small end.
5. Not small: hypervolume above 2% - five new genes.

## Seed 49, predicted (Iteration 286) - written before seed 48's results were seen

Seed 49 starts before seed 48's packs are processed, so these are written without
them - seed 48's own predictions wait to be scored. The same genes as seed 48 (jitk,
lto, gotodup, compiler, factor - their first run was 48), for 8 hours.

1. Small: hypervolume under 2% - the second run of a gene set, and no new gene.
2. factor at 1 or more on at least half of the small third.
3. lto on most of the front's GCC-built designs.
4. Crossover 30-37%, as every run since seed 44.

## Seed 49, scored (Iteration 288)

1. Small, hypervolume under 2% - **wrong**: not small, +4.0%. The gene set's second
   run still found the fast end: 0.128 in the run, the best Q 0.204.
2. factor at 1 or more on at least half of the small third - **right**: 56 of 57,
   and at level 3 (every word) on 46 of them.
3. lto on most of the front's GCC-built designs - **right**: 111 of 154.
4. Crossover 30-37% - **right**: 33.1% (the last fifth 36.5%).

Three of four. Seed 48's predictions are still unscored: its packs have not come.

## Seed 50, predicted (Iteration 288)

Twelve hours (the owner), the same genes as seeds 48 and 49 - the third run of the
set.

1. Not small: hypervolume above 2% - the set still yielded 4.0% in six hours.
2. factor at 3 on most of the front (96 of 172 in seed 49).
3. compiler=1 (clang) on under a quarter of the front (18 of 172).
4. The smallest at least 30 bytes under seed 49's 15,672.
5. Crossover 30-37%.

## Seed 50, scored (Iteration 296)

1. Not small, hypervolume above 2% - **wrong**: small, +0.4%; the gene set's third run.
2. factor at 3 on most of the front - **right**: 121 of 187.
3. compiler=1 (clang) on under a quarter - **right**: 28 of 187.
4. The smallest at least 30 bytes under seed 49's 15,672 - **wrong**: 15,647, 25 under.
5. Crossover 30-37% - **right**: 35.2%.

Three of five.

## Seed 51, predicted (Iteration 296)

Twelve hours (the owner), the first run with the after-seed-50 batch: 2@ and 2! in the
format-10 pool, opinline, tailpn, knumber.

1. Not small: new genes.
2. knumber on at least half of the front's klookup designs.
3. opinline on at least a quarter of the front.
4. A tail engine on the front again, with tailpn - none on seeds 49 and 50's.
5. 2@ or 2! among the format-10 words of at least a quarter of the front's designs
   without the JIT.
6. Crossover 30-37%.

(Iteration 297: seed 51 runs 10 hours, the owner's change after these were written; they stand.)

## Seed 51, scored (Iteration 300)

1. Not small: new genes - **wrong**: small, though the fastest moved +4.9%, just under
   its 5%.
2. knumber on at least half of the front's klookup designs - **wrong**: 8 of 69. Put
   first, it pushes a word out of a full list; mostly not worth it.
3. opinline on at least a quarter of the front - **right**: 64 of 162.
4. A tail engine on the front again, with tailpn - **wrong**: none.
5. 2@ or 2! on a quarter of the designs without the JIT - **wrong**: 8 of 69. The JIT
   designs took 2@ - five of the six fastest.
6. Crossover 30-37% - **right**: 34.6%.

Two of six: every miss on how widely a new gene would be taken. The slots of a full
format-10 list are the price an interpreted design pays for a new opcode.

## Seed 52, predicted (Iteration 300)

The after-seed-51 batch: alignhot; > and 0= as opcodes.

1. Small: alignhot reaches few designs (20 of seed 50's 187 could take it), and > and 0=
   compete for the same slots 2@ did.
2. alignhot on fewer than 10 of the front.
3. > or 0= expressed on at least 10 of the front - the JIT designs, as with 2@.
4. opinline on at least a third of the front (64 of 162 in seed 51).
5. Crossover 30-38%.

(Iteration 301: seed 52 runs 6 hours, the owner's, not the 10 these were written for; they stand.)

## Seed 52, scored (Iteration 310)

1. Small - **right**: hypervolume +0.5%.
2. alignhot on fewer than 10 of the front - **right**: on none.
3. > or 0= expressed on at least 10 of the front - **wrong**: > on 3, 0= on none.
4. opinline on at least a third of the front - **right**: 70 of 164.
5. Crossover 30-38% - **right**: 31.9%.

Four of five. The new opcodes again taken by few; alignhot by none - as the counters said,
the front end waits on the dispatch itself, not on where code is aligned.

## Seed 53, predicted (Iteration 310)

The same genes as seed 52, a second time - no batch between.

1. Small - and with seed 52's, two small runs in a row: the stopping rule's end of this gene
   set.
2. alignhot still on none of the front.
3. 2@ on at least 77 of the front again (77 in seed 52).
4. Held out: Spearman with sieve between 0.92 and 0.95.
5. Crossover 30-38%.

## Seed 53, predicted again (Iteration 318)

The Iteration 310 predictions assumed the same genes a second time; the after-seed-52 batch is
applied since - the JIT fix and the gene bfind - and the remote checks run alongside. These
replace them:

1. No design dies on the corpus (seed 52: 2 - the JIT fault, fixed).
2. bfind on at least 20 of the front - of ~130 that can express it.
3. Small: hypervolume within +2%.
4. The remote checks: dream.lan's ranking of the sample against the laptop's, Spearman at least
   0.90 (the same binaries, another x86-64); rage.lan's lower than dream's (another
   architecture, its own builds, no JIT).
5. Crossover 30-38%.

## Seed 53, scored (Iteration 320)

1. No corpus deaths - **right**: none (27 refused before running).
2. bfind on at least 20 of the front - **wrong**: 17 of 172, after an evolution of 80 minutes.
3. Small, hypervolume within +2% - **right**: +0.3%.
4. dream's Spearman at least 0.90, rage's lower - **half**: dream 0.959; rage no data (its
   build-stages.sh failed: a stage with sysc).
5. Crossover 30-38% - **right**: 31.3%.

Three right, one wrong, one half.

## Seed 54, predicted (Iteration 320)

The same genes as seed 53 - 9 hours, the owner's (Iteration 321), the comparison at 6 rounds.

1. Small - with seed 53's, two small in a row: the stopping rule's end of this gene set.
2. bfind on more of the front than seed 53's 17 - seven hours of evolution, not 80 minutes.
3. No corpus deaths.
4. dream's Spearman, if it runs again, between 0.93 and 0.98.
5. Crossover 30-38%.

## Seed 54, scored (Iteration 333)

1. Small - **right**: +1.1%; with seed 53's, two small in a row.
2. bfind on more of the front than 17 - **right**: 67 of 195.
3. No corpus deaths - **right** (one converter death, a new kind - results/drafts/convert-align-death.md).
4. dream's Spearman between 0.93 and 0.98 - **right**: 0.941.
5. Crossover 30-38% - **right**: 34.4%.

Five of five.

## Seed 55, predicted (Iteration 333)

The same genes a third time - the stopping rule's end of them, run all the same for the checks: the
first with dream.lan's 32-bit x86 check and the Tegra back (the after-seed-54 batch), 6 hours.

1. Small.
2. bfind on at least 60 of the front.
3. dream.lan 64-bit: Spearman 0.92-0.98.
4. dream.lan 32-bit x86: Spearman with the laptop below dream's 64-bit one - skew toward 64-bit.
5. The Tegra: at least 6 of its 12 designs measured, its Spearman below the 32-bit x86 one's.

## Seed 55, scored (Iteration 334)

1. Small - **right**: +0.4%; the third small run of these genes.
2. bfind on at least 60 of the front - **right**: 80 of 168.
3. dream.lan 64-bit Spearman 0.92-0.98 - **right**: 0.940.
4. dream.lan 32-bit x86 Spearman below the 64-bit one's - **right**: 0.694 - by far.
5. The Tegra: at least 6 of 12 measured - **wrong**: its build-stages.sh failed (four engines unported).

Four of five.

## Seeds 56 and 57: none written

Seed 56's processing (Iteration 354) wrote no predictions for seed 57, and none were written for seed
56 itself - step 4 of the routine skipped twice; noticed at Iteration 378, too late to predict either
honestly. Seed 58's are written before it starts.

## Seed 58, predicted (Iteration 378)

The anchoring and constraint test (HANDOFF 4c): 12 hours from scratch (nocarry: the hand-made designs
and founders) without the tag2 requirement every run since Iteration 71 has had, selected at both
widths; the after-seed-57 batch applied (non-PIE 32-bit engines, superinstruction pairs named right).
Its remote checks measure seed 57's front - and, first, designs seed 57 rejected (xcheck --rejected).

1. Its fastest at 64 bits 3-15% behind the carried runs' best (seed 57's 0.128): from scratch, as seed
   36 ended 12% behind after 2 h 40 min.
2. The search chooses tag2 itself on at least 60% of its front.
3. But not everywhere: at least 10% of the front plain CV8 (tag2 off), and its fastest at 32 bits one
   of them - tag2 costs 36% at 32 bits (results/drafts/skew-32.md).
4. Its fastest at 32 bits within 10% of seed 57's 0.337, either side.
5. The Tegra's rejected designs (4 of 16, from seed 57): none faster there than the fastest front
   design sampled - the rank agreement (0.944) holding for designs the laptop rejected.


## Seed 58, scored (Iteration 384)

The anchoring and constraint test: nocarry, no tag2 requirement, both widths (results/evolve-amd-ryzen-7-pro-8840hs-seed58.md). **4 of 5 as written.**

1. **Met.** Its fastest at 64 bits 3.4% behind the others' best in the same session (52917e2595, 0.131) - inside 3-15%, and far nearer than seed 36's 12% after 2 h 40 min.
2. **Missed.** Tag-2 on **43%** of its front (74 of 171), not 60%. The miss is the finding: tag-2 takes the fast end (53 of the fastest 57), plain CV8 the whole small third (57 of 57).
3. **Met**, widely: plain CV8 on 57% of the front (predicted at least 10%), and the fastest at 32 bits plain (d55f05136f).
4. **Met as written, not like for like.** 0.310 against seed 57's recorded 0.337 - 8% faster, inside the band; but in the same session seed 57's best measured 0.377, so the run is 21.5% ahead - outside what the prediction meant.
5. **Met.** No rejected design of seed 57's faster on the Tegra than the front's fastest (3 measured, 0 past it, 2 past the median); the rank agreement 0.973 (seed 56's front: 0.881).

Not predicted, and the run's main result: **it passed every carried run at the small end** (14,146 bytes against 15,633: +10.5%), **in hypervolume (+11.1%) and at 32 bits (+21.5%)**, all three by plain-CV8 designs - territory the requirement kept the carried runs out of. The predictions expected a from-scratch run to trail; it trailed only at the 64-bit fast end (-3.4%) and on best Q (-5.3%).

## Seed 59, predicted (Iteration 384) - the anchoring test, separated

`seed 59 tag2 12h widths nocarry`: from scratch as seed 58, but with the tag-2 requirement - the anchoring test as first specified (Iteration 373). Against seed 58 it isolates the constraint; against the carried runs (seeds 53-57, all tag-2) it isolates anchoring. The first chain on Iteration 379's remote path, with Iteration 381's probes.

1. By the five 64-bit measures against all the others, small (fastest within 5%, smallest and hypervolume under 2%). Reworded at Iteration 386 (results/review-methodology-386.md): read as "no evidence of anchoring at this search budget", not "not anchored" - a fresh run finding nothing shows little - and weaker still because nocarry keeps two evolved founders, about two thirds of seed 58's ancestry. If it passes the carried tag-2 runs somewhere by more than 2%, that is evidence of anchoring.
2. Its smallest about the carried tag-2 runs' (15,633 bytes, within 3%) - at least 7% larger than seed 58's plain-CV8 14,146: seed 58's small end was the encoding's, not the fresh start's.
3. Its fastest at 32 bits at least 15% behind seed 58's 0.310 (a tag-2 design at 32 bits; seed 57's best 0.377 in seed 58's session) - so not small at both widths only if this is wrong.
4. No `L_t2call4` deaths: the requirement holds bytehdr on (require() sets tag2=1, bytehdr=1), and both of seed 58's were tag-2 designs with bytehdr=0.
5. The run starts within 20 minutes of the remote checks' start (the sampling alone; seed 58 waited 55 minutes, seed 57 52), and every host's report ends with the probes' lines - the copy timed with its bytes, the connection, the load; the Tegra's copy again a few KB/s unless the network changed.

## Seed 60, predicted (Iteration 389) - the anchoring test, clean

`seed 60 tag2 12h widths noevolved`: from the hand-made designs and the founders built from them, no design from
an earlier run's record (the review, results/review-methodology-386.md, section 1), the tag-2 requirement, both
widths; the after-seed-59 batch applied; judged in a session whose verdict reads both CPUs (the owner, 389).
Read by section 3c of the review: a gain anywhere is evidence of anchoring; none is no evidence at this budget.

1. Its fastest at 64 bits 5-15% behind the best of the others in its session - it starts at 0.81 of s6 (the s6 +
   JIT founder), where seed 58 started at 0.174 from seed 37's design; seed 36, fresh before those founders
   existed, ended 12% behind after 2 h 40 min.
2. Its smallest within 3% of the carried tag-2 runs' (15,633 bytes), and at least 7% above seed 58's plain-CV8
   14,146: the requirement keeps it from the plain small end.
3. Its fastest at 32 bits at least 15% behind seed 58's 0.310 in the same session - a tag-2 interpreter.
4. Small at both widths, read from both CPUs: no gain beyond the bars - so no evidence of anchoring at 12 hours.
   A gain past a bar (hypervolume or best Q beyond 2%, or the fastest beyond 5%) would be evidence of it.
5. The same structure from a different lineage: bss, lean and thinhdr on every design of its front, as on every
   front since seed 53.

## Seeds 61 and 62, predicted (Iteration 393) - the replicates

Two runs of seed 60's start (`tag2 6h widths noevolved`), other seeds, each its own command after seed 60: how far
runs of one start spread - the owner's local-minimum question (results/convergence-seed58.md, source 3). Compared
with seed 60 at one generation, the earliest last of the three (`review-checks.py spread`); for scale, seed 58's
own fronts at generations 40, 80 and 133 differ by 5-6 points of gene usage between neighbours.

1. One basin: at the common generation the three fronts' fastest within 5% of each other, their smallest within 2%,
   their hypervolumes within 3%.
2. Tuned differently, not built differently: gene usage between any two at most 8 points apart on average, and the
   genes every tag-2 front carries (bss, lean, thinhdr) on all three.
3. No collapse in any: diversity holding as in seed 58 (`review-checks.py progress`).
4. Should one run end 5% faster or 2% smaller than the others at the common generation, runs of one start can stop
   in different places by chance - the case for an escape mechanism (an island or immigrants) after them.

## The footprint step after seed 62, and jithelp and jitre from seed 63 - predicted (Iteration 397)

1. footprint.py on seed 62's front (HANDOFF item 2): each sampled design's time per call against s6 within 2x
   of itself from N = 100 to 30,000 words - the selection's small programs no artifact of a small footprint - and
   the compile phase per word within 2x of s6's.
2. jithelp and jitre (the owner: try them) on under 10% of seed 63's front: by jitleft.py they buy little (the
   kernel's interpreted share 53.7% to 53.6%) for 4.5 KB - if so, out again after it.


## Seed 59, scored (Iteration 398)

Seed 58's start with the tag-2 requirement (results/evolve-amd-ryzen-7-pro-8840hs-seed59.md). **3 met, 1 met but for a clause, 1 missed.**

1. **Met.** Small by the five 64-bit measures, from both CPUs and from each alone. Read by the review's 3c: no evidence of anchoring at this budget - and with seed 58's evolved founders, little weight either way.
2. **Met.** Its smallest 15,915 bytes: 1.8% above the carried tag-2 runs' 15,633, 12.5% above seed 58's plain-CV8 14,146.
3. **Missed.** Its fastest at 32 bits 0.344, 11% behind seed 58's 0.310 - not the 15% predicted.
4. **Met.** No L_t2call4 death - no compile death at all at 64 bits.
5. **Met but for its last clause.** The run six minutes after the checks started (seed 58: 55); every report ends with the probes. But the Tegra's copy ran at 7,219 KB/s, not a few KB/s: its long wait is its own build.
