# How long should a laptop run be? (Iteration 107)

The owner: "too long runs start to lose efficiency at the end". Measured on
the three long runs, by hours elapsed, two ways (lab tooling, one-off): the
3-objective hypervolume (speed, binary + image, memory) of everything
evaluated so far with the run's OWN measurements - noisy, and biased: a run
keeps its luckiest measurements, so its best keeps falling with sampling
alone - and the hypervolume of the FINAL front's designs born so far with
the comparison's 10-round re-measurements - honest, though early on only a
floor (most final-front designs are born late). Sizes are exact.

Seed 28 (population 256, four workers, 158 generations in 7.7 h):

| hours | noisy, share of the run's gain | honest, share | best real speed so far |
|---|---|---|---|
| 0.5 | 69% | - | - |
| 1.0 | 79% | - | - |
| 1.9 | 86% | 17% (a floor) | 0.142 |
| 2.9 | 89% | 87% | 0.142 |
| 3.9 | 91% | 90% | 0.141 |
| 4.9 | 93% | 94% | **0.133** |
| 5.8 | 96% | 97% | 0.133 |
| 7.7 | 100% | 100% | 0.132 |

Seed 27 (96 x 80, one worker, from seed 26's front): 57% of its gain in half
an hour, 76% in the first hour, 83% by 1.8 h. Seed 26 (96 x 80, from short
runs' fronts): 46% in 0.4 h, 79% by 2.5 h, still rising in its last hour.

**The owner was right**: the first hour brings ~80% of a run's gain, three
hours ~87-89%, the remaining five ~10% - and the noisy measure overstates
the tail. But the tail is not empty: seed 28's one real speed jump
(0.141 -> 0.133, confirmed by re-measurement) came between hours 4 and 5.
By generation ~100 the population crowds the front and mutation mostly makes
near-duplicates.

**So**: with new genes, a long run (9 hours) - new combinations to find, and
late real jumps happen; with nothing new (a convergence check), ~4-6 hours
gets ~90-95% of what 9 would. Untested: two ~4-hour runs back to back (the
second carrying the first's front) against one 8-hour run - a fresh
population might beat a long run's late phase.
