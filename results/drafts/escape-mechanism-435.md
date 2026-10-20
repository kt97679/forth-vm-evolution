# An escape mechanism for the fast end - options and costs (Iteration 435)

The owner asked for this after seed 62's processing (HANDOFF item 4c): runs of one start reach one basin at the small
end but stop about 5% apart at the fast end. A design note, nothing built; the choice is the owner's.

## What the replicates showed

Seeds 60, 61 and 62 - one setup, three seeds - at their common generation, 133 (review-checks.py spread): smallest
15,938, 15,939, 15,929 bytes (0.06%), hypervolume within 0.7%, fastest 0.1111, 0.1108, 0.1164 (5.05%). The fast end
stops improving early and stays where it stopped: the best speed's last gain of 2% or more came at generation 104,
75 and 45 of 138-155. Which lineage won the fast end early decides where it ends - chance, worth about 5%.

## What the evolver already does for diversity

NSGA-II-style ranking with crowding; one parent in ten from the attic (demoted designs carrying gene values the
population lost, Iteration 188); a gene borrowed from another design in 15% of children; each encoding family's best
and the 8 best by Q always survive (lab/evolve/evolve.py, the generation loop). These keep *gene values* alive. None
keeps a second *lineage* alive at the fast end: once one family of fast designs leads, crowding spreads the front
along the size axis, not across rival fast lineages.

## The options

| option | what | evaluations | expected | risk |
|---|---|---|---|---|
| A. Islands | 4 subpopulations of 64, each ranked alone; every 10 generations each sends its 2 fastest and its best by Q to the next (a ring); the run's front is all islands' together | the same | the best of four lineages within one run - toward the best replicate (0.1108 against 0.1164) | each island converges more slowly (64 against 256): the small end, now within 0.06% between runs, may take longer to reach |
| B. Immigrants, age-layered (ALPS) | new random designs enter every few generations and compete only with designs of their age, layer by layer | the same | a fresh lineage can mature before it meets the leaders | more machinery (ages, layers); random designs are mostly far from the front here |
| C. Restart on stagnation | when the fastest has not gained 2% in K generations, part of the population is reseeded from mutants of the non-leading fast designs | the same | targets exactly the stall seen | the trigger and the share are new tuning knobs |
| D. Replicates, as now | several runs, the comparison's joint front keeps the best | k runs | the best of k, known to work | k times the laptop's time |

## Recommendation

**A, islands**, as an evolver option off by default (an `islands` word in NEXT-RUN's line, EVOLVE_ISLANDS for tests) -
the simplest of the four, no new objective, no extra evaluations, and its effect is the replicates' own effect
within one run. Built kept apart (a work directory, as the register machine was), checked with a short local run for
correctness, then one run with it on the laptop against seeds 63-64 without - read at their common generation:
the fast end against theirs, the small end not worse than 0.5%.

What would make it not worth it: the small end slowed past 0.5% at the common generation, or the fast end not
better than the runs without it.
