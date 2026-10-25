# The answers to the evolver's bug hunt, checked - two real bugs fixed (Iteration 527)

Five answers to results/drafts/ask-evolver-review-524.md (the owner, 527; two of them the same text). Every claim read
against evolve.py and, where it could be, run.

## Real, and fixed (results/pending/bughunt-evolver-after-seed73.patch)

**first_front did not follow dominates()** (answers 57 and 58 by its 2% band; 54 and 57 by the 32-bit speed). Its
staircase called a design dominated by any faster one with no more total and memory - ignoring the 2% tolerance in speed,
and with two widths the 32-bit speed altogether. Shown: two designs 1% apart in speed, equal otherwise - fronts()[0] keeps
both, first_front one; with a better 32-bit speed for the slower, fronts()[0] keeps the slower and first_front the
faster. On random populations of 25 they differed **176 times in 200**. first_front is not selection (rank() uses
fronts()), but every report, the gate, the re-measure and the appbench sample are: **seed 72's front is 246 designs, not
the 185 reported**. Now an archive by dominates() itself, each member then checked against every design of no more total
(tolerances make dominance intransitive): 0 differences in 400, 7 s for seed 72's 21,557 designs.

**A gated design whose second run failed kept its first reading** (answer 58). The re-measure combined the two readings
only when the second succeeded, and marked the design done either way: a design that timed out or printed wrong the
second time stayed alive on one lucky reading. Now it dies with the second run's failure.

**Hardening that came with it**: a run with no measurement line raised AttributeError, which evaluate() does not catch -
it would have ended the run (answers 56, 58); now a death. EVOLVE_SCREEN_AUDIT=0 divided by zero (57); now none audited.

## Not bugs

| claim | who | verdict |
|---|---|---|
| the fast gate's 1.05 lets slower designs in | 54 (and 55, the same) "high" | **wrong** - speed is a time ratio; "below 1.05 x the 20th's ratio" is "within 5% of the top 20 or faster", as meant (56 and 57 reason it through) |
| the output check compares sets, not rounds | 57, 58 "high" | **true in form, harmless in fact** - s6 is deterministic, so its set is one output and the design's must be that one in every round; it would matter only for a reference that varies |
| the 'Redefining:' strip runs before the CR removal | 57 | **wrong** - the replace is the argument to re.sub: CRs go first |
| gated designs wait forever if a whole generation is screened | 57 | **no** - every gated design waits for the next batch with children; a generation of 256 all screened has not happened (19% are) |
| OUT_LAST/RSS_LAST shared between workers | 54 | **no** - each worker is its own process |
| the gate counts gated designs' single readings | 56 | true; a matter of method, the gate's 20th is a rank among hundreds |

## The answers, ranked

58 the best: three real findings among four, each with a trigger, and the right test (first_front against fronts()[0]
on generated populations). 57 found first_front twice over, with three wrong claims beside them. 56 found the crash path
after long wandering. 54/55 (the same answer twice): one real finding (the 32-bit speed in first_front), its "high" claim
wrong.
