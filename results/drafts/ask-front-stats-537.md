# Comparing Pareto fronts across runs of a stochastic search - and deciding when to stop

I run a multi-objective evolutionary search over designs of a small virtual machine, one run a day, and I need sound
statistics for three decisions: when the search has stopped improving, whether a final "confirmation" run changes the
picture, and which designs to pick as the final set. I would like the established methods of multi-objective
benchmarking, fitted to the constraints below, with references (links) - and "unsure" where unsure.

## The setting (real figures)

- **A run**: 9-11 hours, 26,000-40,000 designs evaluated, 100-155 generations of 256 children (NSGA-II: non-dominated
  rank, then crowding). Runs are randomized (different seeds); a design's identity never repeats between runs.
- **Objectives, all minimised**: speed (a geometric mean of seven workloads' time ratios to a fixed reference; one
  reading's noise about 1%), size (engine + image bytes, exact), memory (peak RSS in KB, near exact), and the same speed
  measured at 32-bit cells (a fourth). Dominance has tolerances: 2% in speed, a few KB in memory.
- **The final fronts** (by the dominance just described): 212, 313 and 246 designs in the last three runs. Their
  extremes, from my own spread tool at generation 102 of each run:

| run | method | fastest | smallest (bytes) | least memory (KB) | the tool's hypervolume |
|---|---|---|---|---|---|
| A | six workloads | 0.1300 | 14,207 | 108 | 0.8370 |
| B | six workloads | 0.1274 | 14,199 | 108 | 0.8395 |
| C | six workloads | 0.1267 | 14,143 | 108 | 0.8419 |
| D | seven workloads | 0.1452 | 14,210 | 136 | 0.3790 |
| E | seven workloads | 0.1485 | 14,079 | 460 | 0.1880 |

  (D and E measured speed over seven workloads, so they compare with each other only; their memory figures were
  measurement faults since fixed - D's from designs that failed a workload early, E's from that workload's own data. Its hypervolume is relative to a reference point the tool derives per comparison - not fixed.)
- **The method changes often**: rarely more than two or three runs share an identical method. Each run costs a day.
- **Today's rules** (home-grown): a run is "within the spread" when its fastest, smallest and least memory are no better
  than the best of the earlier runs on the same method by more than their range; my stopping rule (just adopted) is
  "two consecutive runs on an unchanged method with no gain beyond the replicate spread on any objective". A gene the
  search has stopped using is "frozen" (removed from mutation) when, over three runs, it is on under a tenth of the
  front and in none of its fastest, smallest or best-quality (speed x size x memory) tenths; a confirmation run with
  every frozen gene re-enabled will be judged "confirmed" if no re-enabled gene reaches one of those tenths.

## The questions

1. **Comparing fronts from repeated runs**: which indicators and tests fit - hypervolume with a fixed reference point
   and normalisation (how to choose them for objectives this different in scale), rank tests across replicate runs,
   empirical attainment functions and their differences, others - and which of them make sense with two or three runs
   per method?
2. **The stopping rule**: with runs this expensive, is "two consecutive runs with no gain beyond the spread" sound? What
   are its false-stop and false-continue risks, and what would you use instead (a statistic, a minimum number of runs,
   a practically meaningful effect size)?
3. **The confirmation run**: is "no re-enabled gene in a top tenth of the front" a sound test that the frozen genes are
   worthless? What would be a better one - for instance a comparison of the front with and without those genes, or a
   test on how often they appear among the front's designs against their share of the children?
4. **Choosing the final set**: established methods for picking a few representative designs from a front of a few
   hundred - the extremes and a "knee" (knee-point detection, hypervolume contribution, a reference point) - and which
   suit four objectives with tolerances.

## The answer I'd like

For each question: the method, how to compute it (formulas or pseudocode in plain Python is fine), how many runs it
needs, its pitfalls with our constraints, and references with links. Ranked by how much each would change our decisions
for its cost. Mark what you are unsure of.
