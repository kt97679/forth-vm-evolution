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
