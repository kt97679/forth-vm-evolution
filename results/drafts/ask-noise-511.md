# Selecting under measurement noise in a multi-objective evolutionary search

I run a multi-objective evolutionary search over designs of a small virtual machine, and its fastest designs look
better during the run than they really are. I'd like to know which established methods fit my situation, with
references, and a concrete protocol. Where you are not sure, say so.

## The setting

- About **40,000 designs per 10-hour run** on a laptop (an 8-core AMD Ryzen 7 PRO 8840HS), four worker processes,
  each pinned to its own core.
- Each design is **built** (compiled and converted: about 1 s or more) and then **measured**: seven selection
  workloads, each run for a few rounds; a workload's time is the median CPU time of its rounds - about 10-100 ms per
  reading on a fast design. A design's **speed** is the geometric mean of its seven times, each divided by a fixed
  reference design's time (measured on the same machine, once per run).
- **Three objectives**: speed (noisy - about 2-3% between readings of the same design, more under co-runner load),
  size in bytes (exact), and peak memory (near exact). Selection keeps the Pareto front (about 150-300 designs) plus an
  archive of designs with gene values no survivor has.
- **The problem**: after a run, the fastest tenth of the front, re-measured in a quieter setting, is 7-10% slower than
  its in-run speed - every run. About half of that is load (the run measures among co-runners; the re-measure does not);
  the rest is selection: the best of thousands of noisy readings is chosen on its lucky draw (the winner's curse).
- **The mitigation now**: a child faster than 1.05 times the 20th fastest design alive is measured a second time, in
  the next generation's batch (other co-runners, another moment). Its speed was the geometric mean of the two
  readings; it is about to become the slower of the two - free, and pessimistic where the mean was optimistic.

## The questions

1. **Is "the slower of two readings" sound here?** Its bias against the mean of the two; whether it distorts the
   ranking near the gate - a design just under the gate is read once, one just over it twice and takes the slower.
2. **Which established methods fit?** Re-evaluating elites (how many, how often), adaptive averaging (Optimal Computing
   Budget Allocation, racing as in irace/F-race, successive halving), shrinking each reading toward the population's
   mean by the known noise (a regression-to-the-mean correction), noise-aware Pareto dominance (probabilistic or
   confidence-interval dominance), an archive of re-measured elites. With references.
3. **The most budget-efficient protocol for my costs** - a build costs about ten readings, so a reading is cheap next to
   a design. Concretely: how many readings for which designs, combined how (median, trimmed mean, minimum of k, mean),
   and when to stop reading.
4. **Load against luck**: how to separate the two biases, and whether measuring each design relative to a reference
   measured at the same moment, under the same load (paired, interleaved), would remove the load part - and its cost.
5. **Verifying a fix**: a protocol to show the bias is gone - what to re-measure, under what load, which statistic to
   report.

## The answer I'd like

Ranked recommendations. For each: the mechanism, its cost in readings per design, the effect to expect (numbers where
you can), the pitfalls, and references (links). Mark what you are unsure of.
