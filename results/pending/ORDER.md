# The after-seed-62 batch - apply in this order (against master after Iteration 393)

Prepared at Iteration 391 while seed 59 ran: re-measuring designs before they enter the fast end (the owner,
Iteration 391; results/review-methodology-386.md, 2a). Waits for seed 62's processing (Iteration 393: renamed
from after-seed-60) so that seed 60 - the anchoring test - and seeds 61-62, its replicates, all run on the
evolver of seeds 53-59: a change of evolver between them would be read as run-to-run spread.

| # | patch | what it does |
|---|---|---|
| 1 | fastgate-after-seed62.patch | evolve.py: a child whose speed is under the fast gate - 5% above the 20th fastest design alive so far - is measured again, the same rounds on the engine as built, and its speed is the geometric mean of the two (speed1 and speed2 kept in its record; memory and size the first measurement's). The fast end's in-run speeds were ~10% optimistic, designs admitted on lucky draws (a 3% noise, the best of thousands); twice the rounds where admission is decided. `--fastgate N` sets the 20; 0 turns it off. |

    git apply results/pending/fastgate-after-seed62.patch

Its cost, from seed 58's evaluations replayed through the gate: 1,121 of 24,885 measured children (4.5%) under
it, their evaluations 4.4% of the evaluation time - an upper bound on the added time, the second measurement
having no build and no 32-bit pass. The 32-bit fast end is not gated: a later step, if the first run with this
shows it worth it. What to look for in that run: `review-checks.py curse` on its report - the fastest tenth's
re-measured / in-run ratio down from seed 58's 1.112.

Tested at Iteration 391, in a scratch clone of master: fast_gate() over 30 alive designs gives 1.05 x the 20th
fastest, None with fewer alive and with --fastgate 0; a miniature run (--pop 6 --gens 2 --rounds 1 --fastgate
3) measured 3 of its 28 designs twice - 524fef96b3 0.2264 then 0.2547, 12.5% apart - each record's speed exactly
the geometric mean of its two and of its workloads' figures, its memory the first measurement's, generation 0
(no gate yet) once; exit 0.

With it applied: run-tests.sh PASS - no regressions; evolve.py --validate 7 of 7 IDENTICAL; test-jail.py PASS. On a fresh clone of
master it applies, and lab/evolve/evolve.py is then byte for byte the tested file.
