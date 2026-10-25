# Our past front figures rechecked by the corrected rule, and "one round first" priced (Iteration 528)

The owner asked, while seed 73 runs: recheck what the old first_front shaped (results/drafts/ask-evolver-review-answers-527.md),
above all the gene votes behind the freeze of 521, then price stopping hopeless children after one round. Seeds 70-72's
full records, from their chain archives; the corrected rule as in the after-seed-73 batch.

## The fronts were not just smaller - mostly different

| seed | reported front | by dominates() | in both |
|---|---|---|---|
| 70 | 156 | 212 | 63 |
| 71 | 210 | 313 | 76 |
| 72 | 185 | 246 | 72 |

The shortcut kept designs the full rule finds dominated (a design within 2% in speed and better in 32-bit speed, total or
memory dominates under the rule; the shortcut never looked) and dropped designs the rule keeps. **About a third of each
reported front is the true front.** Selection used fronts() throughout and is untouched; what the reports, the gate's
front, the re-measure and the appbench samples said about "the front" is affected.

## The votes over seeds 70-72, both ways

Freeze candidates (11 or 12 of 12), reported: alignhot jitos **jitret** jitrp kstack msc rtfuse rtimm scale sharedcall
tail tailpn. By dominates(): alignhot **jitexec** jitrp kstack msc rtfuse rtimm scale sharedcall tail tailpn.

- **rtfuse 12 -> 11, rtimm 12 -> 11: still candidates** - their freeze stands.
- **jitret 11 -> 8: not a candidate.** By the true fronts it is in the fastest tenth in every run (seed 70: 1, 71: 1,
  72: 2 of 24) and seed 70's best-Q tenth. **The freeze of jitret rested on the wrong fronts.**
- jitexec 10 -> 12: a candidate by count, but its table bug made 70-72 unfair - its votes count from seed 74 (518).
- jitos 12 -> 10 (frozen since 495); no other gene crosses into or out of candidacy.

jitfuse in seed 72 by the true front: on 17 of 107 JIT designs, but **12 of the fastest 24** (reported: 3 of 18) - its
prediction (508: half the JIT designs, most of the fastest tenth) still fails, by less than recorded. jitmul: 11.8% of
the front, 14 of the fastest 24.

## "One round first", priced on seed 72

21,384 children measured in full after generation 0. A child that, measured, was beaten in speed by a margin by a design
measured before it - no larger, memory within MEM_TOL - against the final front by dominates():

| margin | children beaten | of them on the final front |
|---|---|---|
| 10% | 13,434 (63%) | 27 |
| 15% | 11,400 (53%) | 7 |
| 20% | 9,766 (46%) | 2 |
| 30% | 6,956 (33%) | 0 |

One round strays from three by up to 7.4% (525), so 20-30% is safe from noise. Stopped after one round, such a child
skips the other two 64-bit rounds and the whole 32-bit evaluation (a second build and its measurement) - roughly
three-fifths of its time. **At 30%: a third of the measured children stop early, nothing on the final front lost - about
a fifth more children an hour. At 20%: nearly half, two of 246 lost** (by their 32-bit speed, which a stopped child
never gets measured). Speed alone (without memory) lost more: 9 at 20%, 2 at 30%.

## Proposed (the owner's)

1. **Take jitret out of the freeze** (the after-seed-73 batch keeps rtfuse and rtimm).
2. **One round first at 30%**: after the first 64-bit round, a child beaten by 30% in that round's speed by a design
   measured before - no larger, memory within MEM_TOL - stops there, recorded "stopped after one round" with its
   one-round figures, not measured at 32 bits; one in ten measured in full anyway, as the screen's audit, to keep its
   own check. Predicted: a fifth more children an hour, the audits' full measurements off the front.
