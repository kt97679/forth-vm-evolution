# Seed 84's fast-end lead, counted - instructions, not time (Iteration 579)

**The question (576)**: the re-measure STANDS - seed 84's bred designs ahead of their founders by 0.8% in their run (the
group medians) but 4.5% re-measured idle on the laptop. Code, or the laptop's core? Counted here, deterministically: each
of the re-measure's 41 designs at 64 bits, user-space instructions on the seven selection workloads (valgrind cachegrind,
--smc-check=all for the JIT's code), against s6's, the geometric mean as evolve.py's speed (fastend-icount-579.py; the
counts fastend-icount-579.jsonl, s6's .s6.json; the timings from seed 85's chain's loadtest.md).

| group (64 bits) | n | instructions / s6, median | re-measured idle | in-run | idle per instruction | in-run per instruction |
|---|---|---|---|---|---|---|
| seed 84 bred | 22 | 0.1763 (0.1674-0.1785) | 0.1437 | 0.1346 | 0.822 | 0.759 |
| its founders, re-timed | 4 | 0.1788 (0.1778-0.1800) | 0.1504 | 0.1357 | 0.841 | 0.762 |
| the pool's fastest | 8 | 0.1875 (0.1773-0.1924) | 0.1574 | 0.1417 | 0.830 | 0.753 |

**What it says.** Of the bred designs' 4.5% lead re-measured, about 1.4% is fewer instructions - in the code, so it should
hold on any machine - and about 2.3% is the laptop running their instructions faster when idle; under the run's load that
part was 0.4%. Every workload counts the same for bred and founders except corpus, where the bred designs execute 2.4%
fewer (0.1978 against 0.2026): the parsing and compiling workload. No switch gene separates the groups (no expressed value
differs in half of them); the difference is in the word lists - superinstructions, ops10. Ranks: instructions against the
idle re-measure Spearman 0.632 over the 34, the idle against the in-run 0.842 - time is more than the count.

**For seed 86's processing**: dream's re-measure of the same 41 should show the bred lead between about 1.4% (the code
alone) and 4.5% (the laptop's idle reading); the prediction (under 2% there, 60/40) stands. A lead of 1.4% is under the
2% bar the re-measure used - if dream reads it so, the gain is real but small, as the in-run measure said.
