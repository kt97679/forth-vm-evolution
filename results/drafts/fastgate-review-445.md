# The fast gate, reviewed (Iteration 445)

results/seed63-rules.md's rule 3: the fast end's optimism (review-checks.py curse: the front's fastest tenth
re-measured, 6 rounds after the run, against its in-run speed) at most 1.05, or the gate's threshold revisited. Seeds
58-64: 1.112, -, 1.066, 1.095, 1.066, 1.051, 1.085 - the gate (Iteration 391, in since seed 63) has not brought it down.
Seed 64's database (kept for the islands trial) says why.

## What the gate does

A child faster than 5% above the 20th fastest alive is measured a second time - the same rounds, the engine as built,
**at once, back to back with the first** - and its speed recorded as the geometric mean of the two (evolve.py,
evaluate()). Every measurement is the median of its rounds, the design and hand-made s6 alternating (measure()).

## What seed 64's database shows

- **The two in-run measurements agree**: 1,174 children measured twice; second / first, median 1.000, the geometric mean
  of the ratios 1.001, 51% slower the second time. No regression to the mean between them.
- **The re-measure after the run does not**: for the front's fastest tenth measured twice (7 of 16), re-measured / the
  recorded speed 1.102, / the first measurement 1.106, / the second alone 1.096.

So the optimism is not the noise of one measurement, which a second independent one would average away: the two in-run
readings share their luck. Taken back to back they share the moment - the other three workers' load on the machine, its
clock and temperature, the caches - and a design that met a kind moment meets it twice. The selection keeps exactly
those; the re-measure, in another moment, finds them about 10% slower.

## Proposed (the owner's call)

**Decorrelate the second measurement**: a gated child is measured again not at once but in a later moment - queued and
measured at the start of the next generation's batch, among other co-runners - and its speed is the geometric mean then.
Same cost as now (one more measurement for some 4% of children), no new threshold. Then rule 3 reads the effect at the
next run. As a patch after seed 65, so the islands trial is not mixed with it.
