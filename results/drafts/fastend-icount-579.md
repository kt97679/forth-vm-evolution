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

**What it says** (corrected at 581: 579's per-workload line compared the bred designs with a group that held them too -
"founder" is in both groups' labels; the medians above were right). Of the bred designs' 4.5% lead re-measured, about
1.4% is fewer instructions - in the code, so it should hold on any machine - and about 2.3% is the laptop running their
instructions faster when idle; under the run's load that part was 0.4%. Per workload, bred against founders: corpus
0.961 (0.1978 against 0.2058), apps 0.995, kernel 0.998, the other four 0.999-1.001.

**The gene** (581, fastend-knockout-581.py - one gene switched, counted): guard (-DGUARD=1) - 4df5b46d00 corpus 0.1876
with it, 0.2043 without (8.2% fewer), kernel 0.3087 against 0.3288 (6.1%); 332d4a8da1 and b27ca531b3 the same, 8-10% on
corpus. Only 3 of the 22 bred designs have it (3 of the pool's 8, none of the 4 founders) - and they are among the
fastest re-measured idle (0.1381, 0.1383, 0.1408 against the bred median 0.1437). Without guard the bred designs' corpus
median is 0.2029 against the founders' 0.2065 (1.7%): the rest is spread - hotinl 20 against 40 in most, jitimg (the outer
interpreter JIT'd: 0.3-0.5% on corpus, knocked out on four). No other gene separates the groups.

**At 32 bits** (581; fastend-icount-581-32.jsonl, run under setarch -L - the 32-bit engine's legacy-layout re-exec escapes
valgrind otherwise): seed 84's 3 bred against the pool's 4 - instructions 0.1608 against 0.1638 by the medians (1.8%
fewer), the best 0.1601 against 0.1612 (0.7%); re-measured idle the best bred 4.8% ahead, loaded 1.0% behind. The code
nearly ties at the top; the idle reading favours the bred as at 64 bits.

**For seed 86's processing**: dream's re-measure of the same 41 should show the bred lead between about 1.4% (the code
alone) and 4.5% (the laptop's idle reading); the prediction (under 2% there, 60/40) stands. A lead of 1.4% is under the
2% bar the re-measure used - if dream reads it so, the gain is real but small, as the in-run measure said.
