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
